from django.contrib import admin
from app_assessment.models_app.models_assessment_questions import *
from app_assessment.models_app.models_assessment_answers import *
from app_assessment.models_app.models_assessment_score import *
from app_assessment.models_app.models_maturity_assessments import *
from app_assessment.models_app.models_assessments import *


class AssessmentAnswersAmdin(admin.ModelAdmin):
    list_display = ('id', 'question', 'text', 'is_correct', 'active',  'author')

class AssessmentResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'author', 'candidate', 'correct_answer_text', 'correct_answer_text', 'response_answer_text', 'incorrect_answer_text', 'response_correct',)
    
class AssessmentScoreAdmin(admin.ModelAdmin):
    list_display = ('id',  'assessment', 'candidate', 'score', 'total_score', 'passing_percentage', 'candidate_percentage', 'passing_score', 'candidate_pass', 'author')

class AssessmentDetailsAdmin(admin.ModelAdmin):
    list_display = ('id', 'org', 'assessment', 'expiry_date', 'start_date', 'end_date', 'actual_start_date', 'actual_end_date', 'announcement_date', 'assessment_locked_after_end_date', 'assessment_edit_locked_after_start_date', 'attempts_allowed', 'passing_score', 'passing_percentage', 'negative_marking', 'partially_correct_is_incorrect', 'total_time_given', 'certificate', 'author')

class AssessmentMaturityTypeRatings5Admin(admin.ModelAdmin):
    list_display = ('id', 'assessment', 'participant', 'area', 'question', 'rating', 'author')


admin.site.register(AssessmentMaturityTypeRating5, AssessmentMaturityTypeRatings5Admin)
admin.site.register(AssessmentDetails, AssessmentDetailsAdmin)
admin.site.register(AssessmentScore, AssessmentScoreAdmin)
admin.site.register(AssessmentResponse, AssessmentResponseAdmin)
admin.site.register(AssessmentAnswers, AssessmentAnswersAmdin)