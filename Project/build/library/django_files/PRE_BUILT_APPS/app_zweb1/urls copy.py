from django.urls import path

from app_zweb1.views_zweb1 import views as zweb1_views
from app_zweb1.views_zweb1 import views_organization as zweb1_views_organization
from app_zweb1.views_zweb1 import view_blogs as zweb1_views_blogs
from app_zweb1.views_zweb1 import view_personal_kanban as zweb1_views_personal_kanban
from app_zweb1.views_zweb1 import view_personal_todolist as zweb1_views_personal_todolist
urlpatterns = [
    # all users will come to this visitor page
    path('', zweb1_views.general_home_page, name="general_home_page"),
    
    path('get_started/', zweb1_views.get_started, name="get_started"),
    path('at_login/', zweb1_views.at_login, name="at_login"),
    path('at_register/', zweb1_views.at_register, name="at_register"),
    path('features/', zweb1_views.features, name="features"),
    path('at_logout/', zweb1_views.at_logout, name="at_logout"),
    path('loggedin_home_page/', zweb1_views.loggedin_home_page, name="loggedin_home_page"),
    path('learn/', zweb1_views.learn, name="learn"),
    path('blogs/', zweb1_views.blogs, name="blogs"),
    path('FAQs/', zweb1_views.FAQs, name="FAQs"),
    path('contact_support/', zweb1_views.contact_support, name="contact_support"),
    path('about/', zweb1_views.about, name="about"),
    path('provide_feedback/', zweb1_views.provide_feedback, name="provide_feedback"),
    path('consult_feature/<str:feature>/', zweb1_views.consult_feature, name="consult_feature"),
    # blogs
    path('blog_details/', zweb1_views_blogs.blog_details, name="blog_details"),
    # organization
    path('organization_list/', zweb1_views_organization.organization_list, name="organization_list"),
    # personal kanban
    path('generate_cfd/<int:board_id>/', zweb1_views_personal_kanban.generate_cfd, name="generate_cfd"),
    path('personal_kanban/', zweb1_views_personal_kanban.personal_kanban, name="personal_kanban"),
    path('view_kanban_board/<int:pk>/', zweb1_views_personal_kanban.view_kanban_board, name="view_kanban_board"),
    path('create_kanban_board/', zweb1_views_personal_kanban.create_kanban_board, name="create_kanban_board"),
    path('edit_kanban_board/<int:pk>/', zweb1_views_personal_kanban.edit_kanban_board, name="edit_kanban_board"),
    path('delete_kanban_board/<int:pk>/', zweb1_views_personal_kanban.delete_kanban_board, name="delete_kanban_board"),
    path('visualize_kanban_workflow/<int:pk>/', zweb1_views_personal_kanban.visualize_kanban_workflow, name="visualize_kanban_workflow"),
    # Board State
    path('board_states/<int:board_id>/', zweb1_views_personal_kanban.board_states, name="board_states"),
    path('view_board_state/<int:board_id>/<int:pk>/', zweb1_views_personal_kanban.view_board_state, name="view_board_state"),
    path('create_board_state/<int:board_id>/', zweb1_views_personal_kanban.create_board_state, name="create_board_state"), 
    path('edit_board_state/<int:board_id>/<int:pk>/', zweb1_views_personal_kanban.edit_board_state, name="edit_board_state"),
    path('delete_board_state/<int:board_id>/<int:pk>/', zweb1_views_personal_kanban.delete_board_state, name="delete_board_state"),
    
    # Card
    path('view_card/<int:pk>/', zweb1_views_personal_kanban.view_card, name="view_card"),
    path('edit_card/<int:pk>/', zweb1_views_personal_kanban.edit_card, name="edit_card"),
    path('delete_card/<int:pk>/', zweb1_views_personal_kanban.delete_card, name="delete_card"),
    # AJAX
    path('ajax_update_model_list_sorted/', zweb1_views_personal_kanban.ajax_update_model_list_sorted, name='ajax_update_model_list_sorted'),
    path('ajax_update_kanban_board_state/', zweb1_views_personal_kanban.ajax_update_kanban_board_state, name='ajax_update_kanban_board_state'),
    
    # Configuration of Kanban Boards & other settings
    path('configure_kanban_board/<int:pk>/', zweb1_views_personal_kanban.configure_kanban_board, name='configure_kanban_board'),
    
    
    ## Personal Todo List
    path('personal_todolist/', zweb1_views_personal_todolist.personal_todolist, name="personal_todolist"),
    path('create_todolist_topic/', zweb1_views_personal_todolist.create_todolist_topic, name="create_todolist_topic"),
    path('edit_todolist_topic/<int:pk>/', zweb1_views_personal_todolist.edit_todolist_topic, name="edit_todolist_topic"),
    path('view_todolist_topic/<int:pk>/', zweb1_views_personal_todolist.view_todolist_topic, name="view_todolist_topic"),
    path('delete_todolist_topic/<int:pk>/', zweb1_views_personal_todolist.delete_todolist_topic, name="delete_todolist_topic"),
    path('configure_todolist_topic/<int:pk>/', zweb1_views_personal_todolist.configure_todolist_topic, name="configure_todolist_topic"),
    path('view_todolist/<int:pk>/', zweb1_views_personal_todolist.view_todolist, name="view_todolist"),
    path('copy_todolist_topic/<int:pk>/', zweb1_views_personal_todolist.copy_todolist_topic, name="copy_todolist_topic"),
    # todo list item
    # item
    path('view_list_item/<int:pk>/', zweb1_views_personal_todolist.view_list_item, name="view_list_item"),
    path('edit_list_item/<int:pk>/', zweb1_views_personal_todolist.edit_list_item, name="edit_list_item"),
    path('delete_list_item/<int:pk>/', zweb1_views_personal_todolist.delete_list_item, name="delete_list_item"),
    
    # templates
    path('create_todolist_templates/', zweb1_views_personal_todolist.create_todolist_templates, name="create_todolist_templates"),
    path('create_template/', zweb1_views_personal_todolist.create_template, name="create_template"),
    path('edit_template/<int:pk>/', zweb1_views_personal_todolist.edit_template, name="edit_template"),
    path('delete_template/<int:pk>/', zweb1_views_personal_todolist.delete_template, name="delete_template"),
    path('view_template/<int:pk>/', zweb1_views_personal_todolist.view_template, name="view_template"),
    path('copy_template/<int:pk>/', zweb1_views_personal_todolist.copy_template, name="copy_template"),
    # ajax todolist
    path('ajax_update_todolist_done_state/', zweb1_views_personal_todolist.ajax_update_todolist_done_state, name='ajax_update_todolist_done_state'),
    
]

