from app_assessment.models_app.all_model_imports import *
from app_xpresskanban.models.delivery_models import *
from app_assessment.models_app.models_asmt import *
from app_assessment.models_app.models_assessment_questions import *

class AssessmentMaturityTypeRating5(BaseCafeImpl):
    # many different combinations in this
    assessment = models.ForeignKey('app_assessment.AssessmentTemplates', on_delete=models.CASCADE,
                                related_name="ama_rating5s", null=True, blank=True)
    
    
    participant = models.ForeignKey(User, on_delete=models.SET_NULL, 
                                    null=True, blank=True,
                                    related_name="participant_assessment_maturity_type_rating5")
    
    area = models.ForeignKey('app_assessment.AssessmentAreas', 
                             on_delete=models.SET_NULL,
                             related_name="area_ama_rating5s",
                             null=True, blank=True)
    
    question = models.ForeignKey('app_assessment.AssessmentQuestions', 
                                 on_delete=models.SET_NULL, 
                                    null=True, blank=True,
                                    related_name="qama_rating5s")
    
    rating = models.IntegerField(default=0)
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name="author_ama_rating5s")
    

    def __str__(self):
        if self.name != None:
            return self.name
        else:
            return str(self.id)