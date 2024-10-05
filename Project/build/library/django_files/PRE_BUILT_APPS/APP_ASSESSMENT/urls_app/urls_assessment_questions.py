from django.urls import path, include

from app_assessment.views_app import views_asmt
from app_assessment.views_app import views_ai
from app_assessment.views_app import views_assessment_questions


urlpatterns = [
    # app_assessment/assessment_questions: DB/Model: AssessmentQuestions
    path('list_assessment_questions/<int:areas_id>/', views_assessment_questions.list_assessment_questions, name='list_assessment_questions'),
    path('create_assessment_question/<int:areas_id>/', views_assessment_questions.create_assessment_question, name='create_assessment_question'),
    path('edit_assessment_question/<int:areas_id>/<int:question_id>/', views_assessment_questions.edit_assessment_question, name='edit_assessment_question'),
    path('delete_assessment_question/<int:areas_id>/<int:question_id>/', views_assessment_questions.delete_assessment_question, name='delete_assessment_question'),
    path('view_assessment_question/<int:areas_id>/<int:question_id>/', views_assessment_questions.view_assessment_question, name='view_assessment_question'),
    path('copy_assessment_question/<int:areas_id>/<int:question_id>/', views_assessment_questions.copy_assessment_question, name='copy_assessment_question'),
]
