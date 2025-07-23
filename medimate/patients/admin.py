from django.contrib import admin
from .models import PatientProfile, Doctor, Appointment

admin.site.register(PatientProfile)
admin.site.register(Doctor)
admin.site.register(Appointment)

