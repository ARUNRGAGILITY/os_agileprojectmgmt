from app_assessment.models_app.all_model_imports import *
from app_xpresskanban.models.delivery_models import *
from app_assessment.models_app.models_asmt import *

class AssessmentTemplateTypes(BaseCafeImpl):
    org = models.ForeignKey('app_xpresskanban.Organization', on_delete=models.CASCADE, 
                              related_name="org_template_types")
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_template_types")
   
        
    def __str__(self):
        return self.name + ''

