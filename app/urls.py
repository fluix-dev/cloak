from . import views

from django.urls import path

urlpatterns = [
    path("", views.index, name="index"),
    path("public/", views.public_forms, name="public"),
    path("form/<uuid:uuid>/<str:form_id>/", views.fill, name="fill"),
    path("form/<uuid:uuid>/<str:form_id>/submit/", views.submit, name="submit"),
    path(
        "form/<uuid:uuid>/<str:form_id>/submitted/",
        views.submitted,
        name="submitted",
    ),
    path("debug/400/", views.debug_400),
    path("debug/403/", views.debug_403),
    path("debug/500/", views.debug_500),
]
