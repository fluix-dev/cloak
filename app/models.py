import secrets
import uuid

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone


class Form(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    editors = models.ManyToManyField(
        User,
        verbose_name="Editors",
        related_name="edited_forms",
        blank=True,
        help_text="Users that will be able to edit this form.",
    )
    reviewers = models.ManyToManyField(
        User,
        verbose_name="Reviewers",
        related_name="reviewed_forms",
        blank=True,
        help_text="Users that will be able to seee this forms responses.",
    )
    name = models.CharField(
        verbose_name="Name", max_length=255, help_text="The name of this form."
    )
    description = models.TextField(
        verbose_name="Description",
        max_length=1024,
        blank=True,
        help_text="A description for this form that describes its purpose.",
    )
    is_open = models.BooleanField(
        verbose_name="Open",
        default=True,
        help_text="Whether this form is accepting responses.",
    )
    close_datetime = models.DateTimeField(
        verbose_name="Auto-Close Date",
        null=True,
        blank=True,
        help_text="Optional date and time on which the form will automatically "
        + "stop accepting responses. Leave blank to disable.",
    )
    is_public = models.BooleanField(
        verbose_name="Publicly Displayed",
        default=False,
        help_text="Whether this form is displayed on the front page of this "
        + "site. Great for advertising your form!",
    )
    login_required = models.BooleanField(
        verbose_name="Requires login",
        default=False,
        help_text="Whether a user is required to make an account to fill out "
        + "this form.",
    )
    is_single_response = models.BooleanField(
        verbose_name="Single Response",
        default=True,
        help_text="Whether users are only allowed to submit one response. Only "
        + "works when 'Requires Login' is also enabled.",
    )
    form_id = models.CharField(
        verbose_name="Random Form ID",
        max_length=128,
        editable=False,
        help_text="Securely randomly generated base 64 encoded bytes used for "
        + "form url.",
    )

    def clean(self):
        if (
            self.is_open
            and self.close_datetime
            and self.close_datetime <= timezone.now()
        ):
            raise ValidationError("Auto-Close Date must be in the future.")

    def __str__(self):
        return self.name


@receiver(pre_save, sender=Form)
def generate_form_id(sender, instance, **kwargs):
    instance.form_id = secrets.token_urlsafe(64)


class FormField(models.Model):
    form = models.ForeignKey(
        Form,
        verbose_name="Form",
        related_name="fields",
        on_delete=models.CASCADE,
    )
    INPUT_TYPE_CHOICES = [
        ("M", "Multiple Choice"),
        ("N", "Numeric"),
        ("S", "Short Answer"),
        ("L", "Long Answer"),
    ]
    input_type = models.CharField(
        verbose_name="Input Type",
        max_length=1,
        choices=INPUT_TYPE_CHOICES,
        default="S",
        help_text="Type of input.",
    )
    is_required = models.BooleanField(
        verbose_name="Required",
        default=True,
        help_text="Whether this field is required to be filled in.",
    )
    is_secret = models.BooleanField(
        verbose_name="Secret",
        default=False,
        help_text="Whether this field will be completely hidden from reviewers "
        + "until the application is accepted.",
    )
    question = models.CharField(
        verbose_name="Question",
        max_length=255,
        help_text="Question displayed to the user.",
    )
    description = models.TextField(
        verbose_name="Description",
        max_length=1024,
        blank=True,
        help_text="A description that will be shown under the question in "
        + "smaller text.",
    )
    multiple_choices = models.TextField(
        verbose_name="Multiple Choice Choices",
        max_length=1024,
        blank=True,
        help_text="The choices for a multiple choice field. Include one option "
        + "per line. This field will be ignored for fields that aren't "
        + "Multiple Choice ones.",
    )
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta(object):
        ordering = ["order"]

    def __str__(self):
        return self.question


class Response(models.Model):
    form = models.ForeignKey(
        Form,
        verbose_name="Form",
        related_name="responses",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        verbose_name="User",
        related_name="responses",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text="The user who submitted this response. null if no account "
        + "was used.",
    )
    name = models.CharField(
        verbose_name="Full Name", max_length=255, help_text="Name of submitter."
    )
    email = models.EmailField(
        verbose_name="Email", help_text="Email address to use for contact."
    )
    submission_datetime = models.DateTimeField(
        verbose_name="Submission Date",
        auto_now_add=True,
        help_text="Date and time of this response.",
    )
    STATUS_CHOICES = [
        ("P", "Pending"),
        ("R", "Rejected"),
        ("A", "Accepted"),
    ]
    status = models.CharField(
        verbose_name="Status",
        max_length=1,
        choices=STATUS_CHOICES,
        default="P",
        help_text="Status of this response. Mark as accepted to view secrets "
        + "and send submitter an acceptance email. Once marked as accepted, "
        + "the status cannot be changed.",
    )

    def __str__(self):
        return "Form Response (%d)" % self.pk


class FormFieldResponse(models.Model):
    form_field = models.ForeignKey(
        FormField,
        verbose_name="Form Field",
        related_name="responses",
        on_delete=models.CASCADE,
    )
    response = models.ForeignKey(
        Response,
        verbose_name="Response",
        related_name="fields",
        on_delete=models.CASCADE,
    )
    content = models.TextField(
        max_length=8191,
        verbose_name="Content",
        help_text="A JSON data object for storing response data.",
    )

    def parse_content():
        pass

    def __str__(self):
        return self.form_field.question
