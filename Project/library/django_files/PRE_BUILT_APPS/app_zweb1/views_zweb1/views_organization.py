from app_zweb1.views_zweb1.view_imports import *
app_name = 'app_zweb1'
app_version = 'v1'

@login_required
def organization_list(request):
    # take inputs
    # process inputs
    user = request.user   
    list_organizations = Organization.objects.filter(active=True)
    # send outputs (info, template,
    context = {
        'parent_page': 'loggedin_home_page',
        'page': 'organization_list',
        'user': user,
        'list_organizations': list_organizations,
    }       
    template_file = f"{app_name}/organization/organization_list.html"
    return render(request, template_file, context)

