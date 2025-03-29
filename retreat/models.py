from itertools import groupby
from datetime import date

from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page

from base.models import AvailableRetreat, Coordinator, TeacherBiography


class RetreatPageAvailableRetreat(models.Model):
    page = ParentalKey(
        "RetreatPage",
        on_delete=models.CASCADE,
        related_name="retreat_page_available_retreats",
    )
    available_retreat = models.ForeignKey(
        AvailableRetreat,
        on_delete=models.CASCADE,
        related_name="+",
    )

    panels = [
        FieldPanel("available_retreat"),
    ]


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

    content_panels = Page.content_panels + [
        FieldPanel("teacher_biography"),
        MultiFieldPanel(
            [
                InlinePanel("retreat_page_available_retreats", label="Available Retreats"),
            ],
            heading="Available Retreats",
        ),
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
    ]

    parent_page_types = ["RetreatIndexPage"]
    subpage_types = []

    def grouped_available_retreats(self):
        # Get all available retreats for this page
        retreats = self.retreat_page_available_retreats.all()
        # Sort the retreats by category name (or "Uncategorized" if no category exists)
        sorted_retreats = sorted(
            retreats,
            key=lambda r: r.available_retreat.category.name if r.available_retreat.category else "Uncategorized"
        )
        # Group the sorted retreats by category name
        grouped = groupby(
            sorted_retreats,
            key=lambda r: r.available_retreat.category.name if r.available_retreat.category else "Uncategorized"
        )
        # Return grouped data as a dictionary
        return {category: list(items) for category, items in grouped}


class RetreatIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    parent_page_types = ["home.HomePage"]
    subpage_types = ["RetreatPage"]

    def grouped_available_retreats(self):
        # Get the current year
        current_year = date.today().year

        # Get all RetreatPage instances under this index page
        retreats = RetreatPage.objects.live().descendant_of(self)

        # Prepare a list of all available retreats starting in the current year or later
        available_retreats = []
        for retreat in retreats:
            # Filter available retreats by start date
            filtered_available_retreats = retreat.retreat_page_available_retreats.filter(
                available_retreat__start_date__year__gte=current_year
            )
            available_retreats.extend(filtered_available_retreats)

        # Group the available retreats by year
        grouped_by_year = groupby(
            sorted(available_retreats, key=lambda r: r.available_retreat.start_date.year),
            key=lambda r: r.available_retreat.start_date.year
        )

        # For each year, group the retreats by category
        grouped_data = {}
        for year, retreats_in_year in grouped_by_year:
            retreats_in_year = list(retreats_in_year)  # Convert groupby iterator to list
            grouped_by_category = groupby(
                sorted(
                    retreats_in_year,
                    key=lambda r: (
                        r.available_retreat.category.display_order if r.available_retreat.category else -1,
                        r.available_retreat.category.name if r.available_retreat.category else "Uncategorized",
                    ),
                ),
                key=lambda r: r.available_retreat.category.name if r.available_retreat.category else "Uncategorized"
            )
            grouped_data[year] = {category: list(items) for category, items in grouped_by_category}

        return grouped_data

    def get_context(self, request):
        context = super().get_context(request)
        context["grouped_available_retreats"] = self.grouped_available_retreats()
        return context
