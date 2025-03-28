from wagtail.fields import RichTextField
from wagtail.models import Page


class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + ["intro"]
