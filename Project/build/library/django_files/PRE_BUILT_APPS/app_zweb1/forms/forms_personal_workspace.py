from app_zweb1.forms.all_form_imports import *
from app_zweb1.models.models_personal_workspace import *

class WorkspaceForm(forms.ModelForm):
    class Meta:
        model = Workspace
        fields = ['name', 'description', 'template', 'done']
    def __init__(self, *args, **kwargs):
        super(WorkspaceForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False


