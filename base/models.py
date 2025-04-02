from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.images.models import Image
from wagtail.snippets.models import register_snippet


@register_snippet
class RetreatCategory(models.Model):
    name = models.CharField(max_length=255, help_text="Name of the retreat category")
    display_order = models.IntegerField(
        default=0,
        help_text="Smaller numbers appear first in the retreat index page."
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("display_order"),
    ]

    class Meta:
        ordering = ["display_order", "name"]  # Default ordering by descending display_order
        verbose_name = "Retreat Category"
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
