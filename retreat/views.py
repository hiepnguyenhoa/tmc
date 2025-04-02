from django.shortcuts import render, get_object_or_404, redirect
from .models import RetreatDuration, Registration

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
