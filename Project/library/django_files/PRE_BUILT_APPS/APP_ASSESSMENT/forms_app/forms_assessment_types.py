from app_assessment.forms_app.all_form_imports import *
from app_assessment.models_app.models_assessment_types import *

class AssessmentTypesForm(forms.ModelForm):
    class Meta:
        model = AssessmentTypes
        fields = ['name', 'description']
    def __init__(self, *args, **kwargs):
        super(AssessmentTypesForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False

