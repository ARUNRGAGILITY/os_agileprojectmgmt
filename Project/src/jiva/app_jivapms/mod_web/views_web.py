from app_web.mod_app.all_view_imports import *
from app_memberprofilerole.mod_app.all_model_imports import *
from app_memberprofilerole.mod_member.models_member import *

from app_jivapms.mod_app.all_view_imports import *

app_name = "app_jivapms"
version = "v1"
module_dirname = "mod_web"

from app_jivapms.mod_web.helper_web import *
from app_jivapms.mod_web.views_ajax_web import *
# Create your views here.
def index(request):
    user = request.user
    context = {
        'parent_page': 'home',
        'page': 'index',
        'page_title': 'Home Page',
        'user': user,
        'roles': [],
        'member': None,
        'super_user': False,
        'multiple_roles': False,
        'no_of_roles': 0,
        'user_roles_data': [],
        'anonymous': False,
    }

    if user.is_authenticated:
        logger.debug(f"User authenticated: {user.id}")
        if user.is_superuser:
            context['super_user'] = True
            context['role'] = COMMON_ROLE_CONFIG["SUPER_USER"]["name"]
        else:
            try:
                member = Member.objects.prefetch_related('member_roles__role', 'member_roles__org').get(user=user)
                roles = member.member_roles.filter(active=True)

                # Prepare user role data
                user_data = {
                    'member_id': member.id,
                    'username': member.user.username if member.user else 'Unknown User',
                    'roles': []
                }

                for role in roles:
                    role_data = {
                        'org_id': role.org.id if role.org else None,
                        'role_id': role.role.id if role.role else None,
                        'role_name': role.role.name if role.role else 'No Role',
                        'org_name': role.org.name if role.org else 'No Org',
                        'lc_role_name': role.role.name.lower().replace(' ', '_') if role.role else 'no page',
                    }
                    # Append the role data to user_data['roles']
                    user_data['roles'].append(role_data)

                # Add user_data to the context
                context['user_roles_data'].append(user_data)
                context['roles'] = roles
                context['member'] = member
                context['no_of_roles'] = roles.count()
                context['multiple_roles'] = roles.count() > 1
                context['role'] = roles.first().role.name if roles.exists() else COMMON_ROLE_CONFIG["NO_ROLE"]["name"]

            except Member.DoesNotExist:
                logger.error(f"Member not found for user: {user.id}")
                context['role'] = COMMON_ROLE_CONFIG["NO_ROLE"]["name"]
    else:
        logger.debug(f"Anonymous user")
        context['role'] = COMMON_ROLE_CONFIG["NO_ROLE"]["name"]
        context['anonymous'] = True

    # Assign template based on role
    template_url = get_template_for_role(context)

    try:
        get_template(template_url)
        return render(request, template_url, context)
    except TemplateDoesNotExist:
        logger.error(f"Template not found: {template_url}")
        template_url = f"{app_name}/{module_dirname}/general_homepage/general_homepage.html"
        return render(request, template_url, context)

def get_template_for_role(context):
    app_name = "app_jivapms"
    module_dirname = "mod_web"
    
    if context['super_user']:
        return f"{app_name}/{module_dirname}/super_user/super_user_homepage.html"
    elif context['multiple_roles']:
        return f"{app_name}/{module_dirname}/multiple_roles/multiple_roles_homepage.html"
    elif context['anonymous']:
        return f"{app_name}/{module_dirname}/index.html"
    
    role_to_template_map = {
        COMMON_ROLE_CONFIG["SITE_ADMIN"]["name"]: "site_admin/site_admin_homepage.html",
        COMMON_ROLE_CONFIG["ORG_ADMIN"]["name"]: "org_admin/org_admin_homepage.html",
        COMMON_ROLE_CONFIG["PROJECT_ADMIN"]["name"]: "project_admin/project_admin_homepage.html",
    }
    
    role = context.get('role')
    if role in role_to_template_map:
        return f"{app_name}/{module_dirname}/{role_to_template_map[role]}"
    else:
        return f"{app_name}/{module_dirname}/general_homepage/general_homepage.html"

def role_homepage(request, role_name):
    user = request.user
    context = {
        'parent_page': 'home',
        'page': 'role_homepage',
        'page_title': 'Role Home Page',
    }
    template_url = f"app_jivapms/mod_web/{role_name}/{role_name}_homepage.html"

    try:
        # Try to load the template, if it exists
        get_template(template_url)
        logger.debug(f"Template found: {template_url}")
        return render(request, template_url, context)
    except TemplateDoesNotExist:
        logger.error(f"Template not found: {template_url}")
        # Fall back to the default template
        general_template_url = "app_jivapms/mod_web/general_homepage/general_homepage.html"
        return render(request, general_template_url, context)



def about_the_project(request):

    
    context = {
        'parent_page': 'home',
        'page': 'about_the_project',
        'page_title': 'About the Project',
    }
    template_url = f"app_jivapms/mod_web/about_the_project.html"
    return render(request, template_url, context)   

def blogs(request):

    
    context = {
        'parent_page': 'home',
        'page': 'blogs',
        'page_title': 'Blogs Page',
    }
    template_url = f"app_common/common_files/specific/blogs.html"
    return render(request, template_url, context)   



def learn(request):

    
    context = {
        'parent_page': 'home',
        'page': 'learn',
        'page_title': 'Learning Page',
    }
    template_url = f"app_common/common_files/specific/learn.html"
    return render(request, template_url, context)   


def about(request):
    # common about
    
    context = {
        'parent_page': 'home',
        'page': 'about',
        'page_title': 'About Page',
    }
    template_url = f"app_common/common_files/specific/about.html"
    return render(request, template_url, context)   
