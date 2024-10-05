from django.urls import path, include

from app_assessment.views_app import views_asmt
from app_assessment.views_app import views_ai
from app_assessment.views_app import views_areas


urlpatterns = [
    # app_assessment/areas: DB/Model: AssessmentAreas
    path('list_areas/<int:template_id>/', views_areas.list_areas, name='list_areas'),
    path('create_area/<int:template_id>/', views_areas.create_area, name='create_area'),
    path('edit_area/<int:template_id>/<int:area_id>/', views_areas.edit_area, name='edit_area'),
    path('delete_area/<int:template_id>/<int:area_id>/', views_areas.delete_area, name='delete_area'),
    path('view_area/<int:template_id>/<int:area_id>/', views_areas.view_area, name='view_area'),
    path('copy_area/<int:template_id>/<int:area_id>/', views_areas.copy_area, name='copy_area'),
]
