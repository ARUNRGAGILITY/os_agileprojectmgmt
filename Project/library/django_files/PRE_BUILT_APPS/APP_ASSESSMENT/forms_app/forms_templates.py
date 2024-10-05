from app_assessment.forms_app.all_form_imports import *
from app_assessment.models_app.models_templates import *

class AssessmentTemplatesForm(forms.ModelForm):
    class Meta:
        model = AssessmentTemplates
        fields = ['name', 'description']
    def __init__(self, *args, **kwargs):
        super(AssessmentTemplatesForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False

class AssessmentAreasForm(forms.ModelForm):
    class Meta:
        model = AssessmentAreas
        fields = ['name', 'description']
    def __init__(self, *args, **kwargs):
        super(AssessmentAreasForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False
