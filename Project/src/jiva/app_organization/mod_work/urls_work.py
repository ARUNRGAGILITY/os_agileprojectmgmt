
from django.urls import path, include

from app_organization.mod_work import views_work


urlpatterns = [
    # app_organization/works: DB/Model: Work
    path('list_works/<int:pro_id>/', views_work.list_works, name='list_works'),
    path('list_deleted_works/<int:pro_id>/', views_work.list_deleted_works, name='list_deleted_works'),
    path('create_work/<int:pro_id>/', views_work.create_work, name='create_work'),
    path('edit_work/<int:pro_id>/<int:work_id>/', views_work.edit_work, name='edit_work'),
    path('delete_work/<int:pro_id>/<int:work_id>/', views_work.delete_work, name='delete_work'),
    path('permanent_deletion_work/<int:pro_id>/<int:work_id>/', views_work.permanent_deletion_work, name='permanent_deletion_work'),
    path('restore_work/<int:pro_id>/<int:work_id>/', views_work.restore_work, name='restore_work'),
    path('view_work/<int:pro_id>/<int:work_id>/', views_work.view_work, name='view_work'),
]
