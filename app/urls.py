from . import views

from django.urls import path

urlpatterns = [
    path("", views.index, name="index"),
    path("form/<uuid:uuid>/<str:form_id>/", views.fill, name="fill"),
    path("form/<uuid:uuid>/<str:form_id>/submit/", views.submit, name="submit"),
]
