from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from app.models import Form, FormFieldResponse, Response

# Create your views here.
def index(request):
    return render(request, "index.html", {})

def fill(request, uuid, form_id):
    form = get_object_or_404(Form, uuid=uuid, form_id=form_id)
    context = {"form" : form}
    return render(request,"fill.html",context)

def submit(request, uuid, form_id):
	form = get_object_or_404(Form, uuid=uuid,form_id=form_id)
	resp = Response(
		form=form,
		name="thing",email="aaaaa@gmail.com"
		)
		# name=request.POST["name"],
		# email=request.POST["email"],
	resp.save()

	for field in form.fields.all():
		fieldresp = FormFieldResponse(form_field=field,response=resp,content=request.POST[str(field.pk)])
		fieldresp.save()
	return redirect("submitted", form.uuid, form.form_id)

def submitted(request, uuid, form_id):
    context = {"form_name" : Form.objects.get(uuid=uuid,form_id=form_id).name, "uuid" : uuid, "form_id": form_id}
    return render(request,"submitted.html",context)
