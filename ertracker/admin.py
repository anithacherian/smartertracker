from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Patient)
admin.site.register(Resource)
admin.site.register(Specialization)
admin.site.register(Doctor)
