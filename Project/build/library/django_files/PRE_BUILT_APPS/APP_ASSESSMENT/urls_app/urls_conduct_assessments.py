
from django.urls import path, include

from app_assessment.views_app import views_asmt
from app_assessment.views_app import views_ai
from app_assessment.views_app import views_conduct_assessments


urlpatterns = [
    # app_assessment/templates: DB/Model: AssessmentTemplates
    path('conduct_assessments/<int:org_id>/', views_conduct_assessments.conduct_assessments, name='conduct_assessments'),
    path('select_assessment/<int:org_id>/', views_conduct_assessments.select_assessment, name='select_assessment'),
    path('configure_assessment/<int:org_id>/<int:template_id>/', views_conduct_assessments.configure_assessment, name='configure_assessment'),    
    path('schedule_assessment/<int:org_id>/<int:template_id>/', views_conduct_assessments.schedule_assessment, name='schedule_assessment'),
    path('assessment/<int:org_id>/<int:template_id>/', views_conduct_assessments.assessment, name='assessment'),
    path('assessment_maturity_type/<int:org_id>/<int:template_id>/', views_conduct_assessments.assessment_maturity_type, name='assessment_maturity_type'),
    path('review_assessment/<int:org_id>/<int:template_id>/', views_conduct_assessments.review_assessment, name='review_assessment'),   
    path('analyze_assessment/<int:org_id>/<int:template_id>/', views_conduct_assessments.analyze_assessment, name='analyze_assessment'),
    path('action_and_coaching_plan/<int:org_id>/<int:template_id>/', views_conduct_assessments.action_and_coaching_plan, name='action_and_coaching_plan'),
    path('test_tab/<int:org_id>/', views_conduct_assessments.test_tab, name='test_tab'),
]
