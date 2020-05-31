from .models import Form, FormField, Response, FormFieldResponse
from .utils import gen_braille

from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin


class FormFieldInline(SortableInlineAdminMixin, admin.StackedInline):
    model = FormField
    extra = 0
    verbose_name = "Click and drag to change order ::"
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "order",
                    ("input_type", "question"),
                    ("is_required", "is_secret"),
                ),
            },
        ),
        (
            "Additional",
            {
                "fields": ("description", "multiple_choices",),
                "classes": ("collapse",),
            },
        ),
    )

    def get_readonly_fields(self, request, obj):
        if obj:
            return ["is_secret"]
        return []


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    search_fields = ["name", "description"]
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


class FormFieldResponse(admin.StackedInline):
    model = FormFieldResponse
    verbose_name = ""
    extra = 0

    def get_readonly_fields(self, request, obj):
        readonly_fields = ["summary", "question"]
        if not request.user.is_superuser:
            readonly_fields += ["content"]
        return readonly_fields

    def get_fields(self, request, obj=None):
        fields = ["summary"]
        if request.GET.get("full", False):
            fields[0] = "content"
        if request.user.is_superuser:
            fields.insert(0, "form_field")

        """
        fieldsets[0][1]["fields"] = fields
        if obj and getattr(obj, "form_field").input_type == "L":
            fieldsets += (
                "Summary",
                {"fields": ("summary",), "classes": ("collapse",)},
            )
        print(fieldsets[0][1]["fields"])"""
        return fields


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    date_hierarchy = "submission_datetime"
    list_display = (
        "response_num",
        "form",
        "user_hidden",
        "name_hidden",
        "email_hidden",
        "status",
        "submission_datetime",
    )

    def response_num(self, obj):
        return "%010d" % obj.id

    response_num.short_description = "Response ID"

    def user_hidden(self, obj):
        return gen_braille() if obj.status != "A" else obj.user

    user_hidden.short_description = "User"

    def name_hidden(self, obj):
        return gen_braille() if obj.status != "A" else obj.name

    name_hidden.short_description = "Name"

    def email_hidden(self, obj):
        return gen_braille() if obj.status != "A" else obj.email

    email_hidden.short_description = "Email"

    def get_readonly_fields(self, request, obj):
        readonly_fields = [
            "submission_datetime",
            "user_hidden",
            "name_hidden",
            "email_hidden",
        ]
        if not request.user.is_superuser:
            readonly_fields += ["form", "user", "name", "email"]
        if obj and obj.status == "A":
            readonly_fields += ["status"]
        return readonly_fields

    fieldsets = (
        ("Connections", {"fields": ("form", "user_hidden",),},),
        (
            "Response",
            {
                "fields": (
                    "name_hidden",
                    "email_hidden",
                    "submission_datetime",
                    "status",
                ),
            },
        ),
    )

    inlines = [
        FormFieldResponse,
    ]
