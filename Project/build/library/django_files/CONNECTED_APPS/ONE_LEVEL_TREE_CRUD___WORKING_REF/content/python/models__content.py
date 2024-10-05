from app_common.mod_common.models_common import *
from __appname__.mod_app.all_model_imports import *
from __appname__.mod_app.all_form_imports import *
from __appname__.mod___singularmodname__.models___singularmodname__ import *



# Core Hierarchical System Database
class __dbmodelnameprimary__(MPTTModel, BaseModelImpl):
  
    
    __connectstr__ = models.ForeignKey("__connectappname__.__connectmoduletitle__", 
                                       on_delete=models.SET_NULL, 
                                              null=True, blank=True, 
                                              related_name='__pluralmodname__')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='__dbconnectname__', on_delete=models.CASCADE)
   
    type = TreeForeignKey("__appname__.__dbmodelnameprimary__Type", null=True, blank=True, 
                          related_name='__rootmodulename___types', 
                          on_delete=models.CASCADE)
     
    
    # for now label is a char field
    tag =  models.CharField(max_length=256,null=True, blank=True, default='')
          
   
    duration_in_hours = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
                               blank=True, related_name='author___pluralmodname__')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                             related_name='user___pluralmodname__')
   
    class MPTTMeta:
        order_insertion_by = ['position']

    def __str__(self):
        return self.name

    def get_completion_stats(self):
        total_count = self.get_descendants().filter(done=True, active=True).count() + self.get_descendants().filter(done=False, active=True).count()
        completed_count = self.get_descendants().filter(done=True, active=True).count()
        percent_complete = round((completed_count / total_count) * 100, 2) if total_count > 0 else 0.0
        #print(f"====> {completed_count}/{total_count} ===> {percent_complete}")
        return {
            'total_count': total_count,
            'completed_count': completed_count,
            'percent_complete': percent_complete,
        }
    
    def get_active_descendants(self):
        return self.get_descendants().filter(active=True)

    #
    # DEF BLOCK UNBLOCK
    #
    def block(self):
        self.blocked = "blocked"
        self.block_count += 1

    def unblock(self):
        self.blocked = "unblocked"

    ## display 
    def children(self):
        return __dbmodelnameprimary__.objects.filter(parent=self.pk, active=True)
    
    def serializable_object(self):
        obj = {'name': self.name, 'contents': []}
        for child in self.children():
            obj['children'].append(child.serializable_object())
        return obj
    
    def get_active_children(self):
        return self.get_children().filter(active=True)
