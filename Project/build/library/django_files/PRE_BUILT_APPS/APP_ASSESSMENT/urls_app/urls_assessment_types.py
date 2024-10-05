from django.urls import path, include

from app_assessment.views_app import views_asmt
from app_assessment.views_app import views_ai
from app_assessment.views_app import views_assessment_types


urlpatterns = [
    # app_assessment/assessment_types: DB/Model: AssessmentTypes
    path('list_assessment_types/<int:org_id>/', views_assessment_types.list_assessment_types, name='list_assessment_types'),
    path('create_assessment_type/<int:org_id>/', views_assessment_types.create_assessment_type, name='create_assessment_type'),
    path('edit_assessment_type/<int:org_id>/<int:type_id>/', views_assessment_types.edit_assessment_type, name='edit_assessment_type'),
    path('delete_assessment_type/<int:org_id>/<int:type_id>/', views_assessment_types.delete_assessment_type, name='delete_assessment_type'),
    path('view_assessment_type/<int:org_id>/<int:type_id>/', views_assessment_types.view_assessment_type, name='view_assessment_type'),
]
