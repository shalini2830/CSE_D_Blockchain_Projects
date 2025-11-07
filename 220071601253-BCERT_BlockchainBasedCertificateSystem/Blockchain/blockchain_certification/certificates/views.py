import base64
import hashlib
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
import io

from users.models import Institution
from .models import Certificate
from blockchain.models import Block
from blockchain.utils import add_certificate_to_blockchain, get_blockchain
from .utils import generate_qr_code


def _require_login(request: HttpRequest):
    if not request.session.get('institution_id'):
        return redirect('login')
    return None


def dashboard(request: HttpRequest):
    redirect_resp = _require_login(request)
    if redirect_resp:
        return redirect_resp
    qs = Certificate.objects.filter(issuer_id=request.session['institution_id']).order_by('-id')
    q = request.GET.get('q', '').strip()
    if q:
        from django.db.models import Q
        qs = qs.filter(
            Q(certificate_id__icontains=q) |
            Q(student_name__icontains=q) |
            Q(course_name__icontains=q)
        )

    # export CSV
    if request.GET.get('export') == 'csv':
        import csv
        resp = HttpResponse(content_type='text/csv')
        resp['Content-Disposition'] = 'attachment; filename="certificates.csv"'
        writer = csv.writer(resp)
        writer.writerow(['ID','Student','Course','Date','Status'])
        for c in qs:
            writer.writerow([c.certificate_id, c.student_name, c.course_name, c.issue_date, c.status])
        return resp

    # simple pagination
    from django.core.paginator import Paginator
    paginator = Paginator(qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'dashboard.html', {'certificates': page_obj.object_list, 'page_obj': page_obj})


def issue_certificate(request: HttpRequest):
    redirect_resp = _require_login(request)
    if redirect_resp:
        return redirect_resp

    if request.method == 'POST':
        student_name = request.POST.get('student_name', '').strip()
        course_name = request.POST.get('course_name', '').strip()
        issue_date_str = request.POST.get('issue_date', '').strip()
        certificate_id = request.POST.get('certificate_id', '').strip()

        if not (student_name and course_name and issue_date_str and certificate_id):
            messages.error(request, 'All fields are required')
            return render(request, 'issue_certificate.html')

        try:
            issue_date = datetime.strptime(issue_date_str, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, 'Invalid date format; expected YYYY-MM-DD')
            return render(request, 'issue_certificate.html')

        institution = get_object_or_404(Institution, pk=request.session['institution_id'])

        # Compute certificate hash (SHA-256 over canonical string)
        certificate_payload = f"{student_name}|{course_name}|{issue_date.isoformat()}|{certificate_id}|{institution.email}"
        certificate_hash = hashlib.sha256(certificate_payload.encode('utf-8')).hexdigest()

        # Add to blockchain (creates new block)
        block = add_certificate_to_blockchain(certificate_hash, issuer=institution.name)

        cert = Certificate.objects.create(
            student_name=student_name,
            course_name=course_name,
            issue_date=issue_date,
            certificate_id=certificate_id,
            blockchain_hash=certificate_hash,
            issuer=institution,
        )

        verify_url = request.build_absolute_uri(reverse('verify_certificate', args=[certificate_id]))
        qr_png = generate_qr_code(verify_url)
        qr_b64 = base64.b64encode(qr_png).decode('ascii')

        messages.success(request, 'Certificate issued and recorded on blockchain')
        return render(request, 'certificate_display.html', {
            'certificate': cert,
            'block': block,
            'qr_base64': qr_b64,
            'verify_url': verify_url,
        })

    return render(request, 'issue_certificate.html')


def verify_certificate_form(request: HttpRequest):
    if request.method == 'POST':
        certificate_id = request.POST.get('certificate_id', '').strip()
        if certificate_id:
            return redirect('verify_certificate', certificate_id=certificate_id)
    return render(request, 'verification.html')


def verify_certificate(request: HttpRequest, certificate_id: str):
    cert = Certificate.objects.filter(certificate_id=certificate_id).first()
    chain = get_blockchain()
    valid = False
    matched_block = None
    if cert:
        # Consider status; revoked certificates are invalid
        if cert.status == 'Valid':
            # Prefer direct DB lookup for reliability
            matched_block = Block.objects.filter(certificate_hash=cert.blockchain_hash).order_by('-index').first()
            valid = matched_block is not None

    context = {
        'certificate': cert,
        'block': matched_block,
        'valid': valid,
    }
    return render(request, 'verification_result.html', context)


