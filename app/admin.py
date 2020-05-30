from .models import Form, FormField, Response, FormFieldResponse

from django.contrib import admin


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ("name", "description_truncate", "is_open", "close_datetime")

    def description_truncate(self, obj):
        return obj.description[:200] + (
            "..." if len(obj.description) > 200 else ""
        )

    readonly_fields = ['uuid', 'form_id']
    fieldsets = (
        (
            "User Access",
            {
                "fields": (
                    "editors",
                    "reviewers",
                ),
                "classes": (
                    "collapse",
                )
            },
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
            {
                "fields": (
                    "uuid",
                    "form_id",
                ),
                "classes": (
                    "collapse",
                )
            },
        )
    )


admin.site.register(FormField)
admin.site.register(Response)
admin.site.register(FormFieldResponse)
