from django.urls import path, include

urlpatterns = [
    path('pw/', include('app_zweb1.urls_app.urls_personal_workspace')),   
    
    path('drawing/', include('app_zweb1.urls_app.urls_drawing')),

]
