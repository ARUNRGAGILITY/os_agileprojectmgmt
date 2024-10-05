
from django.urls import path, include

from app_memberprofilerole.mod_member import views_member


urlpatterns = [
    # app_memberprofilerole/members: DB/Model: Member
    path('list_members/<int:org_id>/', views_member.list_members, name='list_members'),
    path('list_deleted_members/<int:org_id>/', views_member.list_deleted_members, name='list_deleted_members'),
    path('create_member/<int:org_id>/', views_member.create_member, name='create_member'),
    path('edit_member/<int:org_id>/<int:member_id>/', views_member.edit_member, name='edit_member'),
    path('delete_member/<int:org_id>/<int:member_id>/', views_member.delete_member, name='delete_member'),
    path('permanent_deletion_member/<int:org_id>/<int:member_id>/', views_member.permanent_deletion_member, name='permanent_deletion_member'),
    path('restore_member/<int:org_id>/<int:member_id>/', views_member.restore_member, name='restore_member'),
    path('view_member/<int:org_id>/<int:member_id>/', views_member.view_member, name='view_member'),   
    path('ajax_get_roles_for_organization/', views_member.ajax_get_roles_for_organization, name='ajax_get_roles_for_organization'),
    
    path('member_admin/<int:org_id>/', views_member.member_admin, name='member_admin'),
]
