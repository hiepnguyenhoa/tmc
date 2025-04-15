from django.shortcuts import render, get_object_or_404, redirect
from django.core.files.storage import FileSystemStorage

from base.models import RegistrationStatus
from .models import RetreatPage, RetreatDuration, Registration
from .ultil import extract_and_create_registration


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
    print("DEBUG: registrations_admin_view called")
    if request.method == "POST":
        # Handle file upload
        if "upload_pdf" in request.POST:
            uploaded_file = request.FILES.get("pdf_file")
            if uploaded_file:
                fs = FileSystemStorage(location="media/registrations/")
                filename = fs.save(uploaded_file.name, uploaded_file)
                file_path = fs.path(filename)

                # Extract information and create a registration
                retreat_duration_id = 1  # Replace with the actual retreat duration ID
                extract_and_create_registration(file_path, retreat_duration_id)

                print(f"DEBUG: File uploaded and registration created from {file_path}")
            return redirect("registrations_admin")  # Redirect after upload

        # Handle status updates
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

    # Fetch all unique retreats
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
