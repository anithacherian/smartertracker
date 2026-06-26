from django import forms
from .models import *

class LoginForm(forms.Form):
    email = forms.EmailField(
        widget = forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email',
        })
    )

    password = forms.CharField(
        widget = forms.PasswordInput(attrs={
            'class' : 'form-control',
            'placeholder' : 'Password',
        })
    )

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name','age','symptoms','severity','status']

        widgets = {
            'name' : forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'exampleInputName',
                'placeholder': 'Enter name',
            }),
            'age' : forms.NumberInput(attrs={
                'class': 'form-control',
                'id': 'exampleInputAge',
                'placeholder': 'Enter Age',
            }),
            'symptoms' : forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'exampleInputSymptoms',
                'rows':3,
                'placeholder': 'Enter Symptoms',
            }),
            'severity' : forms.Select(attrs={
                'class': 'form-control',
                'id': 'exampleInputSeverity',
            }),
            'status' : forms.Select(attrs={
                'class': 'form-control',
                'id': 'exampleInputStatus',
            }),
        }

# class SpecializationForm(forms.ModelForm):
#     class Meta:
#         model = Specialization
#         fields = ['name']

#         widgets = {
#             'name' : forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'id': 'exampleInputName',
#                 'placeholder': 'Enter specialization name',
#             }),
#         }


# class DoctorForm(forms.ModelForm):
#     class Meta:
#         model = Resource
#         fields = ['name','specialization']

#         widgets = {
#             'name' : forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'id': 'exampleInputName',
#                 'placeholder': 'Enter name',
#             }),
#             'specialization' : forms.Select(attrs={
#                 'class': 'form-control',
#                 'id': 'exampleInputSpecialization',
#             }),
#         }

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['total_count']
        widgets = {
            'total_count' : forms.NumberInput(attrs={
                'class' : 'form-control',
                'id' : 'exampleInputTotalCount',
            }),
        }