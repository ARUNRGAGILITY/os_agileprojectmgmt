from __appname__.mod_app.all_form_imports import *
from __appname__.mod___rootmodulename___type.models___rootmodulename___type import *



class __dbmodelnameprimary__TypeForm(forms.ModelForm):
    class Meta:
        model = __dbmodelnameprimary__Type
        fields = ['name', 'description']
    def __init__(self, *args, **kwargs):
        super(__dbmodelnameprimary__TypeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False

