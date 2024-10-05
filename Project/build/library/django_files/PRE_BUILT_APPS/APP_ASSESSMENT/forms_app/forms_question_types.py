from app_assessment.forms_app.all_form_imports import *
from app_assessment.models_app.models_question_types import *

class AssessmentQuestionTypesForm(forms.ModelForm):
    class Meta:
        model = AssessmentQuestionTypes
        fields = ['name', 'description']
    def __init__(self, *args, **kwargs):
        super(AssessmentQuestionTypesForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False

