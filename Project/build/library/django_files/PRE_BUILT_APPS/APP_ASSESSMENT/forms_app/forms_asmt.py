from app_assessment.forms_app.all_form_imports import *
from app_assessment.models_app.all_model_imports import *


class QuestionForm(forms.Form):
    QUESTION_TYPE_CHOICES = [
        ('multiple_choice', 'Multiple Choice'),
        ('text', 'Text'),
        ('yes/no', 'Yes/No'),
        ('rating', 'Rating'),
    ]
    
    question_type = forms.ChoiceField(choices=QUESTION_TYPE_CHOICES)
    question_text = forms.CharField(widget=forms.Textarea)
    answer1 = forms.CharField(label='Answer 1', required=False)
    answer2 = forms.CharField(label='Answer 2', required=False)
    answer3 = forms.CharField(label='Answer 3', required=False)
    answer4 = forms.CharField(label='Answer 4', required=False)
    answer5 = forms.CharField(label='Answer 5', required=False)
    correct_answer = forms.ChoiceField(choices=[(i, f"Answer {i}") for i in range(1, 6)])

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        # Dynamically adjust the correct_answer choices based on the provided answers
        self.fields['correct_answer'].choices = [
            (i, f"Answer {i}") for i in range(1, 6) if kwargs['initial'].get(f'answer{i}')
        ]
