
from django.urls import path, include

from app_memberprofilerole.mod_regcode import views_regcode


urlpatterns = [
    # app_memberprofilerole/regcodes: DB/Model: Regcode
    path('list_regcodes/<int:org_id>/', views_regcode.list_regcodes, name='list_regcodes'),
    path('list_deleted_regcodes/<int:org_id>/', views_regcode.list_deleted_regcodes, name='list_deleted_regcodes'),
    path('create_regcode/<int:org_id>/', views_regcode.create_regcode, name='create_regcode'),
    path('edit_regcode/<int:org_id>/<int:regcode_id>/', views_regcode.edit_regcode, name='edit_regcode'),
    path('delete_regcode/<int:org_id>/<int:regcode_id>/', views_regcode.delete_regcode, name='delete_regcode'),
    path('permanent_deletion_regcode/<int:org_id>/<int:regcode_id>/', views_regcode.permanent_deletion_regcode, name='permanent_deletion_regcode'),
    path('restore_regcode/<int:org_id>/<int:regcode_id>/', views_regcode.restore_regcode, name='restore_regcode'),
    path('view_regcode/<int:org_id>/<int:regcode_id>/', views_regcode.view_regcode, name='view_regcode'),
]
