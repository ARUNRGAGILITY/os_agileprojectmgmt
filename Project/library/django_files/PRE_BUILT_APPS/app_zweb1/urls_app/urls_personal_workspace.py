from django.urls import path, include

from app_zweb1.views_zweb1 import views as zweb1_views
from app_zweb1.views_zweb1 import views_organization as zweb1_views_organization
from app_zweb1.views_zweb1 import view_blogs as zweb1_views_blogs
from app_zweb1.views_zweb1 import view_personal_kanban as zweb1_views_personal_kanban
from app_zweb1.views_zweb1 import view_personal_todolist as zweb1_views_personal_todolist
from app_zweb1.views_zweb1 import view_personal_workspace as zweb1_views_personal_workspace

urlpatterns = [
   path('personal_workspace/', zweb1_views_personal_workspace.personal_workspace, name='personal_workspace'),
   path('create_workspace/', zweb1_views_personal_workspace.create_workspace, name='create_workspace'),
   path('edit_workspace/<int:pk>/', zweb1_views_personal_workspace.edit_workspace, name='edit_workspace'),
   path('view_workspace/<int:pk>/', zweb1_views_personal_workspace.view_workspace, name='view_workspace'),
   path('delete_workspace/<int:pk>/', zweb1_views_personal_workspace.delete_workspace, name='delete_workspace'),
   path('configure_workspace/<int:pk>/', zweb1_views_personal_workspace.configure_workspace, name='configure_workspace'),
   path('copy_workspace/<int:pk>/', zweb1_views_personal_workspace.copy_workspace, name='copy_workspace'),
   
   # workspace details 
   path('view_workspace_details/<int:pk>/', zweb1_views_personal_workspace.view_workspace_details, name='view_workspace_details'),
   path('view_workspace_level/<int:pk>/', zweb1_views_personal_workspace.view_workspace_level, name='view_workspace_level'),
   
   # workspace item
   path('view_ws_item/<int:pk>/', zweb1_views_personal_workspace.view_ws_item, name='view_ws_item'),
   path('edit_ws_item/<int:pk>/', zweb1_views_personal_workspace.edit_ws_item, name='edit_ws_item'),
   path('delete_ws_item/<int:pk>/', zweb1_views_personal_workspace.delete_ws_item, name='delete_ws_item'),
   
   # view workspace tree
   path('view_workspace_tree/<int:pk>/', zweb1_views_personal_workspace.view_workspace_tree, name='view_workspace_tree'),
   
   # ajax
   path('ajax_update_wslist_done_state/', zweb1_views_personal_workspace.ajax_update_wslist_done_state, name='ajax_update_wslist_done_state'),
]
