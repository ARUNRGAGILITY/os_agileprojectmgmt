
from app_organization.mod_app.all_view_imports import *
from app_organization.mod_project.models_project import *
from app_organization.mod_project.forms_project import *

from app_organization.mod_organization.models_organization import *

from app_common.mod_common.models_common import *

from app_memberprofilerole.mod_role.models_role import *
from app_jivapms.mod_app.all_view_imports import *

from app_organization.org_decorators import *

app_name = 'app_organization'
app_version = 'v1'

module_name = 'projects'
module_path = f'mod_project'


org_admin_str = COMMON_ROLE_CONFIG['ORG_ADMIN']['name']
project_admin_str = COMMON_ROLE_CONFIG['PROJECT_ADMIN']['name']

PROJECT_ADMIN_ROLE_STR = COMMON_PROJECT_ROLE_CONFIG['PROJECT_ADMIN']
PROJECT_EDITOR_ROLE_STR = COMMON_PROJECT_ROLE_CONFIG['PROJECT_EDITOR']
PROJECT_VIEWER_ROLE_STR = COMMON_PROJECT_ROLE_CONFIG['PROJECT_VIEWER']
PROJECT_NOROLE_ROLE_STR = COMMON_PROJECT_ROLE_CONFIG['PROJECT_NOROLE']

# First, fetch the Role objects for 'Project Admin' and 'Org Admin'
project_admin_role = Role.objects.get(name=project_admin_str)  # 'Project Admin'
org_admin_role = Role.objects.get(name=org_admin_str)  # 'Org Admin'

# viewable flag
first_viewable_flag = '__ALL__'  # 'all' or '__OWN__'
viewable_flag = '__ALL__'  # 'all' or '__OWN__'
# Setup dictionaries based on flags
viewable_dict = {} if viewable_flag == '__ALL__' else {'author': user}
first_viewable_dict = {} if first_viewable_flag == '__ALL__' else {'author': user}
def get_viewable_dicts(user, viewable_flag, first_viewable_flag):
    viewable_dict = {} if viewable_flag == '__ALL__' else {'author': user}
    first_viewable_dict = {} if first_viewable_flag == '__ALL__' else {'author': user}
    return viewable_dict, first_viewable_dict
