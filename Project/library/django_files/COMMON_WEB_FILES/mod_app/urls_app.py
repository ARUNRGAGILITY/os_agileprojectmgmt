from django.urls import path, include

urlpatterns = [
    path('', include('app_web.mod_web.urls_web')),
   
]
