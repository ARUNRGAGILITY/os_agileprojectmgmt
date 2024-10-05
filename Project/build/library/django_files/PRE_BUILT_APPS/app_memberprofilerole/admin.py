from django.contrib import admin
from app_memberprofilerole.mod_member.models_member import *
from app_memberprofilerole.mod_profile.models_profile import *
from app_memberprofilerole.mod_role.models_role import *

class MemberOrganizationRoleAdmin(admin.ModelAdmin):
    list_display = ('member', 'org', 'role', 'created_at', 'updated_at')

class MemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'org',  'created_at', 'updated_at')

class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'org', 'author',  'created_at', 'updated_at')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'org', 'author', 'created_at', 'updated_at')

admin.site.register(MemberOrganizationRole, MemberOrganizationRoleAdmin)
admin.site.register(Member, MemberAdmin)

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Role, RoleAdmin)

# Register your models here.
