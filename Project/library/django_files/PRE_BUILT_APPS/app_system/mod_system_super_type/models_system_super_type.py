
from app_common.mod_common.models_common import *

from app_system.mod_app.all_model_imports import *
from app_system.mod_app.all_form_imports import *

from app_system.mod_system_super_type.models_system_super_type import *
from app_system.mod_system_type.models_system_type import *


        
# Super Type
class SystemSuperType(BaseModelImpl):    
     
    org = models.ForeignKey("app_organization.Organization", 
                                       on_delete=models.SET_NULL, 
                                              null=True, blank=True, 
                                              related_name='system_super_type_supertypes')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
                               blank=True, 
                               related_name='author_system_super_typesupertypes')
    def __str__(self):
        return f"{self.name}"
