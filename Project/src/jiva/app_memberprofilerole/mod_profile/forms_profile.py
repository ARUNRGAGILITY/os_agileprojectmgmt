
from app_memberprofilerole.mod_app.all_form_imports import *
from app_memberprofilerole.mod_profile.models_profile import *

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'description']
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False
#############################################################################
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        
            
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'bio']
        
#############################################################################