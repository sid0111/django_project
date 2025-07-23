from django.shortcuts import render, redirect, get_object_or_404

from .models import PatientProfile

def patient_list(request):
    patients = PatientProfile.objects.all()
    return render(request,'patient_list.html',{'patients': patients})

def patient_create(request):
    if request.method=='POST':
        user = request.POST['user']
        age = request.POST['age']
        gender = request.POST['gender']
        phone = request.POST['phone']
        address = request.POST['address']
        PatientProfile.objects.create(user=user, age=age, gender=gender, phone = phone, address = address)
        return redirect('patient_list')
    
    return render(request, 'patient_form.html')

def patient_update(request, id):
    pat = get_object_or_404(PatientProfile, pk=id)
    if request.method == 'POST':
        pat.user = request.POST['user']
        pat.age = request.POST['age']
        pat.gender = request.POST['gender']
        pat.phone = request.POST['phone']
        pat.address = request.POST['address']
        pat.save()
        return redirect('patient_list')
    return render(request, 'patient_form.html',{'patients':pat})

def patient_delete(request, id):
    pat = get_object_or_404(PatientProfile, pk=id)
    pat.delete()
    return redirect('patient_list')
    