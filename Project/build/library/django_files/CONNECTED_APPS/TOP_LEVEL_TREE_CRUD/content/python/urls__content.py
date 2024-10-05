
from django.urls import path, include

from __appname__.mod___singularmodname__ import views___singularmodname__


urlpatterns = [
    # app_automate/contents: DB/Model: Content
    path('list___pluralmodname__/<int:parent_id>/', views___singularmodname__.list___pluralmodname__, name='list___pluralmodname__'),
    path('list_deleted___pluralmodname__/<int:parent_id>/', views___singularmodname__.list_deleted___pluralmodname__, name='list_deleted___pluralmodname__'),
    path('create___singularmodname__/<int:parent_id>/', views___singularmodname__.create___singularmodname__, name='create___singularmodname__'),
    path('edit___singularmodname__/<int:parent_id>/<int:content_id>/', views___singularmodname__.edit___singularmodname__, name='edit___singularmodname__'),
    path('delete___singularmodname__/<int:parent_id>/<int:content_id>/', views___singularmodname__.delete___singularmodname__, name='delete___singularmodname__'),
    path('permanent_deletion___singularmodname__/<int:parent_id>/<int:content_id>/', views___singularmodname__.permanent_deletion___singularmodname__, name='permanent_deletion___singularmodname__'),
    path('restore___singularmodname__/<int:parent_id>/<int:content_id>/', views___singularmodname__.restore___singularmodname__, name='restore___singularmodname__'),
    path('view___singularmodname__/<int:parent_id>/<int:content_id>/', views___singularmodname__.view___singularmodname__, name='view___singularmodname__'),
]
