from django.urls import path, include

from app_assessment.views_app import views_asmt
from app_assessment.views_app import views_ai
from app_assessment.views_app import views_question_types


urlpatterns = [
    # app_assessment/question_types: DB/Model: AssessmentQuestionTypes
    path('list_question_types/<int:org_id>/', views_question_types.list_question_types, name='list_question_types'),
    path('create_question_type/<int:org_id>/', views_question_types.create_question_type, name='create_question_type'),
    path('edit_question_type/<int:org_id>/<int:question_type_id>/', views_question_types.edit_question_type, name='edit_question_type'),
    path('delete_question_type/<int:org_id>/<int:question_type_id>/', views_question_types.delete_question_type, name='delete_question_type'),
    path('view_question_type/<int:org_id>/<int:question_type_id>/', views_question_types.view_question_type, name='view_question_type'),
]
