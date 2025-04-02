from django.contrib import admin
from .models import RetreatDuration, Registration

class RegistrationAdmin(admin.ModelAdmin):
    list_display = ("retreat_duration", "first_name", "last_name", "email", "phone", "age", "sex")
    list_filter = ("retreat_duration", "age", "sex")
    search_fields = ("first_name", "last_name", "email", "phone")

admin.site.register(Registration, RegistrationAdmin)

class RetreatDurationAdmin(admin.ModelAdmin):
    list_display = ("page", "start_date", "end_date", "category")
    list_filter = ("category",)
    search_fields = ("page__title", "category__name")

admin.site.register(RetreatDuration, RetreatDurationAdmin)
