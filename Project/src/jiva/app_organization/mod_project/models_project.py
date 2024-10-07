
from app_organization.mod_app.all_model_imports import *
from app_organization.mod_organization.models_organization import *
from app_common.mod_common.models_common import *


# No need to import Member or Role directly

class Project(BaseModelImpl):
    org = models.ForeignKey('app_organization.Organization', on_delete=models.CASCADE, 
                            related_name="org_projects", null=True, blank=True)
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_projects")
    
    # Use a string reference to break the circular dependency with Member
    members = models.ManyToManyField('app_memberprofilerole.Member', through='ProjectMembership', related_name='projects')
   
    def __str__(self):
        return self.name
    

class ProjectRole(BaseModelTrackImpl):
    role_name = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, 
                                related_name='project_roles', null=True, blank=True)
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_project_roles")
    
    def __str__(self):
        return self.role_name if self.role_name else "Empty"


class ProjectMembership(BaseModelImpl):
    member = models.ForeignKey('app_memberprofilerole.Member', on_delete=models.CASCADE, related_name='project_memberships', null=True, blank=True)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='project_members', null=True, blank=True)
    project_role = models.ForeignKey('ProjectRole', on_delete=models.CASCADE, null=True, blank=True)  # Role in the project (e.g., 'Project Admin', 'Viewer')

    def __str__(self):
        return f"{self.member.user.username} in {self.project.name} as {self.project_role.role_name}"

"""
Example Permissions Breakdown:
Organization Admin:
Can create and manage projects.
Can manage all members and roles within the organization.

Project Admin:
Can manage the specific project, assign roles, and edit project details.

Editor:
Can edit content within the project but has no permission to manage users or roles.

Viewer:
Can only view project content.
"""