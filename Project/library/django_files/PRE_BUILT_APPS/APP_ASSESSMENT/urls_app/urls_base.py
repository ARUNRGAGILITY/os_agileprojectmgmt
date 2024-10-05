from django.urls import path, include

urlpatterns = [
    path('asmt/', include('app_assessment.urls_app.urls_asmt')),
    path('asmt/ai/', include('app_assessment.urls_app.urls_ai')),
    path('asmt/templates/', include('app_assessment.urls_app.urls_templates')),
    path('asmt/areas/', include('app_assessment.urls_app.urls_areas')),
    path('asmt/cfg/', include('app_assessment.urls_app.urls_configure')),
    path('asmt/tt/', include('app_assessment.urls_app.urls_template_types')),
    path('asmt/qt/', include('app_assessment.urls_app.urls_question_types')),
    path('asmt/aq/', include('app_assessment.urls_app.urls_assessment_questions')),
    path('asmt/aa/', include('app_assessment.urls_app.urls_assessment_answers')),
    path('asmt/inst/', include('app_assessment.urls_app.urls_assessments')),   
    path('asmt/cat/', include('app_assessment.urls_app.urls_conduct_assessments')), 
    path('asmt/atypes/', include('app_assessment.urls_app.urls_assessment_types')), 

]
