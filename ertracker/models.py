from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.
class UserProfile(models.Model):
    ROLE_CHOICES =(
        ('admin','ADMIN'),
        ('doctor','DOCTOR'),
        ('nurse','NURSE'),
        ('receptionist','RECEPTIONIST'),
    )

    user = models.OneToOneField(User,on_delete=models.CASCADE)
    role = models.CharField(max_length=20,choices=ROLE_CHOICES)

    def __str__(self):
        return self.user.username

class Patient(models.Model):
    SEVERITY_CHOICES = (
        (1,'Critical'),
        (2,'High'),
        (3,'Medium'),
        (4,'Low'),
    )

    STATUS_CHOICES = (
        ('waiting','Waiting'),
        ('in_treatment','In Treatment'),
        ('admitted','Admitted'),
        ('discharged','Discharged'),
    )

    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    symptoms = models.TextField()
    severity = models.PositiveSmallIntegerField(choices=SEVERITY_CHOICES)
    arrival_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='waiting')

    def __str__(self):
        return self.name
    


class Resource(models.Model):
    name = models.CharField(max_length=25)
    total_count = models.IntegerField()
    available_count = models.IntegerField()

    def __str__(self):
        return self.name


class Specialization(models.Model):
    name = models.CharField(max_length=100,unique=True)

    def clean(self):
        self.name = self.name.strip().title()

        duplicate = Specialization.objects.filter(
            name__iexact = self.name).exclude(pk=self.pk).exists()
        
        if duplicate:
            raise ValidationError({
                'name':'This specialization already exists'
            })
        
    def save(self,*args,**kwargs):
        self.full_clean()
        super().save(*args,**kwargs)

    def __str__(self):
        return self.name

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.ForeignKey(
        Specialization,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    availability = models.BooleanField(default=True)

    def __str__(self):
        return self.name