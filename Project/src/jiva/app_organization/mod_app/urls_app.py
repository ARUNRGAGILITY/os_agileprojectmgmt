from django.urls import include, path

urlpatterns = [
    path('organization/', include('app_organization.mod_organization.urls_organization')),
    path('project/', include('app_organization.mod_project.urls_project')),
    path('work/', include('app_organization.mod_work.urls_work')),
]
