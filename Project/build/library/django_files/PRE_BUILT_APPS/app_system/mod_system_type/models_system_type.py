
from app_common.mod_common.models_common import *
from app_system.mod_app.all_model_imports import *
from app_system.mod_app.all_form_imports import *
from app_system.mod_system_type.models_system_type import *
from app_system.mod_system_super_type.models_system_super_type import *


# Core Models
class SystemType(MPTTModel, BaseModelImpl):
     
    org = models.ForeignKey("app_organization.Organization", 
                                       on_delete=models.SET_NULL, 
                                              null=True, blank=True, 
                                              related_name='system_type_types')
    parent = TreeForeignKey('self', null=True, blank=True, 
                            related_name='supertype', on_delete=models.CASCADE)
    super_type = models.ForeignKey("app_system.SystemSuperType", 
                                   on_delete=models.CASCADE,
                                      related_name='supertype_systemtypes', 
                                  null=True, blank=True)
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
                               blank=True, related_name='author_systemtypes')
    
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="user_systemtypes")
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
        return SystemType.objects.filter(parent=self.pk, active=True)
    
    def serializable_object(self):
        obj = {'name': self.name, 'children': []}
        for child in self.children():
            obj['children'].append(child.serializable_object())
        return obj

