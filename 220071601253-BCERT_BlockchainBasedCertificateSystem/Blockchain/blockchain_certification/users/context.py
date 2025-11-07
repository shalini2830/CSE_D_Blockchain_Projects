from .models import Institution


def current_institution(request):
    inst_id = request.session.get('institution_id')
    institution = None
    if inst_id:
        try:
            institution = Institution.objects.get(pk=inst_id)
        except Institution.DoesNotExist:
            institution = None
    return {'current_institution': institution}


