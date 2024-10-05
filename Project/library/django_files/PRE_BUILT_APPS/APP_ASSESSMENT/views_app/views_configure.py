from app_assessment.views_app.all_view_imports import *
from app_assessment.models_app.models_asmt import *
from app_assessment.forms_app.forms_asmt import *

# configure details
from app_assessment.models_app.models_assessments import *


app_name = 'app_assessment'
app_version = 'v1'

module_name = 'configure/home'
module_title = module_name.capitalize()
module_version = ''
# ============================================================= #
@login_required
def configure_home(request, org_id):
    user = request.user
    org = Organization.objects.get(id=org_id)
    parent_page = 'loggedin_home_page'
    
    context = {
        'parent_page': f"{parent_page}",
        'page': 'configure_home',
        'org': org,
        'org_id': org_id,

        'page_title': f'Configure {module_title}',
    }
    template_file = f"{app_name}/{module_name}/configure_home.html"
    return render(request, template_file, context)