from app_zweb1.models.models_imports import *
from app_zweb1.models.models_treedb_and_typedb import *

class Workspace(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    
    active = models.BooleanField(default=True)
    position = models.PositiveIntegerField(default=1000)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    approved = models.BooleanField(default=False)
    shared = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    
    done = models.BooleanField(default=False)
    
    template = models.BooleanField(default=False)
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_workspaces")
    
    def __str__(self):
        return self.name
    
class WorkspaceMap(models.Model):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, 
                              related_name="ws_map")
    treedb = models.ForeignKey(TreeDB, on_delete=models.CASCADE,    
                              related_name="tree_ws_map")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_ws_maps")
    ws_theme = models.CharField(max_length=100, default="default")
    
    def __str__(self):
        return self.workspace.name