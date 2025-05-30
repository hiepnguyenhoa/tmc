from datetime import date
from itertools import groupby

from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page

from base.models import Coordinator, TeacherBiography, RetreatCategory, RegistrationStatus, ZoomInformation
from sangha.models import SanghaPage


class RetreatPageCoordinator(models.Model):
    page = ParentalKey(
        "RetreatPage",
        on_delete=models.CASCADE,
        related_name="coordinators",
    )
    coordinator = models.ForeignKey(
        Coordinator,
        on_delete=models.CASCADE,
        related_name="+",
    )

    panels = [
        FieldPanel("coordinator"),
    ]


class RetreatDuration(models.Model):
    page = ParentalKey(
        "RetreatPage",
        on_delete=models.CASCADE,
        related_name="retreat_durations",
    )
    start_date = models.DateField()
    end_date = models.DateField()
    category = models.ForeignKey(
        RetreatCategory,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="retreat_durations",
        help_text="Category of the retreat (e.g., 7-Day Retreat)",
    )

    panels = [
        FieldPanel("category"),  # This allows selecting a category in the admin interface
        FieldPanel("start_date"),
        FieldPanel("end_date"),
    ]

    def __str__(self):
        return f"{self.category.name if self.category else 'Uncategorized'}: {self.start_date} - {self.end_date}"


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
    teacher_biography = models.ForeignKey(
        TeacherBiography,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    zoom_information = models.ForeignKey(
        ZoomInformation,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Select the Zoom information for this retreat.",
    )
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("teacher_biography"),
        FieldPanel("zoom_information"),  # Add the Zoom information snippet
        MultiFieldPanel(
            [
                InlinePanel("coordinators", label="Coordinator"),
            ],
            heading="Coordinators",
        ),
        FieldPanel("intro"),
        InlinePanel("retreat_durations", label="Retreat Durations"),
    ]

    parent_page_types = ["RetreatIndexPage"]
    subpage_types = []

    def grouped_available_retreats(self):
        # Get the current year
        current_year = date.today().year

        # Filter retreat durations by start date in the current year or later
        durations = self.retreat_durations.filter(start_date__year__gte=current_year)

        # Group by category
        grouped = groupby(
            sorted(
                durations,
                key=lambda d: d.category.name if d.category else '',
            ),
            key=lambda d: d.category.name if d.category else '',
        )

        return {category: list(items) for category, items in grouped}

    def grouped_retreat_durations(self):
        # Get all retreat durations for this page
        durations = self.retreat_durations.all()

        # Group durations by category
        grouped = groupby(
            sorted(durations, key=lambda d: d.category.name if d.category else "Uncategorized"),
            key=lambda d: d.category.name if d.category else "Uncategorized",
        )

        # Return grouped data as a dictionary
        return {category: list(items) for category, items in grouped}

    def get_context(self, request):
        context = super().get_context(request)

        # Get the SanghaPage associated with the teacher_biography
        sangha_page = SanghaPage.objects.filter(teacher=self.teacher_biography).first()
        context["sangha_page_url"] = sangha_page.url if sangha_page else None

        return context


class RetreatIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    parent_page_types = ["wagtailcore.Page"]
    subpage_types = ["RetreatPage"]

    max_count = 1

    def grouped_available_retreats(self):
        # Get the current year
        current_year = date.today().year

        # Get all RetreatPage instances under this index page
        retreats = RetreatPage.objects.live().descendant_of(self)

        # Prepare a list of all retreat durations starting in the current year or later
        retreat_durations = []
        for retreat in retreats:
            # Filter retreat durations by start date
            filtered_durations = retreat.retreat_durations.filter(start_date__year__gte=current_year)
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
