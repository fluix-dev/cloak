from . import views

from django.urls import path, include
from django_registration.backends.one_step.views import RegistrationView

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

    path(
        "accounts/register/",
        RegistrationView.as_view(success_url="/admin/"),
        name="django_registration_register",
    ),
    path("accounts/", include("django_registration.backends.one_step.urls")),
    path("accounts/", include("django.contrib.auth.urls")),

    path("api/forms/public/", views.public_api),
    path("api/form/<uuid:uuid>/<str:form_id>/", views.form_api),

    path("debug/400/", views.debug_400),
    path("debug/403/", views.debug_403),
    path("debug/500/", views.debug_500),
]