# ============================================================= #
@login_required
def list_projects(request, org_id):
    user = request.user
    objects_count = 0
    show_all = request.GET.get('all', '25')
    objects_per_page = int(show_all) if show_all != 'all' else 25
    pagination_options = [5, 10, 15, 25, 50, 100, 'all']
    selected_bulk_operations = None
    deleted_count = 0

    # Fetch the organization
    organization = get_object_or_404(Organization, id=org_id, active=True)
    member = Member.objects.get(user=user, org=organization, active=True)
    user_roles = MemberOrganizationRole.objects.filter(member=member)    
    relevant_admin = user_roles.filter(role__name__in=[org_admin_str, project_admin_str]).exists()
    logger.debug(f">>> === RELEVANT ADMIN: {relevant_admin} === <<<")    
    is_org_admin = user_roles.filter(role__name__in=[org_admin_str]).exists()
    user_memberships = ProjectMembership.objects.filter(project__org=organization, member=member, active=True)
    is_project_admin = user_memberships.filter(project_role__role_type=PROJECT_ADMIN_ROLE_STR).exists()
    logger.debug(f">>> === User memberships queryset: {user_memberships.values()} === <<<")
    logger.debug(f">>> === CHECKING1: {user.username} ==> User roles: {user_roles}, Memberships: {user_memberships}, Org Admin: {is_org_admin}, Project Admin: {is_project_admin} === <<<")
 
    # Filter projects based on user access
    if is_org_admin:
        # Org admins can see all active projects in the organization
        tobjects = Project.objects.filter(active=True, org_id=org_id)
        logger.debug(f">>> === Projects:{tobjects} === <<<")
    else:
        # Filter projects where the user has specific project membership (Viewer, Editor, Admin)
        tobjects = Project.objects.filter(
            id__in=user_memberships.values_list('project_id', flat=True),
            active=True,
            org_id=org_id
        )
    logger.debug(f">>> === Projects:{tobjects} === <<<")
    # Process search query
    search_query = request.GET.get('search', '')
    if search_query:
        tobjects = tobjects.filter(name__icontains=search_query).order_by('position')
    else:
        tobjects = tobjects.order_by('position')
        deleted = Project.objects.filter(active=False, org_id=org_id)
        deleted_count = deleted.count()

    # Handle pagination
    if show_all == 'all':
        page_obj = tobjects
        objects_per_page = tobjects.count()
    else:
        paginator = Paginator(tobjects, objects_per_page)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    objects_count = tobjects.count()

    ## Handle POST requests for bulk operations
    if request.method == 'POST':
        selected_bulk_operations = request.POST.getlist('bulk_operations')
        bulk_operation = str(selected_bulk_operations[0].strip()) if selected_bulk_operations else None

        if 'selected_item' in request.POST:
            selected_items = request.POST.getlist('selected_item')
            for item_id in selected_items:
                item = int(item_id)
                project = get_object_or_404(Project, pk=item, active=True)

                if bulk_operation == 'bulk_delete':
                    project.active = False
                    project.save()
                elif bulk_operation == 'bulk_done':
                    project.done = True
                    project.save()
                elif bulk_operation == 'bulk_not_done':
                    project.done = False
                    project.save()
                elif bulk_operation == 'bulk_blocked':
                    project.blocked = True
                    project.save()
                else:
                    return redirect('list_projects', org_id=org_id)

            return redirect('list_projects', org_id=org_id)

    # Prepare the context for the template
    context = {
        'parent_page': 'Projects',
        'page': 'list_projects',
        'organization': organization,
        'org_id': org_id,
        'user': user,
        'tobjects': tobjects,
        'page_obj': page_obj,
        'objects_count': objects_count,
        'objects_per_page': objects_per_page,
        'deleted_count': deleted_count,
        'show_all': show_all,
        'pagination_options': pagination_options,
        'selected_bulk_operations': selected_bulk_operations,
        'page_title': 'Project List',
        'is_org_admin': is_org_admin,
        'is_project_admin': is_project_admin,
        'relevant_admin': relevant_admin,
        'user_roles': user_roles,
        'user_memberships': user_memberships,
    }

    template_file = f"{app_name}/{module_path}/list_projects.html"
    return render(request, template_file, context)


# ============================================================= #
@login_required
def list_deleted_projects(request, org_id):
    # take inputs
    # process inputs
    user = request.user       
    objects_count = 0    
    show_all = request.GET.get('all', '25')
    objects_per_page = int(show_all) if show_all != 'all' else 25
    pagination_options = [5, 10, 15, 25, 50, 100, 'all']
    selected_bulk_operations = None
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    
    search_query = request.GET.get('search', '')
    if search_query:
        tobjects = Project.objects.filter(name__icontains=search_query, 
                                            active=False,
                                            org_id=org_id, **viewable_dict).order_by('position')
    else:
        tobjects = Project.objects.filter(active=False, org_id=org_id,
                                            **viewable_dict).order_by('position')        
    
    if show_all == 'all':
        # No pagination, show all records
        page_obj = tobjects
        objects_per_page = tobjects.count()
    else:
        objects_per_page = int(show_all)     
        paginator = Paginator(tobjects, objects_per_page)  
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    objects_count = tobjects.count()
    
    ## processing the POST
    if request.method == 'POST':
        selected_bulk_operations = request.POST.getlist('bulk_operations')
        bulk_operation = str(selected_bulk_operations[0].strip()) if selected_bulk_operations else None
     
        if 'selected_item' in request.POST:  # Correct the typo here
                selected_items = request.POST.getlist('selected_item')  # Use getlist to ensure all are captured
                for item_id in selected_items:
                    item = int(item_id)  # Ensure item_id is converted to int if necessary
                    if bulk_operation == 'bulk_restore':
                        object = get_object_or_404(Project, pk=item, active=False, **viewable_dict)
                        object.active = True
                        object.save()         
                    elif bulk_operation == 'bulk_erase':
                        object = get_object_or_404(Project, pk=item, active=False, **viewable_dict)
                        object.active = False  
                        object.deleted = True             
                        object.save()    
                    else:
                        redirect('list_projects', org_id=org_id)
                redirect('list_projects', org_id=org_id)
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_deleted_projects',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,
        'user': user,
        'tobjects': tobjects,
        'page_obj': page_obj,
        'objects_count': objects_count,
        'objects_per_page': objects_per_page,
        'show_all': show_all,
        'pagination_options': pagination_options,
        'selected_bulk_operations': selected_bulk_operations,
        'page_title': f'Project List',
    }       
    template_file = f"{app_name}/{module_path}/list_deleted_projects.html"
    return render(request, template_file, context)



