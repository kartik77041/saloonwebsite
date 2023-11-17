from atexit import register
from django.contrib import admin
from .models import *

admin.site.register(Profile)
admin.site.register((Comments))

@admin.register(schedule_info)
class GroupModelAdmin(admin.ModelAdmin):
    list_dispaly = ['fname', 'lname','date','phone_number']
