from app_assessment.forms_app.all_form_imports import *
from app_assessment.models_app.models_assessment_questions import *
from app_assessment.models_app.models_question_types import *

class AssessmentQuestionsForm(forms.ModelForm):
    class Meta:
        model = AssessmentQuestions
        fields = ['question_type', 'text', 'description', 'instructions' ]
        widgets = {
            'text': forms.Textarea(attrs={'class': 'custom-css-class', 'rows': 3, 'cols': 40}),
            'instructions': forms.Textarea(attrs={'class': 'custom-css-class', 'rows': 2, 'cols': 40}),
        }

    def __init__(self, *args, **kwargs):
        super(AssessmentQuestionsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False
        
        # question type order by position and filter active
        self.fields['question_type'].queryset = AssessmentQuestionTypes.objects.filter(active=True).order_by('position')
