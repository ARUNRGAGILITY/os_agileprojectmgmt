
from django.urls import path, include


from app_system.mod_system_super_type import views_system_super_type

urlpatterns = [
    # app_automate/super_types: DB/Model: SuperType
    path('list_system_super_types/<int:org_id>/', views_system_super_type.list_system_super_types, name='list_system_super_types'),
    path('list_deleted_system_super_types/<int:org_id>/', views_system_super_type.list_deleted_system_super_types, name='list_deleted_system_super_types'),
    path('create_system_super_type/<int:org_id>/', views_system_super_type.create_system_super_type, name='create_system_super_type'),
    path('edit_system_super_type/<int:org_id>/<int:super_type_id>/', views_system_super_type.edit_system_super_type, name='edit_system_super_type'),
    path('delete_system_super_type/<int:org_id>/<int:super_type_id>/', views_system_super_type.delete_system_super_type, name='delete_system_super_type'),
    path('permanent_deletion_system_super_type/<int:org_id>/<int:super_type_id>/', views_system_super_type.permanent_deletion_system_super_type, name='permanent_deletion_system_super_type'),
    path('restore_system_super_type/<int:org_id>/<int:super_type_id>/', views_system_super_type.restore_system_super_type, name='restore_system_super_type'),
    path('view_system_super_type/<int:org_id>/<int:super_type_id>/', views_system_super_type.view_system_super_type, name='view_system_super_type'),
]
