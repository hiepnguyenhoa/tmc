from wagtail import hooks
from wagtail.admin.menu import MenuItem
from django.urls import path
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from .models import Registration, RetreatDuration


# Custom view to display registrations filtered by retreat
@staff_member_required
def registrations_view(request):
    retreat_id = request.GET.get("retreat")  # Get the retreat ID from the query parameters
    if retreat_id:
        registrations = Registration.objects.filter(retreat_duration__page_id=retreat_id)
        selected_retreat = RetreatDuration.objects.filter(page_id=retreat_id).first()
    else:
        registrations = Registration.objects.all()
        selected_retreat = None

    retreats = RetreatDuration.objects.values("page_id", "page__title").distinct()

    return render(
        request,
        "retreat/registrations_admin.html",
        {
            "registrations": registrations,
            "retreats": retreats,
            "selected_retreat": selected_retreat,
        },
    )


# Register the custom admin URL
@hooks.register("register_admin_urls")
def register_admin_urls():
    return [
        path("registrations/", registrations_view, name="registrations_admin"),
    ]


# Add a custom menu item for the Retreat app
@hooks.register("register_admin_menu_item")
def register_retreat_menu_item():
    return MenuItem(
        "Registrations",  # Label for the menu item
        "/admin/registrations/",  # URL for the custom view
        icon_name="form",  # Wagtail icon (e.g., "form", "date", "user")
        order=1000,  # Position in the menu
    )