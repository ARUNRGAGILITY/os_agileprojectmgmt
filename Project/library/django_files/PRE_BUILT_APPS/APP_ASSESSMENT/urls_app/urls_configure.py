from django.urls import path, include

from app_assessment.views_app import views_asmt
from app_assessment.views_app import views_ai
from app_assessment.views_app import views_configure


urlpatterns = [
    # app_assessment configure
    path('configure_home/<int:org_id>/', views_configure.configure_home, name='configure_home'),
   
]
