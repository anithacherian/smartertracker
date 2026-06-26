from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.shortcuts import redirect, render, get_object_or_404
from .forms import *
from django.contrib.auth.models import User
from .models import *


DASHBOARD_BY_ROLE = {
    'admin': 'admin_dashboard',
    'doctor': 'doctor_dashboard',
    'nurse': 'nurse_dashboard',
    'receptionist': 'receptionist_dashboard',
}

# Create your views here.
def indexpage(request):
    return render(request,'login.html')

def loginpage(request):
    form = LoginForm()

    # if request.user.is_authenticated:
    #     return redirect_dashboard(request.user)
    
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                user_obj = User.objects.get(email=email)
                user = authenticate(request,username=user_obj.username,password=password)
            
            except User.DoesNotExist:
                user = None 

            if user is not None: #check user is not null
                login(request,user)
                return redirect_dashboard(user)
        
            messages.error(request,'Invalid email or password')
    
    return render(request,'login.html',{'form':form})

def redirect_dashboard(user):
    role = getattr(getattr(user,'userprofile', None), 'role', None)
    if user.is_superuser or user.is_staff:
        return redirect('admin_dashboard')


    # if role == 'admin':
    #     return redirect('admin_dashboard')
    #     elif role == 'doctor':
    #         return redirect('doctor_dashboard')
    #     elif role == 'nurse':
    #         return redirect('nurse_dashboard')
    #     elif role == 'receptionist':
    #         return redirect('receptionist_dashboard')
    
    dashboard_name =  DASHBOARD_BY_ROLE.get(role)
    if dashboard_name:
        return redirect(dashboard_name)
    return redirect('home')

def logoutpage(request):
    logout(request)
    return redirect('home')


@login_required(login_url='home')
def admin_dashboard(request):
    return render(request,'admin_dashboard.html')

@login_required(login_url='home')
def doctor_dashboard(request):
    return render(request,'doctor_dashboard.html')

@login_required(login_url='home')
def nurse_dashboard(request):
    return render(request,'nurse_dashboard.html')

@login_required(login_url='home')
def receptionist_dashboard(request):
    return render(request,'receptionist_dashboard.html')

#check receptionist login
def is_receptionist(user):
    return hasattr(user,'userprofile')and user.userprofile.role == 'receptionist'

#check admin login
def is_admin(user):
    return (user.is_authenticated and(
        user.is_superuser or user.is_staff or (
        hasattr(user,'userprofile') and user.userprofile.role == 'admin'
    )
    ))

@login_required(login_url='home')
@user_passes_test(is_receptionist,login_url='home') #only receptionist can login
def patient_list(request):
    patients = Patient.objects.all().order_by('arrival_time')
    return render(request,'patient_list.html',{
        'patients':patients
    })


@login_required(login_url='home')
@user_passes_test(is_receptionist,login_url='home') #only receptionist can login
def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        
        if form.is_valid():
            form.save()

            messages.success(request,'Patient Details Added Successfully')
            return redirect('patient_list')
        
        print(form.errors)
        messages.error(request,'Unable to Add Patient Details. Please Try Again.')
    else: 
        form = PatientForm()
    
    return render(request,'add_patient.html',{
        'form':form
    })


@login_required(login_url='home')
@user_passes_test(is_receptionist,login_url='home') #only receptionist can login
def edit_patient(request,pk):
    patients = get_object_or_404(
        Patient,
        pk=pk
    )
    if request.method == 'POST':
        form = PatientForm(request.POST,instance=patients)

        try:
            if form.is_valid():
                form.save()
                messages.success(request,'Patient Details Updated Successfully.')
        
        except Exception:
            messages.error(request,'Unable to Edit. Please Try Again')


    else:
        form = PatientForm(instance=patients)

    return render(request,'edit_patient.html',{
        'form':form
    })

@login_required(login_url='home')
@user_passes_test(is_receptionist,login_url='home') #only receptionist can login
def delete_patient(request,pk):
    patient = get_object_or_404(
        Patient,
        pk=pk
    )

    # if request.method == 'POST':
    try:
        patient.delete()
        messages.success(request,'Patient Deleted Successfully')
    except Exception:
        messages.error(request,'Unable to delete. Please Try Again')

    return redirect(patient_list)

@login_required(login_url='home')
@user_passes_test(is_receptionist,login_url='home') #only receptionist can login
def erqueue(request):
    patients = Patient.objects.filter(
        status='waiting'
    ).order_by('severity','arrival_time')
    return render(request,'erqueue.html',{
        'patients':patients
    })


@login_required(login_url='home')
def resource_list(request):
    resources = Resource.objects.all()
    total_doctors = Doctor.objects.all().count()
    docotor_count = Doctor.objects.filter(availability=True).count()
    return render(request,'resource_list.html',{
        'resources':resources,
        'total_doctors':total_doctors,
        'doctor_count' : docotor_count
    })

@login_required(login_url='home')
@user_passes_test(is_admin,login_url='home') #only receptionist can login
def specialization_list(request):
    specializations = Specialization.objects.all()
    return render(request,'specialization_list.html',{
        'specializations':specializations
    })




@login_required(login_url='home')
@user_passes_test(is_admin,login_url='home') #only receptionist can login
def add_specialization(request):
    if request.method == 'POST':
        form = SpecializationForm(request.POST)
        
        if form.is_valid():
            form.save()

            messages.success(request,'Specialization Added Successfully')
            return redirect('res')
        
        print(form.errors)
        messages.error(request,'Unable to Add Specialization. Please Try Again.')
    else: 
        form = SpecializationForm()
    
    return render(request,'add_specialization.html',{
        'form':form
    })


@login_required(login_url='home')
@user_passes_test(is_admin,login_url='home') #only receptionist can login
def add_resource(request):
    if request.method == 'POST':
        form = SpecializationForm(request.POST)
        
        if form.is_valid():
            form.save()

            messages.success(request,'Doctor Added Successfully')
            return redirect('res')
        
        print(form.errors)
        messages.error(request,'Unable to Add Specialization. Please Try Again.')
    else: 
        form = SpecializationForm()
    
    return render(request,'add_specialization.html',{
        'form':form
    })
