from app_assessment.models_app.all_model_imports import *
from app_xpresskanban.models.delivery_models import *
from app_assessment.models_app.models_asmt import *


class AssessmentQuestions(BaseCafeImpl):
    areas = models.ForeignKey('app_assessment.AssessmentAreas', on_delete=models.CASCADE, 
                              related_name="area_questions", null=True, blank=True,)
    question_type = models.ForeignKey('app_assessment.AssessmentQuestionTypes', on_delete=models.CASCADE, 
                              related_name="question_type_questions", null=True, blank=True)
    instructions = models.TextField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_area_questions")
   
        
    def __str__(self):
        if self.text != None:
            return self.text
        else:
            return str(self.id)
