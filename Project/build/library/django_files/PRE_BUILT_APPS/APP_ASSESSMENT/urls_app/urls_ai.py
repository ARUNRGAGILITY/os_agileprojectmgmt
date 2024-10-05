
from django.urls import path, include


from app_assessment.views_app import views_ai


urlpatterns = [
    # AI related
    path('sample_asmt/<int:org_id>/', views_ai.sample_asmt, name='sample_asmt'),
]
