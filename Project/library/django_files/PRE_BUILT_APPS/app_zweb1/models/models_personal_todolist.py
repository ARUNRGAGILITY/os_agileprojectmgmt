from app_zweb1.models.models_imports import *
from app_zweb1.models.models_treedb_and_typedb import *

class TodoListTopic(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    
    active = models.BooleanField(default=True)
    position = models.PositiveIntegerField(default=1000)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    approved = models.BooleanField(default=False)
    shared = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    
    done = models.BooleanField(default=False)
    
    template = models.BooleanField(default=False)
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_todolist_topics")
    
    def __str__(self):
        return self.name
    

class TopicTodoListMap(models.Model):
    topic = models.ForeignKey(TodoListTopic, on_delete=models.CASCADE, 
                              related_name="topic_todolist_map")
    treedb = models.ForeignKey(TreeDB, on_delete=models.CASCADE,    
                              related_name="treedb_todolist_map")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_topic_todolist_maps")
    todolist_theme = models.CharField(max_length=100, default="default")
    
    def __str__(self):
        return self.topic.name