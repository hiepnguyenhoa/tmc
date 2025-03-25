from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page
from wagtail.snippets.models import register_snippet


# Snippet for Teacher Biography
@register_snippet
class TeacherBiography(models.Model):
    name = models.CharField(max_length=255)
    biography = RichTextField()

    panels = [
        FieldPanel("name"),
        FieldPanel("biography"),
    ]

    def __str__(self):
        return self.name


# Snippet for Coordinator
@register_snippet
class Coordinator(models.Model):
    name = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=255)

    panels = [
        FieldPanel("name"),
        FieldPanel("contact_info"),
    ]

    def __str__(self):
        return self.name


# Retreat Page
class RetreatPage(Page):
    teacher_biography = models.ForeignKey(
        TeacherBiography,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    duration = models.CharField(max_length=255, blank=True)
    zoom_information = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("teacher_biography"),
        FieldPanel("duration"),
        FieldPanel("zoom_information"),
        MultiFieldPanel(
            [
                InlinePanel("coordinators", label="Coordinator"),
            ],
            heading="Coordinators",
        ),
    ]

    parent_page_types = ["retreat.RetreatIndexPage"]
    subpage_types = []


# Coordinator Relationship for RetreatPage
class RetreatPageCoordinator(models.Model):
    page = ParentalKey(
        RetreatPage, on_delete=models.CASCADE, related_name="coordinators"
    )
    coordinator = models.ForeignKey(
        Coordinator, on_delete=models.CASCADE, related_name="+"
    )

    panels = [
        FieldPanel("coordinator"),
    ]


class RetreatIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    template = "retreat/retreat_index_page.html"

    # Allow this page to be added under the HomePage
    parent_page_types = ["home.HomePage"]

    # Optionally, restrict the types of child pages this page can have
    subpage_types = ["retreat.RetreatPage"]
