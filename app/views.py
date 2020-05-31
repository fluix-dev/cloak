from app.models import Form, FormFieldResponse, Response

from django.core.exceptions import PermissionDenied, SuspiciousOperation
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone


# Create your views here.
def index(request):
    return render(request, "index.html", {})


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


def fill(request, uuid, form_id):
    form = get_object_or_404(Form, uuid=uuid, form_id=form_id)
    if not form.is_open:
        raise PermissionDenied()
    if form.close_datetime and form.close_datetime < timezone.now():
        form.is_open = False
        form.save()
        raise PermissionDenied()
    context = {"form": form}
    return render(request, "fill.html", context)


def submit(request, uuid, form_id):
    form = get_object_or_404(Form, uuid=uuid, form_id=form_id)
    resp = Response(form=form, name="thing", email="aaaaa@gmail.com")
    # name=request.POST["name"],
    # email=request.POST["email"],
    resp.save()

    for field in form.fields.all():
        fieldresp = FormFieldResponse(
            form_field=field, response=resp, content=request.POST[str(field.pk)]
        )
        fieldresp.save()
    return redirect("submitted", form.uuid, form.form_id)


def submitted(request, uuid, form_id):
    context = {
        "form_name": Form.objects.get(uuid=uuid, form_id=form_id).name,
        "uuid": uuid,
        "form_id": form_id,
    }
    return render(request, "submitted.html", context)


def public_forms(request):
    context = {
        "forms": Form.objects.filter(is_public=False)
    }
    return render(request, "public.html", context)


def register(request):
    return render(request, "register.html")
