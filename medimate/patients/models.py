from django.db import models

class PatientProfile(models.Model):
    user = models.CharField(max_length=10)
    age = models.IntegerField()
    gender = models.CharField(max_length = 10)
    phone = models.CharField(max_length = 10)
    address = models.TextField()

def __str__(self):        
    return self.user
