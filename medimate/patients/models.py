from django.db import models

class PatientProfile(models.Model):
    user = models.CharField(max_length=10)
    age = models.IntegerField()
    gender = models.CharField(max_length = 10)
    phone = models.CharField(max_length = 10)
    address = models.TextField()

    def __str__(self):        
        return self.user

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)

    def __str__(self):
        return f"Dr. {self.name} ({self.specialization})"

class Appointment(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"Appointment of {self.patient.user} with {self.doctor.name} on {self.date} at {self.time}"