# # Create View
# @login_required
# @org_access_required(allowed_roles=['Project Admin'])
# def create_project(request, org_id):
#     user = request.user
#     organization = Organization.objects.get(id=org_id, active=True, 
#                                                 **first_viewable_dict)
    
#     if request.method == 'POST':
#         form = ProjectForm(request.POST)
#         if form.is_valid():
#             form.instance.author = user
#             form.instance.org_id = org_id
#             form.save()
#         else:
#             print(f">>> === form.errors: {form.errors} === <<<")
#         return redirect('list_projects', org_id=org_id)
#     else:
#         form = ProjectForm()

#     context = {
#         'parent_page': '___PARENTPAGE___',
#         'page': 'create_project',
#         'organization': organization,
#         'org_id': org_id,
        
#         'module_path': module_path,
#         'form': form,
#         'page_title': f'Create Project',
#     }
#     template_file = f"{app_name}/{module_path}/create_project.html"
#     return render(request, template_file, context)

@login_required
@org_access_required()
def create_project(request, member, org_membership, org_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, **first_viewable_dict)
    logger.debug(f">>> === ORG_DECORATOR: {user.username} ==> User roles: {org_membership} === <<<")
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.author = user
            project.org_id = org_id
            project.save()
            
            # Check if the member has 'Project Admin' role in the organization
            if org_membership.role.name == 'Project Admin':
                # Create or get the 'Admin' role for the project
                admin_role, created = ProjectRole.objects.get_or_create(role_type=PROJECT_ADMIN_ROLE_STR)

                # Assign the member as 'Admin' in the ProjectMembership
                ProjectMembership.objects.create(
                    member=member,
                    project=project,
                    project_role=admin_role
                )
            
            return redirect('list_projects', org_id=org_id)
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
    else:
        form = ProjectForm()

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'create_project',
        'organization': organization,
        'org_id': org_id,
        'module_path': module_path,
        'form': form,
        'page_title': f'Create Project',
    }

    template_file = f"{app_name}/{module_path}/create_project.html"
    return render(request, template_file, context)



# Edit
@login_required
def edit_project(request, org_id, project_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(Project, pk=project_id, active=True,**viewable_dict)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=object)
        if form.is_valid():
            form.instance.author = user
            form.instance.org_id = org_id
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_projects', org_id=org_id)
    else:
        form = ProjectForm(instance=object)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'edit_project',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,
        'form': form,
        'object': object,
        'page_title': f'Edit Project',
    }
    template_file = f"{app_name}/{module_path}/edit_project.html"
    return render(request, template_file, context)



@login_required
def delete_project(request, org_id, project_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(Project, pk=project_id, active=True,**viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.save()
        return redirect('list_projects', org_id=org_id)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'delete_project',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,        
        'object': object,
        'page_title': f'Delete Project',
    }
    template_file = f"{app_name}/{module_path}/delete_project.html"
    return render(request, template_file, context)


@login_required
def permanent_deletion_project(request, org_id, project_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(Project, pk=project_id, active=False, deleted=False, **viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.deleted = True
        object.save()
        return redirect('list_projects', org_id=org_id)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'permanent_deletion_project',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,        
        'object': object,
        'page_title': f'Permanent Deletion Project',
    }
    template_file = f"{app_name}/{module_path}/permanent_deletion_project.html"
    return render(request, template_file, context)


@login_required
def restore_project(request,  org_id, project_id):
    user = request.user
    object = get_object_or_404(Project, pk=project_id, active=False,**viewable_dict)
    object.active = True
    object.save()
    return redirect('list_projects', org_id=org_id)
   


@login_required
def view_project(request, org_id, project_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(Project, pk=project_id, active=True,**viewable_dict)    

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'view_project',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,
        'object': object,
        'page_title': f'View Project',
    }
    template_file = f"{app_name}/{module_path}/view_project.html"
    return render(request, template_file, context)


