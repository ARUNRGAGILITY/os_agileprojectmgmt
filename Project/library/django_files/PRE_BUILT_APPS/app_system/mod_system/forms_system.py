
from app_system.mod_app.all_form_imports import *
from app_system.mod_system.models_system import *
from app_system.mod_system_type.models_system_type import *
from app_system.mod_system_super_type.models_system_super_type import *

class SystemSuperTypeForm(forms.ModelForm):
    class Meta:
        model = SystemSuperType
        fields = ['name', 'description']
    def __init__(self, *args, **kwargs):
        super(SystemSuperTypeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False

class SystemTypeForm(forms.ModelForm):
    class Meta:
        model = SystemType
        fields = ['name', 'description']
    def __init__(self, *args, **kwargs):
        super(SystemTypeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False


class SystemForm(forms.ModelForm):
    class Meta:
        model = System
        fields = ['name', 'description']
    def __init__(self, *args, **kwargs):
        super(SystemForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False