def certificate_display(request: HttpRequest, pk: int):
    cert = get_object_or_404(Certificate, pk=pk)
    # Restrict access: only issuer can view internal display page
    if request.session.get('institution_id') and cert.issuer_id != request.session['institution_id']:
        messages.error(request, 'You do not have permission to view this certificate')
        return redirect('dashboard')
    # Find block if exists
    block = Block.objects.filter(certificate_hash=cert.blockchain_hash).order_by('-id').first()
    verify_url = request.build_absolute_uri(reverse('verify_certificate', args=[cert.certificate_id]))
    qr_png = generate_qr_code(verify_url)
    qr_b64 = base64.b64encode(qr_png).decode('ascii')
    return render(request, 'certificate_display.html', {
        'certificate': cert,
        'block': block,
        'qr_base64': qr_b64,
        'verify_url': verify_url,
    })


def revoke_certificate(request: HttpRequest, pk: int):
    redirect_resp = _require_login(request)
    if redirect_resp:
        return redirect_resp
    if request.method != 'POST':
        return redirect('dashboard')
    cert = get_object_or_404(Certificate, pk=pk)
    if cert.issuer_id != request.session['institution_id']:
        messages.error(request, 'You do not have permission to modify this certificate')
        return redirect('dashboard')
    cert.status = 'Revoked'
    cert.save(update_fields=['status'])
    messages.success(request, f'Certificate {cert.certificate_id} revoked')
    return redirect('certificate_display', pk=pk)


def reissue_certificate(request: HttpRequest, pk: int):
    redirect_resp = _require_login(request)
    if redirect_resp:
        return redirect_resp
    if request.method != 'POST':
        return redirect('dashboard')
    cert = get_object_or_404(Certificate, pk=pk)
    if cert.issuer_id != request.session['institution_id']:
        messages.error(request, 'You do not have permission to modify this certificate')
        return redirect('dashboard')
    # Re-add to blockchain to record re-issuance event using same hash
    institution = cert.issuer
    block = add_certificate_to_blockchain(cert.blockchain_hash, issuer=institution.name)
    cert.status = 'Valid'
    cert.save(update_fields=['status'])
    messages.success(request, f'Certificate {cert.certificate_id} reissued on blockchain (block #{block.index})')
    return redirect('certificate_display', pk=pk)


def reset_all(request: HttpRequest):
    """Debug utility: wipe data only for current institution; optional logout."""
    redirect_resp = _require_login(request)
    if redirect_resp:
        return redirect_resp
    if request.method == 'POST':
        inst = get_object_or_404(Institution, pk=request.session['institution_id'])
        Certificate.objects.filter(issuer=inst).delete()
        Block.objects.filter(issuer=inst.name).delete()
        if request.POST.get('logout') == '1':
            request.session.flush()
            messages.success(request, 'Data cleared for your institution and logged out')
            return redirect('home')
        messages.success(request, 'All data for your institution has been cleared')
        return redirect('dashboard')
    return render(request, 'reset.html')


def certificate_pdf(request: HttpRequest, pk: int) -> HttpResponse:
    cert = get_object_or_404(Certificate, pk=pk)
    verify_url = request.build_absolute_uri(reverse('verify_certificate', args=[cert.certificate_id]))
    qr_png = generate_qr_code(verify_url)

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    p.setFont("Helvetica-Bold", 20)
    p.drawString(72, height - 72, "Certificate of Completion")

    p.setFont("Helvetica", 12)
    y = height - 120
    p.drawString(72, y, f"Student: {cert.student_name}")
    y -= 18
    p.drawString(72, y, f"Course: {cert.course_name}")
    y -= 18
    p.drawString(72, y, f"Date: {cert.issue_date}")
    y -= 18
    p.drawString(72, y, f"Certificate ID: {cert.certificate_id}")
    y -= 18
    p.drawString(72, y, f"Status: {cert.status}")

    # QR code image
    qr_reader = ImageReader(io.BytesIO(qr_png))
    p.drawImage(qr_reader, width - 72 - 150, height - 72 - 150, 150, 150, preserveAspectRatio=True, mask='auto')
    p.setFont("Helvetica", 9)
    p.drawString(width - 72 - 150, height - 72 - 160, "Scan to verify")

    p.showPage()
    p.save()

    buffer.seek(0)
    response = HttpResponse(buffer.read(), content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="certificate_{cert.certificate_id}.pdf"'
    return response


