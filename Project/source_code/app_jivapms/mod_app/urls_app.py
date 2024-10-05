from django.urls import path, include

urlpatterns = [
    path('', include('app_jivapms.mod_web.urls_web')),
   
]
