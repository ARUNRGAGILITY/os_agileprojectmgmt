
from app_memberprofilerole.mod_app.all_form_imports import *
from app_memberprofilerole.mod_member.models_member import *
from app_organization.mod_organization.models_organization import *
from app_memberprofilerole.mod_role.models_role import *

class MemberForm(forms.ModelForm):
   
    class Meta:
        model = Member
        fields = ['user']
       
    def __init__(self, *args, **kwargs):
        super(MemberForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False
        
class MemberOrganizationRoleForm(forms.ModelForm):
    role = forms.ModelMultipleChoiceField(
        queryset=Role.objects.none(),
        widget=CheckboxSelectMultiple
    )
    class Meta:
        model = MemberOrganizationRole
        fields = ['org', 'role']
        widgets = {
            'role': CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        org_id = kwargs.pop('org_id', None)
        super(MemberOrganizationRoleForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = True

        # if 'org' in self.data:
        #     try:
        #         org_id = int(self.data.get('org'))
        #         self.fields['role'].queryset = Role.objects.filter(org_id=org_id)
        #     except (ValueError, TypeError):
        #         self.fields['role'].queryset = Role.objects.none()
        # elif self.instance.pk:
        #     self.fields['role'].queryset = self.instance.org.roles.filter(active=True)
        # else:
        #     self.fields['role'].queryset = Role.objects.none()
        
        # if org_id:
        #     self.fields['role'].queryset = Role.objects.filter(org_id=org_id)
        # elif self.instance.pk:
        #     self.fields['role'].queryset = self.instance.org.roles.filter(active=True)
        # else:
        #     self.fields['role'].queryset = Role.objects.none()
        
        ## Creating organization members and assinging organization roles
        if org_id:
            self.fields['role'].queryset = Role.objects.filter(org_id=org_id)