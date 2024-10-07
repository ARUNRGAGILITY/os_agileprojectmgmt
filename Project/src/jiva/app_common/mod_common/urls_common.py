from django.urls import path, include

from app_common.mod_common import views_common

# purpose: common services for all apps
# caution: need to have imports of all models and forms from all apps

urlpatterns = [
    path('ajax_update_model_list_sorted/', views_common.ajax_update_model_list_sorted, name='ajax_update_model_list_sorted'),
    path('ajax_save_element_text/', views_common.ajax_save_element_text, name='ajax_save_element_text'),
    path('ajax_update_task_done_state/', views_common.ajax_update_task_done_state, name='ajax_update_task_done_state'),
]
