from app_assessment.models_app.all_model_imports import *
from app_xpresskanban.models.delivery_models import *
from app_assessment.models_app.models_asmt import *


class AssessmentAnswers(BaseCafeImpl):
    question = models.ForeignKey('app_assessment.AssessmentQuestions', on_delete=models.CASCADE, 
                              related_name="question_answers", null=True, blank=True,)
  
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_area_answers")
    
    is_correct = models.BooleanField(default=False)
        
    def __str__(self):
        return self.name + ''
