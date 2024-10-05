from django.urls import path, include

from app_zweb1.views_zweb1 import views as zweb1_views
from app_zweb1.views_zweb1 import views_organization as zweb1_views_organization
from app_zweb1.views_zweb1 import view_blogs as zweb1_views_blogs
from app_zweb1.views_zweb1 import view_personal_kanban as zweb1_views_personal_kanban
from app_zweb1.views_zweb1 import view_personal_todolist as zweb1_views_personal_todolist
from app_zweb1.views_zweb1 import view_personal_workspace as zweb1_views_personal_workspace
from app_zweb1.views_zweb1 import view_basic_drawing as zweb1_views_basic_drawing
urlpatterns = [
    path('basic_drawing/', zweb1_views_basic_drawing.basic_drawing, name='basic_drawing'),
]