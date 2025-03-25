from itertools import groupby

from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.images.models import Image
from wagtail.models import Page
from wagtail.snippets.models import register_snippet


@register_snippet
class RetreatCategory(models.Model):
    name = models.CharField(max_length=255)

    panels = [
        FieldPanel("name"),
    ]

    class Meta:
        verbose_name_plural = "Retreat Categories"

    def __str__(self):
        return self.name


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
class AvailableRetreat(models.Model):
    category = models.ForeignKey(
        RetreatCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="available_retreats",
    )
    start_date = models.DateField()
    end_date = models.DateField()
    note = models.TextField(blank=True, null=True)

    panels = [
        FieldPanel("category"),
        FieldPanel("start_date"),
        FieldPanel("end_date"),
        FieldPanel("note"),
    ]

    def __str__(self):
        return f"{self.start_date} - {self.end_date}"


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
