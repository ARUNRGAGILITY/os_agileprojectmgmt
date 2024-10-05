
from app_memberprofilerole.mod_app.all_form_imports import *
from app_memberprofilerole.mod_regcode.models_regcode import *

class RegcodeForm(forms.ModelForm):
    class Meta:
        model = Regcode
        fields = ['name', 'description']
    def __init__(self, *args, **kwargs):
        super(RegcodeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False

