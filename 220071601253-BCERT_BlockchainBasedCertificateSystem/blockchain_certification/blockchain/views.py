from django.shortcuts import render
from .utils import get_blockchain, is_chain_valid
from .models import Block


def _current_institution_name(request):
    inst = getattr(request, 'session', {}).get('institution_id')
    try:
        from users.models import Institution
        if inst:
            return Institution.objects.get(pk=inst).name
    except Exception:
        return None
    return None


def chain_view(request):
    inst_name = _current_institution_name(request)
    if inst_name:
        chain = list(Block.objects.filter(issuer=inst_name).order_by('index'))
    else:
        chain = get_blockchain()
    valid = is_chain_valid(chain)
    return render(request, 'chain.html', {'chain': chain, 'valid': valid})


