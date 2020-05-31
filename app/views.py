from app.models import Form, FormFieldResponse, Response

from django.core.exceptions import PermissionDenied, SuspiciousOperation
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect


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
        "forms" : Form.objects.filter(is_public=True)
    }
    return render(request,"public.html",context)


def public_api(request):
    pub_forms = Form.objects.filter(is_public=True)
    resp = {
        "length" : len(pub_forms),
        "forms" : {form.get_absolute_url():form.name for form in pub_forms}
    }
    return JsonResponse(resp)


def public_api(request):
    pub_forms = Form.objects.filter(is_public=False)
    resp = {
        "length" : len(pub_forms),
        "forms" : [
            {
                "uuid" : form.uuid,
                "form_id" : form.form_id,
                "url" : form.get_absolute_url()
            } for form in pub_forms
        ]
    }
    return JsonResponse(resp)


def form_api(request,uuid,form_id):
    form = Form.objects.get(uuid=uuid,form_id=form_id)
    resp = {
        "name" : form.name,
        "description" : form.description,
        "fields" : [
            {
                "question" : field.question,
                "description" : field.description,
                "input_type" : field.input_type,
                "choices" : field.get_choices,
                "is_secret": field.is_secret,
                "is_required": field.is_required
            } for field in form.fields.all()
        ]
    }
    return JsonResponse(resp)


def form_response_api(request,uuid,form_id,pk):
    pass
