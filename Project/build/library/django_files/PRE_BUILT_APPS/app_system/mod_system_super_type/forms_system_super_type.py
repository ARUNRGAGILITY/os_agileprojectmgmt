
from app_system.mod_app.all_form_imports import *
from app_system.mod_system_super_type.models_system_super_type import *

class SystemSuperTypeForm(forms.ModelForm):
    class Meta:
        model = SystemSuperType
        fields = ['name', 'description']
    def __init__(self, *args, **kwargs):
        super(SystemSuperTypeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False
