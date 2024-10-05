from app_assessment.models_app.all_model_imports import *
from app_xpresskanban.models.delivery_models import *
from app_assessment.models_app.models_asmt import *


class AssessmentAttempts(BaseCafeImpl):
    assessment = models.ForeignKey('app_assessment.AssessmentTemplates', on_delete=models.CASCADE, 
                              related_name="assessment_attempts", null=True, blank=True,)
    candidate = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="user_attempts")
    total_attempts = models.IntegerField(default=0)
   
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_attempts")
   
        
    def __str__(self):
        return self.name + ''




class AssessmentScore(BaseCafeImpl):
    assessment = models.ForeignKey('app_assessment.AssessmentTemplates', on_delete=models.CASCADE, 
                              related_name="assessment_scores", null=True, blank=True,)
    candidate = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="user_scores")
    score = models.IntegerField(default=0)
    total_score = models.IntegerField(default=0)
    passing_percentage = models.IntegerField(default=0)
    candidate_percentage = models.IntegerField(default=0)
    passing_score = models.IntegerField(default=0)
    candidate_pass = models.BooleanField(default=False)
   
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_scores")
   
        
    def __str__(self):
        return self.name + ''


class AssessmentResponse(BaseCafeImpl):
    question = models.ForeignKey('app_assessment.AssessmentQuestions', on_delete=models.CASCADE, 
                              related_name="question_responses", null=True, blank=True,)
    correct_answer_text = models.TextField(null=True, blank=True)
    response_answer_text = models.TextField(null=True, blank=True)
    incorrect_answer_text = models.TextField(null=True, blank=True)
    
    response_correct = models.BooleanField(default=False)
    additional_answers = models.BooleanField(default=False)
    
    candidate = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="user_responses")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_responses")
   
        
   
    def __str__(self):
        return self.name + ''

