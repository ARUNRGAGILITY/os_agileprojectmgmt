
from app_memberprofilerole.mod_app.all_model_imports import *
from app_organization.mod_organization.models_organization import *
from app_common.mod_common.models_common import *
from app_memberprofilerole.mod_role.models_role import *

class Member(BaseModelImpl):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, 
                             related_name="member")
    org = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True, 
                                     related_name="org_members")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_members")
   
    def __str__(self):
        if self.user != None and self.org != None:
            return f"{self.user.username}"
        else:
            return "test"
   
class MemberOrganizationRole(BaseModelImpl):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=True,
                               related_name="member_roles")
    org = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True, 
                                     related_name="mro_members")
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True,
                             related_name="role_members")
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_mro")

    class Meta:
        unique_together = ('member', 'org', 'role')

    def __str__(self):
        if self.member != None  and self.org != None and self.role != None:
            return f"{self.member.user.username} - {self.org.name} - {self.role.name}"
        else:
            return "test"