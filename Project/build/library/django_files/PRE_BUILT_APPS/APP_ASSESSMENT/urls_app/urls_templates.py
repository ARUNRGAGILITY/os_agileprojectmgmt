
from django.urls import path, include

from app_assessment.views_app import views_asmt
from app_assessment.views_app import views_ai
from app_assessment.views_app import views_templates


urlpatterns = [
    # app_assessment/templates: DB/Model: AssessmentTemplates
    path('list_templates/<int:org_id>/', views_templates.list_templates, name='list_templates'),
    path('create_template/<int:org_id>/', views_templates.create_template, name='create_template'),
    path('edit_template/<int:org_id>/<int:template_id>/', views_templates.edit_template, name='edit_template'),
    path('delete_template/<int:org_id>/<int:template_id>/', views_templates.delete_template, name='delete_template'),
    path('view_template/<int:org_id>/<int:template_id>/', views_templates.view_template, name='view_template'),
    path('view_template_tree/<int:org_id>/<int:template_id>/', views_templates.view_template_tree, name='view_template_tree'  ),
    path('copy_template/<int:org_id>/<int:template_id>/', views_templates.copy_template, name='copy_template'),
    
    path('ajax_save_element_text/', views_templates.ajax_save_element_text, name='ajax_save_element_text'),
    
]
