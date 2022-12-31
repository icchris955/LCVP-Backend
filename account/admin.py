from django.contrib import admin
from .models import CustomUser, AdditionalInfo


admin.site.register(CustomUser)
admin.site.register(AdditionalInfo)
