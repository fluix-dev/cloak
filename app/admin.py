from .models import Form, FormField, Response, FormFieldResponse

from django.contrib import admin


class FormFieldInline(admin.StackedInline):
    model = FormField
    extra = 0
    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("input_type", "question"),
                    "description",
                    ("is_required", "is_secret"),
                ),
            },
        ),
    )


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ("name", "description_truncate", "is_open", "close_datetime")

    def description_truncate(self, obj):
        return obj.description[:200] + (
            "..." if len(obj.description) > 200 else ""
        )

    readonly_fields = ["uuid", "form_id"]
    fieldsets = (
        (
            "User Access",
            {"fields": ("editors", "reviewers",), "classes": ("collapse",)},
        ),
        (
            "Properties",
            {
                "fields": (
                    "name",
                    "description",
                    "is_open",
                    "close_datetime",
                    "is_public",
                    "login_required",
                    "is_single_response",
                ),
            },
        ),
        (
            "Identifiers",
            {"fields": ("uuid", "form_id",), "classes": ("collapse",)},
        ),
    )

    inlines = [
        FormFieldInline,
    ]

    # TODO: Make this hide the "Show and Add Another button"
    def change_view(self, request, object_id, form_url="", extra_context=None):
        if extra_context is None:
            extra_context = {
                "show_save": False,
                "show_save_and_add_another": False,
            }
        return super(FormAdmin, self).change_view(
            request,
            object_id=object_id,
            form_url=form_url,
            extra_context=extra_context,
        )


admin.site.register(Response)
admin.site.register(FormFieldResponse)
