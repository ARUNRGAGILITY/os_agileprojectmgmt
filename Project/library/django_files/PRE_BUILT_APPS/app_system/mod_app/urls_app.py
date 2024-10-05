from django.urls import include, path

urlpatterns = [
    path('system_super_type/', include('app_system.mod_system_super_type.urls_system_super_type')),
    path('system_type/', include('app_system.mod_system_type.urls_system_type')),
    path('system/', include('app_system.mod_system.urls_system')),
]
