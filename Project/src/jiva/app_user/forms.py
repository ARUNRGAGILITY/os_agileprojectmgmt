from app_web.imports.all_form_imports import *
from app_user.models import *

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    RegistrationCode = forms.CharField(required=True)
    #groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'RegistrationCode']
        widgets = {
            'username': forms.TextInput(attrs={'autocomplete': 'off'}),
            # Other form field widgets
            'password1': forms.TextInput(attrs={'autocomplete': 'off'}),
        }

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    groups = forms.ModelMultipleChoiceField(queryset=CustomGroup.objects.filter(active=True), widget=forms.CheckboxSelectMultiple, required=False)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Pre-select groups that the user is part of
        if self.instance.pk:
            self.fields['groups'].initial = self.instance.groups.all()

            
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'bio']


class GroupForm(forms.ModelForm):
    class Meta:
        model = CustomGroup
        fields = ['name']