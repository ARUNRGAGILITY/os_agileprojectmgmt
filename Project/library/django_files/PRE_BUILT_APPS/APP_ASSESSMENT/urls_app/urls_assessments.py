
from django.urls import path, include

from app_assessment.views_app import views_asmt
from app_assessment.views_app import views_ai
from app_assessment.views_app import views_assessments


urlpatterns = [
    # app_assessment/templates: DB/Model: AssessmentTemplates
    path('list_assessments/<int:org_id>/', views_assessments.list_assessments, name='list_assessments'),
    path('create_assessment/<int:org_id>/', views_assessments.create_assessment, name='create_assessment'),
    path('edit_assessment/<int:org_id>/<int:template_id>/', views_assessments.edit_assessment, name='edit_assessment'),
    path('delete_assessment/<int:org_id>/<int:template_id>/', views_assessments.delete_assessment, name='delete_assessment'),
    path('view_assessment/<int:org_id>/<int:template_id>/', views_assessments.view_assessment, name='view_assessment'),
    path('view_assessment_tree/<int:org_id>/<int:template_id>/', views_assessments.view_assessment_tree, name='view_assessment_tree'  ),
    path('copy_assessment/<int:org_id>/<int:template_id>/', views_assessments.copy_assessment, name='copy_assessment'),
 
    
]
