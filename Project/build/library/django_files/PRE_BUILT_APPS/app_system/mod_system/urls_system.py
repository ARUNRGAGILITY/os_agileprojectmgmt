
from django.urls import path, include


from app_system.mod_system import views_system


urlpatterns = [
    # app_automate/contents: DB/Model: Content
    path('list_systems/<int:org_id>/<int:parent_id>/', views_system.list_systems, name='list_systems'),
    path('list_deleted_systems/<int:org_id>/<int:parent_id>/', views_system.list_deleted_systems, name='list_deleted_systems'),
    path('create_system/<int:org_id>/<int:parent_id>/', views_system.create_system, name='create_system'),
    path('edit_system/<int:org_id>/<int:parent_id>/<int:content_id>/', views_system.edit_system, name='edit_system'),
    path('copy_system/<int:org_id>/<int:parent_id>/<int:content_id>/', views_system.copy_system, name='copy_system'),
    path('delete_system/<int:org_id>/<int:parent_id>/<int:content_id>/', views_system.delete_system, name='delete_system'),
    path('permanent_deletion_system/<int:org_id>/<int:parent_id>/<int:content_id>/', views_system.permanent_deletion_system, name='permanent_deletion_system'),
    path('restore_system/<int:org_id>/<int:parent_id>/<int:content_id>/', views_system.restore_system, name='restore_system'),
    path('view_system/<int:org_id>/<int:parent_id>/<int:content_id>/', views_system.view_system, name='view_system'),
    path('view_tree__system/<int:org_id>/<int:parent_id>/', views_system.view_tree__system, name='view_tree__system'),
]
