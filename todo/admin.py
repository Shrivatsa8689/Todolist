from django.contrib import admin
from .models import list

class adminn(admin.ModelAdmin):
    readonly_fields= ('created',)

admin.site.register(list,adminn)

