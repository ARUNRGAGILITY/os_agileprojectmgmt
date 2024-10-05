from app_zweb1.forms.all_form_imports import *
from app_zweb1.models.models_personal_kanban import *

class KanbanBoardForm(forms.ModelForm):
    class Meta:
        model = KanbanBoard
        fields = ['name', 'description',]
    def __init__(self, *args, **kwargs):
        super(KanbanBoardForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False

class BoardStateForm(forms.ModelForm):
    class Meta:
        model = BoardState
        fields = ['name', 'description', 'wip_limit', 'done_column', 'exclude_wip_limit']
    def __init__(self, *args, **kwargs):
        super(BoardStateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['name', 'description', 'priority']
    def __init__(self, *args, **kwargs):
        super(CardForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False
