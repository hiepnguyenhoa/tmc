from datetime import date
from itertools import groupby

from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page
from wagtail.snippets.models import register_snippet

from base.models import TeacherBiography, RegistrationStatus, BaseEvent


@register_snippet
class RetreatCategory(models.Model):
    name = models.CharField(max_length=255, unique=True, help_text="Name of the retreat category")
    display_order = models.IntegerField(
        default=0,
        help_text="Higher numbers appear first in the retreat index page."
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("display_order"),
    ]

    class Meta:
        ordering = ["-display_order", "name"]  # Default ordering by descending display_order
        verbose_name = "Retreat Category"
        verbose_name_plural = "Retreat Categories"

    def __str__(self):
        return self.name


class RetreatDuration(models.Model):
    category = models.ForeignKey(
        RetreatCategory,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="retreat_durations",
        help_text="Category of the retreat (e.g., 7-Day Retreat)",
    )
    retreat_event = ParentalKey(  # Changed to ParentalKey
        "RetreatEvent",
        on_delete=models.CASCADE,
        related_name="retreat_durations",
        help_text="The retreat event this duration belongs to.",
    )
    start_date = models.DateField(help_text="The start date of the retreat duration.")
    end_date = models.DateField(help_text="The end date of the retreat duration.")

    panels = [
        FieldPanel("category"),
        FieldPanel("start_date"),
        FieldPanel("end_date"),
    ]

    def __str__(self):
        return f"{self.category.name if self.category else 'Uncategorized'}: {self.start_date} - {self.end_date}"


class RetreatEvent(BaseEvent, ClusterableModel):
    """
    Represents a retreat event with additional properties.
    """
    retreat_page = ParentalKey(
        "RetreatPage",
        on_delete=models.CASCADE,
        related_name="retreat_event",
        help_text="The retreat page this event belongs to.",
    )
    teacher_biography = models.ForeignKey(
        TeacherBiography,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = BaseEvent.panels + [
        FieldPanel("teacher_biography"),
        FieldPanel("zoom_meeting"),
        InlinePanel("retreat_durations", label="Retreat Durations"),
    ]

    def after_save(self):
        """
        Custom logic to handle ManyToMany relationships after saving.
        """
        if hasattr(self, "_coordinators_to_set"):
            print("DEBUG: Setting coordinators:", self._coordinators_to_set)
            self.coordinators.set(self._coordinators_to_set)
            del self._coordinators_to_set

    def set_coordinators(self, coordinators):
        """
        Temporarily store coordinators to be set after the object is saved.
        """
        if self.pk:
            # If the object is already saved, set coordinators immediately
            self.coordinators.set(coordinators)
        else:
            # Otherwise, store coordinators to be set after saving
            self._coordinators_to_set = coordinators


class Registration(models.Model):
    retreat_duration = models.ForeignKey(
        RetreatDuration,
        on_delete=models.CASCADE,
        related_name="registrations",
        help_text="The retreat duration the user is registering for.",
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    sex = models.CharField(
        max_length=50,
        choices=[("male", "Male"), ("female", "Female"), ("monk", "Monk"), ("nun", "Nun")],
    )
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    age = models.CharField(
        max_length=50,
        choices=[
            ("18-19", "18-19"),
            ("20-30", "20-30"),
            ("30-40", "30-40"),
            ("40-50", "40-50"),
            ("50-60", "50-60"),
            ("60-70", "60-70"),
            ("70-80", "70-80"),
            ("over 80", "Over 80"),
        ],
    )
    emergency_contact_name = models.CharField(max_length=255)
    emergency_contact_phone = models.CharField(max_length=20)
    emergency_contact_relation = models.CharField(max_length=255)
    status = models.ForeignKey(
        RegistrationStatus,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="registrations",
        help_text="The current status of the registration.",
    )
    pdf_path = models.CharField(max_length=255, null=True, blank=True)  # Path to the uploaded PDF file

    def save(self, *args, **kwargs):
        # Set the initial status to "Registered" if not already set
        if not self.status:
            self.status, _ = RegistrationStatus.objects.get_or_create(
                name="Registered",
                defaults={"description": "Default status for new registrations."},
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.retreat_duration} ({self.status})"

    class Meta:
        verbose_name = "Registration"
        verbose_name_plural = "Registrations"


class RetreatPage(Page):
    """
    Represents a retreat page with an associated retreat event.
    """
    content_panels = Page.content_panels + [
        InlinePanel("retreat_event", label="Retreat Events"),  # Use InlinePanel to manage RetreatEvent
    ]

    parent_page_types = ["RetreatIndexPage"]
    subpage_types = []

    def get_context(self, request):
        """
        Adds retreat event properties to the context for the template.
        """
        context = super().get_context(request)
        retreat_event = self.retreat_event.first()  # Access the related RetreatEvent
        context["retreat_event"] = retreat_event
        context["teacher_biography"] = retreat_event.teacher_biography if retreat_event else None

        # Fix: Call .all() on coordinators to make it iterable
        context["coordinators"] = retreat_event.coordinators.all() if retreat_event and retreat_event.coordinators else None

        context["zoom_meeting"] = retreat_event.zoom_meeting if retreat_event else None

        # Debug print statement
        print("DEBUG: zoom_meeting =", context["zoom_meeting"])

        return context


class RetreatIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    parent_page_types = ["wagtailcore.Page"]
    subpage_types = ["RetreatPage"]

    def grouped_available_retreats(self):
        # Get the current year
        current_year = date.today().year

        # Get all RetreatPage instances under this index page
        retreats = RetreatPage.objects.live().descendant_of(self)

        # Prepare a list of all retreat durations starting in the current year or later
        retreat_durations = []
        for retreat in retreats:
            # Filter retreat durations by start date
            filtered_durations = retreat.retreat_event.retreat_durations.filter(start_date__year__gte=current_year)
            retreat_durations.extend(filtered_durations)

        # Group durations by year
        grouped_by_year = groupby(
            sorted(retreat_durations, key=lambda d: d.start_date.year),
            key=lambda d: d.start_date.year,
        )

        # For each year, group the durations by category
        grouped_data = {}
        for year, durations_in_year in grouped_by_year:
            durations_in_year = list(durations_in_year)  # Convert groupby iterator to list
            grouped_by_category = groupby(
                sorted(
                    durations_in_year,
                    key=lambda d: (
                        d.category.display_order if d.category else -1,
                        d.category.name if d.category else "Uncategorized",
                    ),
                ),
                key=lambda d: d.category.name if d.category else "Uncategorized",
            )
            grouped_data[year] = {category: list(items) for category, items in grouped_by_category}

        return grouped_data

    def get_context(self, request):
        context = super().get_context(request)
        context["grouped_available_retreats"] = self.grouped_available_retreats()
        return context
