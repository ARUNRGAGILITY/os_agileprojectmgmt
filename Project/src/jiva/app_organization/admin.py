from django.contrib import admin
from app_organization.mod_project.models_project import *

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
admin.site.register(Project, ProjectAdmin)

class ProjectMembershipAdmin(admin.ModelAdmin):
    list_display = ('member', 'project', 'project_role', 'created_at', 'updated_at')

admin.site.register(ProjectMembership, ProjectMembershipAdmin)

class ProjectRoleAdmin(admin.ModelAdmin):
    list_display = (  'role_type', 'description', 'created_at', 'updated_at')

admin.site.register(ProjectRole, ProjectRoleAdmin)


# Register your models here.
