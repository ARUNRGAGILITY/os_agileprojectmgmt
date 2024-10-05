from app_assessment.models_app.all_model_imports import *
from app_xpresskanban.models.delivery_models import *

class BaseCafeImpl(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    
    active = models.BooleanField(default=True)
    position = models.PositiveIntegerField(default=1000)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    archived_at = models.DateTimeField(null=True, blank=True)
    deleted = models.BooleanField(default=False)

# first step
class AssessmentType(BaseCafeImpl):
    
    class Meta:
        verbose_name = "Assessment Type"
        verbose_name_plural = "Assessment Types"
        ordering = ['position', 'name']
        
    def __str__(self):
        return self.name + ''