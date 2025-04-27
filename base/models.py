from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.images.models import Image
from wagtail.snippets.models import register_snippet


@register_snippet
class ZoomMeetingInfo(models.Model):
    """
    Represents Zoom meeting information.
    """
    meeting_link = models.URLField(help_text="The Zoom meeting link.")
    meeting_id = models.CharField(max_length=255, help_text="The Zoom meeting ID.")
    meeting_password = models.CharField(max_length=255, help_text="The Zoom meeting password.")

    panels = [
        FieldPanel("meeting_link"),
        FieldPanel("meeting_id"),
        FieldPanel("meeting_password"),
    ]

    def __str__(self):
        return f"Zoom Meeting (ID: {self.meeting_id})"

    class Meta:
        verbose_name = "Zoom Meeting Info"
        verbose_name_plural = "Zoom Meeting Infos"


@register_snippet
class TeacherBiography(models.Model):
    name = models.CharField(max_length=255)
    biography = RichTextField()
    image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+"
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("biography"),
        FieldPanel("image"),
    ]

    def __str__(self):
        return self.name


@register_snippet
class Coordinator(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    panels = [
        FieldPanel("name"),
        FieldPanel("phone_number"),
        FieldPanel("email"),
    ]

    def __str__(self):
        return self.name


@register_snippet
class RegistrationStatus(models.Model):
    name = models.CharField(max_length=50, unique=True,
                            help_text="Name of the status (e.g., Registered, Accepted, Rejected)")
    description = models.TextField(blank=True, help_text="Optional description of the status")

    panels = [
        FieldPanel("name"),
        FieldPanel("description"),
    ]

    class Meta:
        verbose_name = "Registration Status"
        verbose_name_plural = "Registration Statuses"

    def __str__(self):
        return self.name


class BaseEvent(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    coordinators = models.ManyToManyField(
        "base.Coordinator",
        blank=True,
        related_name="events",
        help_text="Coordinators for this event.",
    )
    zoom_meeting = models.ForeignKey(
        "ZoomMeetingInfo",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="events",
        help_text="Zoom meeting information for the event."
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("description"),
        FieldPanel("start_time"),
        FieldPanel("end_time"),
        FieldPanel("coordinators"),  # Add coordinators to the admin panel
        FieldPanel("zoom_meeting"),
    ]

    def __str__(self):
        return self.title
