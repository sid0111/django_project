from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('patient_lists/',views.patient_list, name='patient_list'),
    path('create/', views.patient_create, name='patient_create'),
    path('patients/<int:id>/edit/', views.patient_update, name='patient_update'),
    path('patients/<int:id>/delete/', views.patient_delete, name='patient_delete'),

    path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointments/create/', views.appointment_create, name='appointment_create'),
]
