from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from app_system.mod_system.models_system import *
from app_system.mod_system_type.models_system_type import *
from app_system.mod_system_super_type.models_system_super_type import *
# Register your models here.
# admin.py

class SystemSupertypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

class SystemTypeAdmin(MPTTModelAdmin):
    mptt_level_indent = 20
    list_display = ('name', 'parent', 'super_type')


class SystemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'type')


admin.site.register(SystemSuperType, SystemSupertypeAdmin)
admin.site.register(SystemType, SystemTypeAdmin)
admin.site.register(System, SystemAdmin)