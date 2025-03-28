from itertools import groupby

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

    parent_page_types = ["home.HomePage"]  # Allow this page to be added under the HomePage
    subpage_types = ["RetreatPage"]  # Restrict the types of child pages this page can have
