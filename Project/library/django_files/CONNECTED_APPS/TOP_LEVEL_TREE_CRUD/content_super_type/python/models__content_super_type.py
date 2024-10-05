
from app_common.mod_common.models_common import *

from __appname__.mod_app.all_model_imports import *
from __appname__.mod_app.all_form_imports import *

from __appname__.mod___singularmodname__.models___singularmodname__ import *
from __appname__.mod___rootmodulename___type.models___rootmodulename___type import *


        
# Super Type
class __dbmodelnameprimary__SuperType(BaseModelImpl):    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
                               blank=True, 
                               related_name='author___singularmodname__supertypes')
    def __str__(self):
        return f"{self.name}"
