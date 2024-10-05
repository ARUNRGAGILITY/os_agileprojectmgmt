from app_zweb1.models.models_imports import *

# TypeDB Type
class TypeDBType(models.Model):
    name = models.CharField(max_length=250, default='', null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    
    active = models.BooleanField(default=True, null=True, blank=True)
    deleted = models.BooleanField(default=False, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.name}"

# Core Models
class TypeDB(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, 
                            related_name='typedb', on_delete=models.CASCADE)
    name =  models.CharField(max_length=256, unique=False)
    description = models.TextField(null=True, blank=True, default='')
    
    # accounting
    position = models.PositiveIntegerField(default=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True, null=True, blank=True)
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
                               blank=True, related_name='author_typedb')
    deleted = models.BooleanField(default=False, null=True, blank=True)
    type_type = models.ForeignKey(TypeDBType, on_delete=models.CASCADE, 
                                  null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="user_typedb")
    class MPTTMeta:
        order_insertion_by = ['position']

    def __str__(self):
        return self.name
   
    def get_active_descendants(self):
        return self.get_descendants().filter(active=True)
    
    def get_parent_id(self):
        if self.parent:
            return self.parent.id
        return None

    ## display 
    def children(self):
        return TypeDB.objects.filter(parent=self.pk, active=True)
    
    def serializable_object(self):
        obj = {'name': self.name, 'children': []}
        for child in self.children():
            obj['children'].append(child.serializable_object())
        return obj


# Core Hierarchical System Database
class TreeDB(MPTTModel):
  
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    name =  models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True, default='')
    
    type = TreeForeignKey(TypeDB, null=True, blank=True, related_name='tree_type', on_delete=models.CASCADE)
    
    done = models.BooleanField(default=False)
    position = models.PositiveIntegerField(default=1000)
    
    # for now label is a char field
    tag =  models.CharField(max_length=256,null=True, blank=True, default='')
    blocked =  models.CharField(max_length=256,null=True, blank=True, default='')
    block_count = models.PositiveIntegerField(default=0)

    
    approved = models.BooleanField(default=False, null=True, blank=True)
    
    # time related
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    duration_in_hours = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    
    active = models.BooleanField(default=True, null=True, blank=True)
    deleted = models.BooleanField(default=False, null=True, blank=True)

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
                               blank=True, related_name='author_treedb')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                             related_name='user_treedb')
   
    class MPTTMeta:
        order_insertion_by = ['position']

    def __str__(self):
        return self.name

    def get_completion_stats(self):
        total_count = self.get_descendants().filter(done=True, active=True).count() + self.get_descendants().filter(done=False, active=True).count()
        completed_count = self.get_descendants().filter(done=True, active=True).count()
        percent_complete = round((completed_count / total_count) * 100, 2) if total_count > 0 else 0.0
        #print(f"====> {completed_count}/{total_count} ===> {percent_complete}")
        return {
            'total_count': total_count,
            'completed_count': completed_count,
            'percent_complete': percent_complete,
        }
    
    def get_active_descendants(self):
        return self.get_descendants().filter(active=True)

    #
    # DEF BLOCK UNBLOCK
    #
    def block(self):
        self.blocked = "blocked"
        self.block_count += 1

    def unblock(self):
        self.blocked = "unblocked"

    ## display 
    def children(self):
        return TreeDB.objects.filter(parent=self.pk, active=True)
    
    def serializable_object(self):
        obj = {'name': self.name, 'children': []}
        for child in self.children():
            obj['children'].append(child.serializable_object())
        return obj
    
    def get_active_children(self):
        return self.get_children().filter(active=True)