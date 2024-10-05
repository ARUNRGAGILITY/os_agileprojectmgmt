from app_web.mod_app.all_view_imports import *
from app_memberprofilerole.mod_app.all_model_imports import *
from app_memberprofilerole.mod_member.models_member import *

from app_jivapms.mod_app.all_view_imports import *

app_name = "app_jivapms"
version = "v1"
module_dirname = "mod_web"

from app_jivapms.mod_web.helper_web import *

# View for Site Administration Content (AJAX)
def ajax_super_user_orgcrudlsp(request):
    context = {
        'parent_page': 'super_user',
        'page': 'org_crud',
        'page_title': 'Org Page',
    }
    template_url = f"{app_name}/{module_dirname}/super_user/ajax_web/org_crudlsp.html"
    return render(request, template_url, context) 

# View for Dashboard Content (AJAX)
def ajax_dashboard(request):
    return render(request, 'partials/dashboard.html')

# View for Settings Content (AJAX)
def ajax_settings(request):
    return render(request, 'partials/settings.html')
