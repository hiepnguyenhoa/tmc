from django.contrib import admin
from django.shortcuts import render, redirect
from .models import RetreatDuration, Registration, RetreatPage
from base.models import RegistrationStatus


class RegistrationAdmin(admin.ModelAdmin):
    list_display = ("retreat_duration", "first_name", "last_name", "email", "phone", "status")
    list_editable = ("status",)  # Allow inline editing of the status
    list_filter = ("retreat_duration", "status")
    search_fields = ("first_name", "last_name", "email", "phone")
    actions = ["mark_as_accepted", "mark_as_rejected"]

    def mark_as_accepted(self, request, queryset):
        accepted_status, _ = RegistrationStatus.objects.get_or_create(
            name="Accepted",
            defaults={"description": "Registration has been accepted."},
        )
        queryset.update(status=accepted_status)
        self.message_user(request, "Selected registrations have been marked as Accepted.")

    mark_as_accepted.short_description = "Mark selected registrations as Accepted"

    def mark_as_rejected(self, request, queryset):
        rejected_status, _ = RegistrationStatus.objects.get_or_create(
            name="Rejected",
            defaults={"description": "Registration has been rejected."},
        )
        queryset.update(status=rejected_status)
        self.message_user(request, "Selected registrations have been marked as Rejected.")

    mark_as_rejected.short_description = "Mark selected registrations as Rejected"


admin.site.register(Registration, RegistrationAdmin)


@admin.register(RetreatDuration)
class RetreatDurationAdmin(admin.ModelAdmin):
    list_display = ("retreat_event", "category", "start_date", "end_date")
    list_filter = ("category", "start_date", "end_date")
    search_fields = ("retreat_event__title", "category__name")


def registrations_admin_view(request):
    print("DEBUG: registrations_admin_view called")
    if request.method == "POST":
        registration_id = request.POST.get("registration_id")
        status_id = request.POST.get("status_id")
        print(f"DEBUG: registration_id={registration_id}, status_id={status_id}")  # Debugging

        if registration_id and status_id:
            try:
                registration = Registration.objects.get(id=registration_id)
                new_status = RegistrationStatus.objects.get(id=status_id)
                registration.status = new_status
                registration.save()
                print(f"DEBUG: Updated registration {registration_id} to status {new_status.name}")  # Debugging
            except (Registration.DoesNotExist, RegistrationStatus.DoesNotExist) as e:
                print(f"ERROR: {e}")  # Debugging
        return redirect("registrations_admin")  # Redirect to the same page after updating

    # Fetch all unique retreats (RetreatPage)
    retreats = RetreatPage.objects.live()  # Fetch only live RetreatPages
    selected_retreat_id = request.GET.get("retreat")
    registrations = Registration.objects.select_related("retreat_duration__page").all()

    # Filter registrations by selected retreat
    selected_retreat = None
    if selected_retreat_id:
        try:
            selected_retreat = RetreatPage.objects.get(id=selected_retreat_id)
            registrations = registrations.filter(retreat_duration__page=selected_retreat)
        except RetreatPage.DoesNotExist:
            print(f"ERROR: RetreatPage with ID {selected_retreat_id} does not exist.")  # Debugging

    statuses = RegistrationStatus.objects.all()
    print(f"DEBUG: Retreats: {retreats}")
    print(f"DEBUG: Registrations: {registrations}")
    print(f"DEBUG: Statuses: {statuses}")

    return render(
        request,
        "retreat/registrations_admin.html",
        {
            "registrations": registrations,
            "statuses": statuses,
            "retreats": retreats,
            "selected_retreat": selected_retreat,
        },
    )
