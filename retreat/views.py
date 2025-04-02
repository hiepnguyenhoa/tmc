from django.shortcuts import render, get_object_or_404
from .models import RetreatDuration

def register_page(request, duration_id):
    duration = get_object_or_404(RetreatDuration, id=duration_id)
    if request.method == "POST":
        # Handle form submission here
        pass
    return render(request, 'retreat/register_page.html', {'duration': duration})
