from datetime import date
from itertools import groupby

from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page

from base.models import Coordinator, TeacherBiography, RetreatCategory


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


class RetreatPage(Page):
    teacher_biography = models.ForeignKey(
        TeacherBiography,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    zoom_link = models.URLField(blank=True, null=True)
    zoom_room_id = models.CharField(max_length=255, blank=True, null=True)
    zoom_room_password = models.CharField(max_length=255, blank=True, null=True)
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("teacher_biography"),
        MultiFieldPanel(
            [
                InlinePanel("coordinators", label="Coordinator"),
            ],
            heading="Coordinators",
        ),
        MultiFieldPanel(
            [
                FieldPanel("zoom_link"),
                FieldPanel("zoom_room_id"),
                FieldPanel("zoom_room_password"),
            ],
            heading="Zoom Information",
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
