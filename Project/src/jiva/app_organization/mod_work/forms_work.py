
from app_organization.mod_app.all_form_imports import *
from app_organization.mod_work.models_work import *

class WorkForm(forms.ModelForm):
    class Meta:
        model = Work
        fields = ['name', 'description']
    def __init__(self, *args, **kwargs):
        super(WorkForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False

