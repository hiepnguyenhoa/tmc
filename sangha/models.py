from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.models import Image


class SanghaIndexPage(Page):
    """
    A container page for SanghaPage instances.
    """
    subpage_types = ['sangha.SanghaPage']  # Only allow SanghaPage as children
    parent_page_types = ['home.HomePage']  # Only allow this page under HomePage

    max_count = 1  # Ensure only one SanghaIndexPage exists

    class Meta:
        verbose_name = "Sangha Index Page"

    def get_context(self, request):
        # Add SanghaPage instances to the context
        context = super().get_context(request)
        context['sangha_pages'] = self.get_children().live().specific()
        return context


class SanghaPage(Page):
    """
    A page representing an individual Sangha member.
    """
    name = models.CharField(max_length=255, help_text="Name of the Sangha member")
    biography = RichTextField(blank=True, help_text="Biography of the Sangha member")
    portrait = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Portrait of the Sangha member"
    )

    parent_page_types = ['sangha.SanghaIndexPage']  # Only allow this page under SanghaIndexPage
    subpage_types = []  # Do not allow child pages under SanghaPage

    content_panels = Page.content_panels + [
        FieldPanel('name'),
        FieldPanel('biography'),
        ImageChooserPanel('portrait'),
    ]

    class Meta:
        verbose_name = "Sangha Page"
