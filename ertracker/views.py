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
    total_patients = Patient.objects.all().count()
    waiting_patients = Patient.objects.filter(status='waiting').count()
    in_treatment = Patient.objects.filter(status='in_treatment').count()
    discharged = Patient.objects.filter(status='dishcarge').count()
    critical_patients = Patient.objects.filter(status='Critical').count()
    bed_resource = Resource.objects.filter(name='Beds',).first()
    available_beds = bed_resource.available_count if bed_resource else 0
    total_resource = Resource.objects.all().count()
    recent_pateints = Patient.objects.all().order_by('-arrival_time')[:5]
    return render(request,'admin/dashboard.html',{
        'total_patients' : total_patients,
        'waiting_patients' : waiting_patients,
        'in_treatment' : in_treatment,
        'discharged' : discharged,
        'critical_patients' : critical_patients,
        'available_beds' : available_beds,
        'recent_pateints' : recent_pateints,
        'total_resource' : total_resource,
    })

@login_required(login_url='home')
def doctor_dashboard(request):
    waiting_patients = Patient.objects.filter(status='waiting').count()
    in_treatment = Patient.objects.filter(status='in_treatment').count()
    critical_patients = Patient.objects.filter(status='Critical').count()
    bed_resource = Resource.objects.filter(name='Beds',).first()
    available_beds = bed_resource.available_count if bed_resource else 0
    erqueue = Patient.objects.filter(status='waiting').order_by('-arrival_time')[:5]
    return render(request,'doctor/dashboard.html',{
        'waiting_patients' : waiting_patients,
        'in_treatment' : in_treatment,
        'critical_patients' : critical_patients,
        'available_beds' : available_beds,
        'erqueue' : erqueue
    })

@login_required(login_url='home')
def nurse_dashboard(request):
    waiting_patients = Patient.objects.filter(status='waiting').count()
    in_treatment = Patient.objects.filter(status='in_treatment').count()
    critical_patients = Patient.objects.filter(status='Critical').count()
    bed_resource = Resource.objects.filter(name='Beds',).first()
    available_beds = bed_resource.available_count if bed_resource else 0
    erqueue = Patient.objects.filter(status='waiting').order_by('-arrival_time')[:5]
    return render(request,'nurse/dashboard.html',{
        'waiting_patients' : waiting_patients,
        'in_treatment' : in_treatment,
        'critical_patients' : critical_patients,
        'available_beds' : available_beds,
        'erqueue' : erqueue
    })

@login_required(login_url='home')
def receptionist_dashboard(request):
    total_patients = Patient.objects.all().count()
    critical_patients = Patient.objects.filter(status='Critical').count()
    waiting_patients = Patient.objects.filter(status='waiting').count()
    bed_resource = Resource.objects.filter(name='Beds',).first()
    available_beds = bed_resource.available_count if bed_resource else 0
    patient_lists = Patient.objects.all().order_by('-arrival_time')[:5]

    return render(request,'receptionist/dashboard.html',{
        'total_patients' : total_patients,
        'critical_patients' : critical_patients,
        'waiting_patients' : waiting_patients,
        'available_beds' : available_beds,
        'patient_lists' : patient_lists
    })

#check receptionist login
def is_receptionist(user):
    return hasattr(user,'userprofile')and user.userprofile.role == 'receptionist'
#check doctor login
def is_doctor(user):
    return hasattr(user,'userprofile')and user.userprofile.role == 'doctor'

#check admin login
def is_admin(user):
    return (user.is_authenticated and(
        user.is_superuser or user.is_staff or (
        hasattr(user,'userprofile') and user.userprofile.role == 'admin'
    )
    ))

@login_required(login_url='home')
# @user_passes_test(is_receptionist,login_url='home') #only receptionist can login
def patient_list(request):
    patients = Patient.objects.all().order_by('arrival_time')
    return render(request,'patient/patient_list.html',{
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
    
    return render(request,'patient/add_patient.html',{
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

    return render(request,'patient/edit_patient.html',{
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
def erqueue(request):
    patients = Patient.objects.filter(
        status='waiting'
    ).order_by('severity','arrival_time')
    return render(request,'queue/erqueue.html',{
        'patients':patients
    })


@login_required(login_url='home')
def resource_list(request):
    resources = Resource.objects.all()
    total_doctors = Doctor.objects.all().count()
    doctor_count = Doctor.objects.filter(availability=True).count()
    return render(request,'resource/resource_list.html',{
        'resources':resources,
        'total_doctors':total_doctors,
        'doctor_count' : doctor_count
    })

# @login_required(login_url='home')
# @user_passes_test(is_admin,login_url='home') #only receptionist can login
# def specialization_list(request):
#     specializations = Specialization.objects.all()
#     return render(request,'specialization_list.html',{
#         'specializations':specializations
#     })

@login_required(login_url='home')
@user_passes_test(is_doctor,login_url='home')
def update_patient_status(request,pk):
    patient = Patient.objects.get(pk=pk)
    if request.method == 'POST':
        try:
            patient.status = request.POST.get('status') #get the value from the button
            patient.save()
            messages.success(request,'Patient status update.')
            print(request.POST)
            print(request.POST.get('status'))

        except Exception as e:
            messages.error(request,str(e))

    return redirect('patient_list')

@login_required(login_url='home')
@user_passes_test(is_admin,login_url='home')
def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request,'doctor/doctor_list.html',{
        'doctors' : doctors
    })

@login_required(login_url='home')
@user_passes_test(is_admin,login_url='home')
def edit_resource(request,pk):
    resource = get_object_or_404(
        Resource,
        pk=pk)
    if request.method == 'POST':
        form = ResourceForm(request.POST,instance=resource)

        try:
            if form.is_valid():
                form.save()
                messages.success(request,'Updated Resource Count')
        except Exception:
            messages.error(request,'Unable to Updated. Please Try Again')
    
    else:
        form = ResourceForm(instance=resource)


    return render(request,'resource/edit_resource.html',{
        'form' : form,
        'resource' : resource,
    })