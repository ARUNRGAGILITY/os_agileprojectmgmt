
from app_memberprofilerole.mod_app.all_model_imports import *
from app_organization.mod_organization.models_organization import *
from app_common.mod_common.models_common import *

class Role(BaseModelImpl):
    
    org = models.ForeignKey('app_organization.Organization', on_delete=models.CASCADE, 
                            related_name="org_roles", null=True, blank=True)
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_roles")
   
        
    def __str__(self):
        return self.name


