from app_assessment.forms_app.all_form_imports import *
from app_assessment.models_app.models_template_types import *

class AssessmentTemplateTypesForm(forms.ModelForm):
    class Meta:
        model = AssessmentTemplateTypes
        fields = ['name', 'description']
    def __init__(self, *args, **kwargs):
        super(AssessmentTemplateTypesForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False