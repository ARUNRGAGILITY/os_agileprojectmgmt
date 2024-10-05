
from app_memberprofilerole.mod_app.all_model_imports import *
from app_organization.mod_organization.models_organization import *
from app_common.mod_common.models_common import *

class Regcode(BaseModelImpl):
    reg_code = models.CharField(max_length=250, default='A1B2C3D4E5F6', 
                                null=False, blank=False)
    org = models.ForeignKey('app_organization.Organization', on_delete=models.CASCADE, 
                            related_name="org_regcodes", null=True, blank=True)
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_regcodes")
   
        
  
    def __str__(self):
        return str(self.reg_code)
    