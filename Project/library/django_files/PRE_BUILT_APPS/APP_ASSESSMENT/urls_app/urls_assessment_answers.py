from django.urls import path, include

from app_assessment.views_app import views_asmt
from app_assessment.views_app import views_ai
from app_assessment.views_app import views_assessment_answers


urlpatterns = [
    # app_assessment/assessment_answers: DB/Model: AssessmentAnswers
    path('list_assessment_answers/<int:question_id>/', views_assessment_answers.list_assessment_answers, name='list_assessment_answers'),
    path('create_assessment_answer/<int:question_id>/', views_assessment_answers.create_assessment_answer, name='create_assessment_answer'),
    path('edit_assessment_answer/<int:question_id>/<int:answer_id>/', views_assessment_answers.edit_assessment_answer, name='edit_assessment_answer'),
    path('delete_assessment_answer/<int:question_id>/<int:answer_id>/', views_assessment_answers.delete_assessment_answer, name='delete_assessment_answer'),
    path('view_assessment_answer/<int:question_id>/<int:answer_id>/', views_assessment_answers.view_assessment_answer, name='view_assessment_answer'),
]
