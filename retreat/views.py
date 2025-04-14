from django.shortcuts import render, get_object_or_404, redirect

from base.models import RegistrationStatus
from .models import RetreatPage, RetreatDuration, Registration


def register_page(request, duration_id):
    duration = get_object_or_404(RetreatDuration, id=duration_id)

    if request.method == "POST":
        # Save the registration data
        Registration.objects.create(
            retreat_duration=duration,
            first_name=request.POST.get("first_name"),
            last_name=request.POST.get("last_name"),
            sex=request.POST.get("sex"),
            address=f"{request.POST.get('address')}, {request.POST.get('city')}, {request.POST.get('state')} {request.POST.get('zipcode')}",
            phone=request.POST.get("phone"),
            email=request.POST.get("email"),
            age=request.POST.get("age"),
            emergency_contact_name=request.POST.get("emergency_contact_name"),
            emergency_contact_phone=request.POST.get("emergency_contact_phone"),
            emergency_contact_relation=request.POST.get("emergency_contact_relation"),
        )
        return redirect("success_page")  # Redirect to a success page after submission

    return render(request, "retreat/register_page.html", {"duration": duration})


def success_page(request):
    return render(request, "retreat/success_page.html")


def registrations_admin_view(request):
    if request.method == "POST":
        registration_id = request.POST.get("registration_id")
        status_id = request.POST.get("status_id")

        if registration_id and status_id:
            try:
                registration = Registration.objects.get(id=registration_id)
                new_status = RegistrationStatus.objects.get(id=status_id)
                registration.status = new_status
                registration.save()
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
