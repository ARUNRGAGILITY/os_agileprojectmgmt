
from django.urls import path, include


from app_backlog.mod_backlog_type import views_backlog_type


urlpatterns = [
    # app_automate/content_types: DB/Model: ContentType
    path('list_backlog_types/<int:org_id>/<int:parent_id>/', views_backlog_type.list_backlog_types, name='list_backlog_types'),
    path('list_deleted_backlog_types/<int:org_id>/<int:parent_id>/', views_backlog_type.list_deleted_backlog_types, name='list_deleted_backlog_types'),
    path('create_backlog_type/<int:org_id>/<int:parent_id>/', views_backlog_type.create_backlog_type, name='create_backlog_type'),
    path('edit_backlog_type/<int:org_id>/<int:parent_id>/<int:content_type_id>/', views_backlog_type.edit_backlog_type, name='edit_backlog_type'),
    path('copy_backlog_type/<int:org_id>/<int:parent_id>/<int:content_type_id>/', views_backlog_type.copy_backlog_type, name='copy_backlog_type'),
    path('delete_backlog_type/<int:org_id>/<int:parent_id>/<int:content_type_id>/', views_backlog_type.delete_backlog_type, name='delete_backlog_type'),
    path('permanent_deletion_backlog_type/<int:org_id>/<int:parent_id>/<int:content_type_id>/', views_backlog_type.permanent_deletion_backlog_type, name='permanent_deletion_backlog_type'),
    path('restore_backlog_type/<int:org_id>/<int:parent_id>/<int:content_type_id>/', views_backlog_type.restore_backlog_type, name='restore_backlog_type'),
    path('view_backlog_type/<int:org_id>/<int:parent_id>/<int:content_type_id>/', views_backlog_type.view_backlog_type, name='view_backlog_type'),
]
