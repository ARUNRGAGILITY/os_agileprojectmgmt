
from django.urls import path, include


from app_backlog.mod_backlog_super_type import views_backlog_super_type

urlpatterns = [
    # app_automate/super_types: DB/Model: SuperType
    path('list_backlog_super_types/<int:org_id>/', views_backlog_super_type.list_backlog_super_types, name='list_backlog_super_types'),
    path('list_deleted_backlog_super_types/<int:org_id>/', views_backlog_super_type.list_deleted_backlog_super_types, name='list_deleted_backlog_super_types'),
    path('create_backlog_super_type/<int:org_id>/', views_backlog_super_type.create_backlog_super_type, name='create_backlog_super_type'),
    path('edit_backlog_super_type/<int:org_id>/<int:stype_id>/', views_backlog_super_type.edit_backlog_super_type, name='edit_backlog_super_type'),
    path('delete_backlog_super_type/<int:org_id>/<int:stype_id>/', views_backlog_super_type.delete_backlog_super_type, name='delete_backlog_super_type'),
    path('permanent_deletion_backlog_super_type/<int:org_id>/<int:stype_id>/', views_backlog_super_type.permanent_deletion_backlog_super_type, name='permanent_deletion_backlog_super_type'),
    path('restore_backlog_super_type/<int:org_id>/<int:stype_id>/', views_backlog_super_type.restore_backlog_super_type, name='restore_backlog_super_type'),
    path('view_backlog_super_type/<int:org_id>/<int:stype_id>/', views_backlog_super_type.view_backlog_super_type, name='view_backlog_super_type'),
]
