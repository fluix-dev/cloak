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
