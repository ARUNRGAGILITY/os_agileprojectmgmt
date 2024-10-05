from app_assessment.models_app.all_model_imports import *
from app_xpresskanban.models.delivery_models import *
from app_assessment.models_app.models_asmt import *
from app_assessment.models_app.models_assessment_questions import *

class AssessmentDetails(BaseCafeImpl):
    org = models.ForeignKey('app_xpresskanban.Organization', on_delete=models.CASCADE, 
                              related_name="org_assessment_details", null=True, blank=True)
    
    # many different combinations in this
    assessment = models.ForeignKey('app_assessment.AssessmentTemplates', on_delete=models.CASCADE,
                                related_name="assessment_details", null=True, blank=True)
    
    
    ## who can access this assessment
    accessible_to_users = models.ManyToManyField(User, related_name="users_assessment_access", blank=True)
    
    ## when they can access this assessment
    expiry_date = models.DateTimeField(null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    actual_start_date = models.DateTimeField(null=True, blank=True)
    actual_end_date = models.DateTimeField(null=True, blank=True)
    announcement_date = models.DateTimeField(null=True, blank=True)
    assessment_locked_after_end_date = models.BooleanField(default=False)
    assessment_edit_locked_after_start_date = models.BooleanField(default=False)   
    
    ## how many times they can access this assessment
    attempts_allowed = models.IntegerField(default=0)
    
    ## how many times they have accessed this assessment 
    ## what is the passing score
    passing_score = models.IntegerField(default=0)
    ## what is the passing percentage
    passing_percentage = models.IntegerField(default=0)
    
    ## negative marking
    negative_marking = models.BooleanField(default=False)
    ## consider partially correct as incorrect or not
    partially_correct_is_incorrect = models.BooleanField(default=False)
    
    ## time
    total_time_given = models.IntegerField(default=0)
    
    ## certificate
    certificate = models.BooleanField(default=False)        
    
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_assessment_details")

        
    def __str__(self):
        return self.name + ''
    
    
class AssessmentFeedback(BaseCafeImpl):
    
    # many different combinations in this
    assessment = models.ForeignKey('app_assessment.AssessmentTemplates', on_delete=models.CASCADE,
                                related_name="assessment_feedback", null=True, blank=True,)
    
    ## stars 5 stars
    stars = models.IntegerField(default=0)
    ## rating can be 1-5 or 1-10
    rating = models.IntegerField(default=0)
    
    # participant
    participant = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_feedback_participant")
    
    org = models.ForeignKey('app_xpresskanban.Organization', on_delete=models.CASCADE, 
                              related_name="org_assessment_feedback")
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_assessment_feedback")

        
    def __str__(self):
        return self.name + ''

