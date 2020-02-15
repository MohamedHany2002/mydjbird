from django.contrib import admin
from .models import profile,user_lastseen
# Register your models here.

admin.site.register(profile)
admin.site.register(user_lastseen)
