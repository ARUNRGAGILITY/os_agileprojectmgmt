from app_zweb1.views_zweb1.view_imports import *
from app_zweb1.models.models_personal_todolist import *
from app_zweb1.forms.form_personal_todolist import *
from app_zweb1.forms.form_treedb_and_typedb import *
from app_zweb1.models.models_treedb_and_typedb import *

app_name = 'app_zweb1'
app_version = 'v1'

@login_required
def basic_drawing(request):
    user = request.user
    # send outputs (info, template,
    context = {
        'parent_page': 'loggedin_home_page',
        'page': 'basic_drawing',
        'user': user,

        'page_title': f'Basic Drawing',
    }       
    template_file = f"{app_name}/platform/drawing/basic/basic_drawing.html"
    return render(request, template_file, context)
