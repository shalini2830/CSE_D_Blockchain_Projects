from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from .models import Institution


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        try:
            inst = Institution.objects.get(email=email)
            if inst.password and (inst.password == password or check_password(password, inst.password)):
                request.session['institution_id'] = inst.id
                messages.success(request, 'Logged in successfully')
                return redirect('dashboard')
        except Institution.DoesNotExist:
            pass

        messages.error(request, 'Invalid credentials')

    return render(request, 'login.html')


def home_view(request):
    from .models import Institution
    institutions = Institution.objects.all().order_by('name')[:50]
    return render(request, 'index.html', {'institutions': institutions})


def ensure_default_institution():
    if not Institution.objects.exists():
        Institution.objects.create(
            name='Default Institution',
            email='admin@example.com',
            password=make_password('admin123'),
        )


def register_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        if not (name and email and password):
            messages.error(request, 'All fields are required')
        elif Institution.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
        else:
            inst = Institution.objects.create(name=name, email=email, password=make_password(password))
            request.session['institution_id'] = inst.id
            messages.success(request, 'Registration successful')
            return redirect('dashboard')
    return render(request, 'register.html')


def logout_view(request):
    request.session.flush()
    messages.success(request, 'Logged out')
    return redirect('home')


