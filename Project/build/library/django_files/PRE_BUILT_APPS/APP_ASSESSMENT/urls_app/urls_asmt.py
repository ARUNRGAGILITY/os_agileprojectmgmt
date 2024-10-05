from django.urls import path, include

from app_assessment.views_app import views_asmt


urlpatterns = [
   path('asmt_home/<int:org_id>/', views_asmt.asmt_home, name='asmt_home'),
   
   
  
]