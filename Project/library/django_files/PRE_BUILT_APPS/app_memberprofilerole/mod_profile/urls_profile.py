
from django.urls import path, include

from app_memberprofilerole.mod_profile import views_profile


urlpatterns = [
    # app_memberprofilerole/profiles: DB/Model: Profile
    path('list_profiles/<int:org_id>/', views_profile.list_profiles, name='list_profiles'),
    path('list_deleted_profiles/<int:org_id>/', views_profile.list_deleted_profiles, name='list_deleted_profiles'),
    path('create_profile/<int:org_id>/', views_profile.create_profile, name='create_profile'),
    path('edit_profile/<int:org_id>/<int:profile_id>/', views_profile.edit_profile, name='edit_profile'),
    path('delete_profile/<int:org_id>/<int:profile_id>/', views_profile.delete_profile, name='delete_profile'),
    path('permanent_deletion_profile/<int:org_id>/<int:profile_id>/', views_profile.permanent_deletion_profile, name='permanent_deletion_profile'),
    path('restore_profile/<int:org_id>/<int:profile_id>/', views_profile.restore_profile, name='restore_profile'),
    path('view_profile/<int:org_id>/<int:profile_id>/', views_profile.view_profile, name='view_profile'),
    path('display_profile/', views_profile.display_profile, name='display_profile'),
]
