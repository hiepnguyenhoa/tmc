from django.db import models
from wagtail.admin.panels import FieldPanel  # Correct imports
from wagtail.fields import RichTextField
from wagtail.models import Page

from base.models import TeacherBiography  # Import TeacherBiography


class SanghaIndexPage(Page):
    """
    A container page for SanghaPage instances.
    """
    intro = RichTextField(blank=True, help_text="Introduction text for the Sangha Index Page")

    subpage_types = ['sangha.SanghaPage']  # Only allow SanghaPage as children
    parent_page_types = None  # Allow this page to be added anywhere

    max_count = 1  # Ensure only one SanghaIndexPage exists

    content_panels = Page.content_panels + [
        FieldPanel('intro'),  # Add the intro field to the admin panel
    ]

    class Meta:
        verbose_name = "Sangha Index Page"

    def get_context(self, request):
        # Add SanghaPage instances and Sangha teachers to the context
        context = super().get_context(request)
        context['sangha_pages'] = self.get_children().live().specific()

        # Serialize sangha_teachers with image URLs and page URLs
        context['sangha_teachers'] = [
            {
                'name': teacher.name,  # Use the correct field for the teacher's name
                'biography': teacher.biography,
                'portrait': teacher.image if teacher.image else None,  # Access the image field
                'page_url': SanghaPage.objects.filter(teacher=teacher).first().url if SanghaPage.objects.filter(teacher=teacher).exists() else None,  # Get the SanghaPage URL
            }
            for teacher in TeacherBiography.objects.filter(is_sangha_member=True)
        ]
        return context


class SanghaPage(Page):
    """
    Represents an individual Sangha member's page.
    """
    teacher = models.ForeignKey(
        TeacherBiography,
        on_delete=models.PROTECT,
        # limit_choices_to={'is_sangha_member': True},  # Only allow teachers with is_sangha_member=True
        related_name="sangha_pages",
        help_text="Select a teacher who is a Sangha member."
    )

    parent_page_types = ['sangha.SanghaIndexPage']  # Only allow this page under SanghaIndexPage
    subpage_types = []  # Do not allow child pages under SanghaPage

    content_panels = Page.content_panels + [
        FieldPanel('teacher'),  # Show the teacher field in the admin interface
    ]

    class Meta:
        verbose_name = "Sangha Page"

    template = "sangha/sangha_page.html"  # Specify the template

    def __str__(self):
        return self.teacher.name
