
from app_common.mod_common.models_common import *
from __appname__.mod_app.all_model_imports import *
from __appname__.mod_app.all_form_imports import *
from __appname__.mod___singularmodname__.models___singularmodname__ import *
from __appname__.mod___rootmodulename___super_type.models___rootmodulename___super_type import *


# Core Models
class __dbmodelnameprimary__Type(MPTTModel, BaseModelImpl):
     
    __connectstr__ = models.ForeignKey("__connectappname__.__connectmoduletitle__", 
                                       on_delete=models.SET_NULL, 
                                              null=True, blank=True, 
                                              related_name='__singularmodname___types')
    parent = TreeForeignKey('self', null=True, blank=True, 
                            related_name='supertype', on_delete=models.CASCADE)
    super_type = models.ForeignKey("__appname__.__dbmodelnameprimary__SuperType", 
                                   on_delete=models.CASCADE,
                                      related_name='supertype___rootmodname__types', 
                                  null=True, blank=True)
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
                               blank=True, related_name='author___rootmodname__types')
    
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="user___rootmodname__types")
    class MPTTMeta:
        order_insertion_by = ['position']

    def __str__(self):
        return self.name
   
    def get_active_descendants(self):
        return self.get_descendants().filter(active=True)
    
    def get_parent_id(self):
        if self.parent:
            return self.parent.id
        return None

    ## display 
    def children(self):
        return __dbmodelnameprimary__Type.objects.filter(parent=self.pk, active=True)
    
    def serializable_object(self):
        obj = {'name': self.name, 'children': []}
        for child in self.children():
            obj['children'].append(child.serializable_object())
        return obj

