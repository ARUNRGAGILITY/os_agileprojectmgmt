from django.contrib import admin
from app_zweb1.models.models_personal_kanban import *
from app_zweb1.models.models_treedb_and_typedb import *
from app_zweb1.models.models_personal_todolist import *
from app_zweb1.models.models_personal_workspace import *


class KanbanBoardAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'active', 'position', 'created_at', 'updated_at', 'completed_at')
    list_filter = ('active', 'created_at')
    search_fields = ('name', 'description')

class BoardStateAdmin(admin.ModelAdmin):
    list_display = ('id', 'position', 'board',  'name', 'description', 'active')
    list_filter = ('active', 'board')
    search_fields = ('board__name', )

class CardAdmin(admin.ModelAdmin):
    list_display = ('name', 'priority', 'board', 'state',  'created_at', 'updated_at', 'active')
    list_filter = ('active', 'board', 'state',)
    search_fields = ('name', 'description')

class CardStateRecordAdmin(admin.ModelAdmin):
    list_display = ('card', 'state', 'start_timestamp', 'end_timestamp')
    list_filter = ('state',)
    search_fields = ('card__name',)


class CardStateCountAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'vstate', 'vcount')


class TreeDBAdmin(admin.ModelAdmin):
    list_display = ('id', 'parent', 'name', 'description', 'done')

class TodoListTopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'done')
    
class TopicTodoListMapAdmin(admin.ModelAdmin):
    list_display = ('id', 'topic', 'treedb', 'todolist_theme')
    
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'done')
    
class WorkspaceMapAdmin(admin.ModelAdmin):
    list_display = ('id', 'workspace', 'treedb', 'ws_theme')
    


admin.site.register(Workspace, WorkspaceAdmin)
admin.site.register(WorkspaceMap, WorkspaceMapAdmin)

admin.site.register(TopicTodoListMap, TopicTodoListMapAdmin)
admin.site.register(TodoListTopic, TodoListTopicAdmin)
admin.site.register(TreeDB, TreeDBAdmin)

admin.site.register(KanbanBoard, KanbanBoardAdmin)
admin.site.register(BoardState, BoardStateAdmin)
admin.site.register(Card, CardAdmin)
admin.site.register(CardStateRecord, CardStateRecordAdmin)
admin.site.register(CardStateCount, CardStateCountAdmin)
