"""
URL configuration for smartertracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ertracker import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.loginpage,name='home'),
    # path('login/',views.loginpage,name='login'),
    path('logout/',views.logoutpage,name='logout'),
    path('admin-dashboard/',views.admin_dashboard,name='admin_dashboard'),
    path('doctor-dashboard/',views.doctor_dashboard,name='doctor_dashboard'),
    path('nurse-dashboard/',views.nurse_dashboard,name='nurse_dashboard'),
    path('receptionist-dashboard/',views.receptionist_dashboard,name='receptionist_dashboard'),
    path('patients/',views.patient_list,name='patient_list'),
    path('patients/add/',views.add_patient,name='add_patient'),
    path('patients/edit/<int:pk>',views.edit_patient,name='edit_patient'),
    path('patients/delete/<int:pk>',views.delete_patient,name='delete_patient'),
    path('patients/erqueue',views.erqueue,name='erqueue'),
    path('resource/',views.resource_list,name='resource_list'),
    path('patient/update_status/<int:pk>',views.update_patient_status,name='update_patient_status'),
    # path('specialization_list/',views.specialization_list,name='specialization_list'),
    # path('specialization/',views.add_specialization,name='add_specialization'),
    path('resource/<int:pk>',views.edit_resource,name='edit_resource'),
    path('doctor_list/',views.doctor_list,name='doctor_list'),
]
