from app_assessment.models_app.all_model_imports import *
from app_xpresskanban.models.delivery_models import *
from app_assessment.models_app.models_asmt import *
from app_assessment.models_app.models_assessment_questions import *

# first step
class Sample(BaseCafeImpl):
    
   
        
    def __str__(self):
        return self.name + ''


class AssessmentTemplates(BaseCafeImpl):
    org = models.ForeignKey('app_xpresskanban.Organization', on_delete=models.CASCADE, 
                              related_name="org_templates")
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_templates")
    
    assessment_type = models.ForeignKey('app_assessment.AssessmentTypes', on_delete=models.CASCADE, 
                                        related_name="assessment_types", null=True, blank=True)
    
  
    template_flag = models.BooleanField(default=True)
    
    locked_flag = models.BooleanField(default=False)
    frozen_by_date = models.DateTimeField(null=True, blank=True)
        
    def __str__(self):
        return self.name + ''

class AssessmentAreas(BaseCafeImpl):
    template = models.ForeignKey('app_assessment.AssessmentTemplates', on_delete=models.CASCADE, 
                              related_name="template_areas", null=True, blank=True,)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_areas")
   
        
    def __str__(self):
        return self.name + ''
