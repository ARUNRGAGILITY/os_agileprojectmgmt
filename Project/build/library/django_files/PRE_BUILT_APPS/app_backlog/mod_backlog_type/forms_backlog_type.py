from app_backlog.mod_app.all_form_imports import *
from app_backlog.mod_backlog_type.models_backlog_type import *



class BacklogTypeForm(forms.ModelForm):
    class Meta:
        model = BacklogType
        fields = ['name', 'description']
    def __init__(self, *args, **kwargs):
        super(BacklogTypeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False

