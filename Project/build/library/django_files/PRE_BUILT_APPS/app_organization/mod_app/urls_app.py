from django.urls import include, path

urlpatterns = [
    path('organization/', include('app_organization.mod_organization.urls_organization')),
]
