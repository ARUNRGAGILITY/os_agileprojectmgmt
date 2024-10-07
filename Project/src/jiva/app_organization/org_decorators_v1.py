from django.http import HttpResponseForbidden
from functools import wraps
from app_memberprofilerole.mod_role.models_role import *
from app_memberprofilerole.mod_member.models_member import *
from app_organization.mod_project.models_project import *


def project_access_required(allowed_roles=None):
    if allowed_roles is None:
        allowed_roles = ['Viewer', 'Editor', 'Admin']  # Default to these roles

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            project_id = kwargs.get('project_id')
            project = Project.objects.get(id=project_id)

            # Check if the user is a member of the organization
            try:
                member = Member.objects.get(user=request.user, organization=project.organization)
            except Member.DoesNotExist:
                return HttpResponseForbidden("You are not a member of this organization.")

            # Check if the member has a role in the project
            try:
                project_membership = ProjectMembership.objects.get(member=member, project=project)
            except ProjectMembership.DoesNotExist:
                return HttpResponseForbidden("You are not part of this project.")

            # Check if the user's role is in the allowed roles
            if project_membership.role.name not in allowed_roles:
                return HttpResponseForbidden(f"You must have one of these roles: {', '.join(allowed_roles)} to access this page.")

            # If the user has the required role, proceed to the view
            return view_func(request, *args, **kwargs)

        return _wrapped_view
    return decorator


"""
@project_access_required(allowed_roles=['Viewer', 'Editor', 'Admin'])
def project_detail_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    return render(request, 'project_detail.html', {'project': project})

@project_access_required(allowed_roles=['Editor', 'Admin'])
def project_edit_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    # Editing logic here
    return render(request, 'project_edit.html', {'project': project})

@project_access_required()
def project_general_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    return render(request, 'project_general.html', {'project': project})

"""