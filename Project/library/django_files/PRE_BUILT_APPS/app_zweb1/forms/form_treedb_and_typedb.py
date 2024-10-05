from app_zweb1.forms.all_form_imports import *
from app_zweb1.models.models_personal_todolist import *

class TreeDBForm(forms.ModelForm):
    class Meta:
        model = TreeDB
        fields = ['name', 'description', 'done']
    def __init__(self, *args, **kwargs):
        super(TreeDBForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False


class ListItemForm(forms.ModelForm):
    class Meta:
        model = TreeDB
        fields = ['name', 'description', 'done']
    def __init__(self, *args, **kwargs):
        super(ListItemForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False