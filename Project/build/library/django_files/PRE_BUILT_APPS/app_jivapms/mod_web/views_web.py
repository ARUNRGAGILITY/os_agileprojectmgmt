from app_web.mod_app.all_view_imports import *
from app_memberprofilerole.mod_app.all_model_imports import *
from app_memberprofilerole.mod_member.models_member import *

from app_jivapms.mod_app.all_view_imports import *

app_name = "app_jivapms"
version = "v1"
module_dirname = "mod_web"

from app_jivapms.mod_web.helper_web import *
# Create your views here.
def index(request):
    print(f">>> === ****************JivaPMS: index ***************** === <<<")
    user = request.user
    roles = []
    member = None
    super_user = False
    multiple_roles = False
    no_of_roles = 0
    app_name = "app_jivapms"
    role = None
    # user's home page
    if user.is_authenticated:
        print(f">>> === User is authenticated: {user} === <<<")
        print(f">>> === User is authenticated: {user.id} === <<<")
        if user.is_superuser:
            print(f">>> === User is superuser: {user} === <<<")
            super_user = True
            role = COMMON_ROLE_CONFIG["SUPER_USER"]["name"]
        else:
            print(f">>> === User is normal user: {user} === <<<")
            member = Member.objects.get(user__id=user.id)
            print(f">>> === Member is normal user: {member} === <<<")
            roles = member.member_roles.filter(active=True)
            no_of_roles = roles.count()
            if roles.count() > 1:
                multiple_roles = True
            else:
                check = roles.first()
                role = check.role.name if no_of_roles == 1 else COMMON_ROLE_CONFIG["NO_ROLE"]["name"]

        logger.debug(f">>> === LOGGER DEBUG {roles}:{role} === <<<")
    else:
        return redirect('at_login')
    ## gather user roles data
    user_roles_data = []
    members = Member.objects.prefetch_related('member_roles__role', 'member_roles__org').filter(user=user)
    
    for member in members:
        user_data = {
            'member_id': member.id,
            'username': member.user.username if member.user else 'Unknown User',
            'roles': []
        }

        for role in member.member_roles.filter(active=True, member=member):
            role_data = {
                'org_id': role.org.id if role.org else None,
                'role_id': role.role.id if role.role else None,
                'role_name': role.role.name if role.role else 'No Role',
                'org_name': role.org.name if role.org else 'No Org',
                'lc_role_name': role.role.name.lower().replace(' ', '_')  if role.role else 'no page',
            }
            user_data['roles'].append(role_data)

        user_roles_data.append(user_data)



    context = {
        'parent_page': 'home',
        'page': 'index',
        'page_title': 'Home Page',

        'user': user,
        'roles': roles,
        'member': member,
        'super_user': super_user,
        'multiple_roles': multiple_roles,
        'no_of_roles': no_of_roles,
        'user_roles_data': user_roles_data,
        
    }
    
    super_user_page_display = "super_user_homepage.html"
    site_admin_page_display = "site_admin_homepage.html"
    org_admin_page_display = "org_admin_homepage.html"
    project_admin_page_display = "project_admin_homepage.html"
    multiple_roles_page_display = "multiple_roles_homepage.html"
    user_page_display = "index.html"
    template_url = f"{app_name}/{module_dirname}/{user_page_display}"
    if super_user:
        template_url = f"{app_name}/{module_dirname}/super_user/{super_user_page_display}" 
        role = COMMON_ROLE_CONFIG["SUPER_USER"]["name"]
    else:
        if role == COMMON_ROLE_CONFIG["SITE_ADMIN"]["name"]:
            template_url = f"{app_name}/{module_dirname}/site_admin/{site_admin_page_display}"
        if role == COMMON_ROLE_CONFIG["ORG_ADMIN"]["name"]:
            template_url = f"{app_name}/{module_dirname}/org_admin/{org_admin_page_display}"
        if role == COMMON_ROLE_CONFIG["PROJECT_ADMIN"]["name"]:
            template_url = f"{app_name}/{module_dirname}/project_admin/{project_admin_page_display}"
        if multiple_roles:
            template_url = f"{app_name}/{module_dirname}/multiple_roles/{multiple_roles_page_display}"
        else:
            role_page = role.role.name.lower().replace(' ', '_') 
            template_url = f"{app_name}/{module_dirname}/{role_page}/{role_page}_homepage.html"
    logger.debug(f">>> === **** role is ==> {role} === <<<")
    print(f">>> === template_url: {template_url} === <<<")
    return render(request, template_url, context)   


def role_homepage(request, role_name):
    user = request.user
    context = {
        'parent_page': 'home',
        'page': 'role_homepage',
        'page_title': 'Role Home Page',
    }
    template_url = f"app_jivapms/mod_web/{role_name}/{role_name}_homepage.html"
    template_dir = settings.TEMPLATES[0]['DIRS']
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
