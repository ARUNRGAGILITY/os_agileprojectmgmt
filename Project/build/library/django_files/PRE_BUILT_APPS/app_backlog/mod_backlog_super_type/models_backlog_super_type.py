
from app_common.mod_common.models_common import *

from app_backlog.mod_app.all_model_imports import *
from app_backlog.mod_app.all_form_imports import *

from app_backlog.mod_backlog_super_type.models_backlog_super_type import *
from app_backlog.mod_backlog_type.models_backlog_type import *


        
# Super Type
class BacklogSuperType(BaseModelImpl):    
     
    org = models.ForeignKey("app_organization.Organization", 
                                       on_delete=models.SET_NULL, 
                                              null=True, blank=True, 
                                              related_name='backlog_super_type_supertypes')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
                               blank=True, 
                               related_name='author_backlog_super_typesupertypes')
    def __str__(self):
        return f"{self.name}"
