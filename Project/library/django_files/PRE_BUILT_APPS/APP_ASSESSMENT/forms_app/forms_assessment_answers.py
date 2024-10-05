from app_assessment.forms_app.all_form_imports import *
from app_assessment.models_app.models_assessment_answers import *

class AssessmentAnswersForm(forms.ModelForm):
    class Meta:
        model = AssessmentAnswers
        fields = ['name', 'description']
    def __init__(self, *args, **kwargs):
        super(AssessmentAnswersForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False

