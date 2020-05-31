from django.core.exceptions import PermissionDenied, SuspiciousOperation
from django.http import Http404
from django.shortcuts import get_object_or_404, render

from app.models import Form

# Create your views here.
def index(request):
    return render(request, "index.html", {})

def fill(request, uuid, form_id):
    form = get_object_or_404(Form, uuid=uuid, form_id=form_id)
    context = {"form" : form}
    return render(request,"fill.html",context)

def submit(request, uuid, form_id):
    pass


def debug_400(request):
    if request.user.is_superuser:
        raise SuspiciousOperation("Debugging...")
    raise Http404()


def debug_403(request):
    if request.user.is_superuser:
        raise PermissionDenied()
    raise Http404()


def debug_500(request):
    if request.user.is_superuser:
        raise Exception()
    raise Http404()
