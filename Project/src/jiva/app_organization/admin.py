from django.contrib import admin
from app_organization.mod_project.models_project import *

from django import forms

class ProjectMembershipForm(forms.ModelForm):
    class Meta:
        model = ProjectMembership
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProjectMembershipForm, self).__init__(*args, **kwargs)

        # For existing instance
        if self.instance and self.instance.pk:
            self.fields['project_role'].queryset = ProjectRole.objects.filter(project=self.instance.project)
        else:
            # Empty queryset for new instance until a project is selected
            self.fields['project_role'].queryset = ProjectRole.objects.none()

        # In case of creating a new object with POST data, dynamically filter roles
        if 'project' in self.data:
            try:
                project_id = int(self.data.get('project'))
                self.fields['project_role'].queryset = ProjectRole.objects.filter(project_id=project_id)
            except (ValueError, TypeError):
                pass  # Invalid input, do nothing

class ProjectMembershipAdmin(admin.ModelAdmin):
    form = ProjectMembershipForm
    list_display = ('member', 'project', 'project_role', 'created_at', 'updated_at')
    
    class Media:
        js = ('admin_projectmembership.js',)  # Add your JS file here

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "project_role" and request._obj_ is not None:
            kwargs["queryset"] = ProjectRole.objects.filter(project=request._obj_.project)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        request._obj_ = obj
        return super(ProjectMembershipAdmin, self).get_form(request, obj, **kwargs)

admin.site.register(ProjectMembership, ProjectMembershipAdmin)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')

admin.site.register(Project, ProjectAdmin)

# class ProjectMembershipAdmin(admin.ModelAdmin):
#     list_display = ('member', 'project', 'project_role', 'created_at', 'updated_at')

# admin.site.register(ProjectMembership, ProjectMembershipAdmin)

class ProjectRoleAdmin(admin.ModelAdmin):
    list_display = (  'project', 'role_name', 'description', 'created_at', 'updated_at')

admin.site.register(ProjectRole, ProjectRoleAdmin)


# Register your models here.
