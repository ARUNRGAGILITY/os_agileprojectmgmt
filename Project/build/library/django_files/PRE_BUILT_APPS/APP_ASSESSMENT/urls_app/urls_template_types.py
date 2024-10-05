from django.urls import path, include

from app_assessment.views_app import views_asmt
from app_assessment.views_app import views_ai
from app_assessment.views_app import views_template_types


urlpatterns = [
    # app_assessment/template_types: DB/Model: AssessmentTemplateTypes
    path('list_template_types/<int:org_id>/', views_template_types.list_template_types, name='list_template_types'),
    path('create_template_type/<int:org_id>/', views_template_types.create_template_type, name='create_template_type'),
    path('edit_template_type/<int:org_id>/<int:template_type_id>/', views_template_types.edit_template_type, name='edit_template_type'),
    path('delete_template_type/<int:org_id>/<int:template_type_id>/', views_template_types.delete_template_type, name='delete_template_type'),
    path('view_template_type/<int:org_id>/<int:template_type_id>/', views_template_types.view_template_type, name='view_template_type'),
]
