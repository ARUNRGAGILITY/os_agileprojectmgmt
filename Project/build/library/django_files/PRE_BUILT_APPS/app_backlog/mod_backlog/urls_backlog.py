
from django.urls import path, include


from app_backlog.mod_backlog import views_backlog


urlpatterns = [
    # app_automate/contents: DB/Model: Content
    path('list_backlogs/<int:org_id>/<int:parent_id>/', views_backlog.list_backlogs, name='list_backlogs'),
    path('list_deleted_backlogs/<int:org_id>/<int:parent_id>/', views_backlog.list_deleted_backlogs, name='list_deleted_backlogs'),
    path('create_backlog/<int:org_id>/<int:parent_id>/', views_backlog.create_backlog, name='create_backlog'),
    path('edit_backlog/<int:org_id>/<int:parent_id>/<int:content_id>/', views_backlog.edit_backlog, name='edit_backlog'),
    path('copy_backlog/<int:org_id>/<int:parent_id>/<int:content_id>/', views_backlog.copy_backlog, name='copy_backlog'),
    path('delete_backlog/<int:org_id>/<int:parent_id>/<int:content_id>/', views_backlog.delete_backlog, name='delete_backlog'),
    path('permanent_deletion_backlog/<int:org_id>/<int:parent_id>/<int:content_id>/', views_backlog.permanent_deletion_backlog, name='permanent_deletion_backlog'),
    path('restore_backlog/<int:org_id>/<int:parent_id>/<int:content_id>/', views_backlog.restore_backlog, name='restore_backlog'),
    path('view_backlog/<int:org_id>/<int:parent_id>/<int:content_id>/', views_backlog.view_backlog, name='view_backlog'),
    path('view_tree__backlog/<int:org_id>/<int:parent_id>/', views_backlog.view_tree__backlog, name='view_tree__backlog'),
]
