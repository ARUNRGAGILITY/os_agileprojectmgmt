from django.urls import path, include

# This is the app level urls file which will collect the
# modules urls and include them here, so that it is connected to project level urls

urlpatterns = [
    path('', include('app_loginsystem.mod_auth.urls_auth')),    
]