
from app_memberprofilerole.mod_app.all_form_imports import *
from app_memberprofilerole.mod_role.models_role import *

class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['name', 'description']
    def __init__(self, *args, **kwargs):
        super(RoleForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False

