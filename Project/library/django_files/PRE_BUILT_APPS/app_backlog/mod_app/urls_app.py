from django.urls import include, path

urlpatterns = [
    path('backlog_super_type/', include('app_backlog.mod_backlog_super_type.urls_backlog_super_type')),
    path('backlog_type/', include('app_backlog.mod_backlog_type.urls_backlog_type')),
    path('backlog/', include('app_backlog.mod_backlog.urls_backlog')),
]
