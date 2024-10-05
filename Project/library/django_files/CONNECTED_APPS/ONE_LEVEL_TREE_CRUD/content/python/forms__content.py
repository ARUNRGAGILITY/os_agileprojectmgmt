
from __appname__.mod_app.all_form_imports import *
from __appname__.mod___singularmodname__.models___singularmodname__ import *
from __appname__.mod___rootmodulename___type.models___rootmodulename___type import *
from __appname__.mod___rootmodulename___super_type.models___rootmodulename___super_type import *

class __dbmodelnameprimary__SuperTypeForm(forms.ModelForm):
    class Meta:
        model = __dbmodelnameprimary__SuperType
        fields = ['name', 'description']
    def __init__(self, *args, **kwargs):
        super(__dbmodelnameprimary__SuperTypeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False

class __dbmodelnameprimary__TypeForm(forms.ModelForm):
    class Meta:
        model = __dbmodelnameprimary__Type
        fields = ['name', 'description']
    def __init__(self, *args, **kwargs):
        super(__dbmodelnameprimary__TypeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False


class __dbmodelnameprimary__Form(forms.ModelForm):
    class Meta:
        model = __dbmodelnameprimary__
        fields = ['name', 'description']
    def __init__(self, *args, **kwargs):
        super(__dbmodelnameprimary__Form, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False