
from app_organization.mod_app.all_model_imports import *
from app_common.mod_common.models_common import *

class Organization(BaseModelImpl):
    #org = models.ForeignKey('', on_delete=models.CASCADE, related_name="org_")
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_Organization")
   
        
    def __str__(self):
        return self.name
