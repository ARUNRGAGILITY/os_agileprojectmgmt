
from django.urls import path, include

from app_memberprofilerole.mod_role import views_role


urlpatterns = [
    # app_memberprofilerole/roles: DB/Model: Role
    path('list_roles/<int:org_id>/', views_role.list_roles, name='list_roles'),
    path('list_deleted_roles/<int:org_id>/', views_role.list_deleted_roles, name='list_deleted_roles'),
    path('create_role/<int:org_id>/', views_role.create_role, name='create_role'),
    path('edit_role/<int:org_id>/<int:role_id>/', views_role.edit_role, name='edit_role'),
    path('delete_role/<int:org_id>/<int:role_id>/', views_role.delete_role, name='delete_role'),
    path('permanent_deletion_role/<int:org_id>/<int:role_id>/', views_role.permanent_deletion_role, name='permanent_deletion_role'),
    path('restore_role/<int:org_id>/<int:role_id>/', views_role.restore_role, name='restore_role'),
    path('view_role/<int:org_id>/<int:role_id>/', views_role.view_role, name='view_role'),
    path('view_my_role/', views_role.view_my_role, name='view_my_role'),
]
