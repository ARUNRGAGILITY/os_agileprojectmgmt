
from django.urls import path, include


from app_system.mod_system_type import views_system_type


urlpatterns = [
    # app_automate/content_types: DB/Model: ContentType
    path('list_system_types/<int:org_id>/<int:parent_id>/', views_system_type.list_system_types, name='list_system_types'),
    path('list_deleted_system_types/<int:org_id>/<int:parent_id>/', views_system_type.list_deleted_system_types, name='list_deleted_system_types'),
    path('create_system_type/<int:org_id>/<int:parent_id>/', views_system_type.create_system_type, name='create_system_type'),
    path('edit_system_type/<int:org_id>/<int:parent_id>/<int:content_type_id>/', views_system_type.edit_system_type, name='edit_system_type'),
    path('copy_system_type/<int:org_id>/<int:parent_id>/<int:content_type_id>/', views_system_type.copy_system_type, name='copy_system_type'),
    path('delete_system_type/<int:org_id>/<int:parent_id>/<int:content_type_id>/', views_system_type.delete_system_type, name='delete_system_type'),
    path('permanent_deletion_system_type/<int:org_id>/<int:parent_id>/<int:content_type_id>/', views_system_type.permanent_deletion_system_type, name='permanent_deletion_system_type'),
    path('restore_system_type/<int:org_id>/<int:parent_id>/<int:content_type_id>/', views_system_type.restore_system_type, name='restore_system_type'),
    path('view_system_type/<int:org_id>/<int:parent_id>/<int:content_type_id>/', views_system_type.view_system_type, name='view_system_type'),
]
