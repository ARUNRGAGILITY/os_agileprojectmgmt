from django.urls import path, include

urlpatterns = [
    path('common_ajax/', include('app_common.mod_common.urls_common')),
   
]
