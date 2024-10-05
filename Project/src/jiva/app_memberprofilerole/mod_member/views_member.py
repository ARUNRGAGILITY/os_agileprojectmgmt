
from app_memberprofilerole.mod_app.all_view_imports import *
from app_memberprofilerole.mod_member.models_member import *
from app_memberprofilerole.mod_member.forms_member import *

from app_organization.mod_organization.models_organization import *

from app_common.mod_common.models_common import *

app_name = 'app_memberprofilerole'
app_version = 'v1'

module_name = 'members'
module_path = f'mod_member'

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
def list_members(request, org_id):
    # take inputs
    # process inputs
    user = request.user       
    objects_count = 0    
    show_all = request.GET.get('all', '25')
    objects_per_page = int(show_all) if show_all != 'all' else 25
    pagination_options = [5, 10, 15, 25, 50, 100, 'all']
    selected_bulk_operations = None
    deleted_count = 0
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    
    search_query = request.GET.get('search', '')
    if search_query:
        tobjects = Member.objects.filter(name__icontains=search_query, 
                                            org_id=org_id, **viewable_dict).prefetch_related('member_roles__role').order_by('position')
    else:
        tobjects = Member.objects.filter(active=True, **viewable_dict).prefetch_related('member_roles__role').order_by('position')
        deleted = Member.objects.filter(active=False, deleted=False,
                                org_id=org_id,
                               **viewable_dict).order_by('position')
        deleted_count = deleted.count()
    
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
                if bulk_operation == 'bulk_delete':
                    object = get_object_or_404(Member, pk=item, active=True, **viewable_dict)
                    object.active = False
                    object.save()
                    
                elif bulk_operation == 'bulk_done':
                    object = get_object_or_404(Member, pk=item, active=True, **viewable_dict)
                    object.done = True
                    object.save()
                    
                elif bulk_operation == 'bulk_not_done':
                    object = get_object_or_404(Member, pk=item, active=True, **viewable_dict)
                    object.done = False
                    object.save()
                    
                elif bulk_operation == 'bulk_blocked':  # Correct the operation check here
                    object = get_object_or_404(Member, pk=item, active=True, **viewable_dict)
                    object.blocked = True
                    object.save()
                    
                else:
                    redirect('list_members', org_id=org_id)
            return redirect('list_members', org_id=org_id)
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_members',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,
        'user': user,
        'tobjects': tobjects,
        'page_obj': page_obj,
        'objects_count': objects_count,
        'objects_per_page': objects_per_page,
        'deleted_count': deleted_count,
        'show_all': show_all,
        
        'pagination_options': pagination_options,
        'selected_bulk_operations': selected_bulk_operations,
        'page_title': f'Member List',
    }       
    template_file = f"{app_name}/{module_path}/list_members.html"
    return render(request, template_file, context)





# ============================================================= #
@login_required
def list_deleted_members(request, org_id):
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
        tobjects = Member.objects.filter(name__icontains=search_query, 
                                            active=False,
                                            org_id=org_id, **viewable_dict).order_by('position')
    else:
        tobjects = Member.objects.filter(active=False, org_id=org_id,
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
                        object = get_object_or_404(Member, pk=item, active=False, **viewable_dict)
                        object.active = True
                        object.save()         
                    elif bulk_operation == 'bulk_erase':
                        object = get_object_or_404(Member, pk=item, active=False, **viewable_dict)
                        object.active = False  
                        object.deleted = True             
                        object.save()    
                    else:
                        redirect('list_members', org_id=org_id)
                redirect('list_members', org_id=org_id)
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_deleted_members',
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
        'page_title': f'Member List',
    }       
    template_file = f"{app_name}/{module_path}/list_deleted_members.html"
    return render(request, template_file, context)



@login_required
def create_member(request, org_id):
    user = request.user
    organization = get_object_or_404(Organization, id=org_id, active=True)
    
    if request.method == 'POST':
        member_form = MemberForm(request.POST)
        org_role_form = MemberOrganizationRoleForm(request.POST, org_id=org_id)
        
        if member_form.is_valid():
            member = member_form.save(commit=False)
            member.org_id = org_id
            member.save()
            roles = request.POST.getlist('role')
            for role_id in roles:
                role = get_object_or_404(Role, id=role_id)
                MemberOrganizationRole.objects.create(
                    member=member,
                    org_id = org_id,
                    role_id=role.id
                )
            messages.success(request, 'Member and roles have been successfully assigned.')
            return redirect('list_members', org_id=org_id)
        else:
            print(f">>> === member_form.errors: {member_form.errors} === <<<")
            print(f">>> === org_role_form.errors: {org_role_form.errors} === <<<")
    else:
        member_form = MemberForm()
        org_role_form = MemberOrganizationRoleForm(org_id=org_id)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'create_member',
        'organization': organization,
        'org_id': org_id,
        'member_form': member_form,
        'org_role_form': org_role_form,
        'module_path': module_path,
        'page_title': f'Create Member',
    }
    template_file = f"{app_name}/{module_path}/create_member.html"
    return render(request, template_file, context)

def is_site_admin(user):
    return user.is_superuser or user.groups.filter(name='Admin').exists()

@login_required
@user_passes_test(is_site_admin)
def member_admin(request, org_id):
    user = request.user
    organization = get_object_or_404(Organization, id=org_id, active=True)
    
    if request.method == 'POST':
        member_form = MemberAdminForm(request.POST)
        org_role_form = MemberOrganizationRoleForm(request.POST, org_id=org_id)
        
        if member_form.is_valid():
            member = member_form.save(commit=False)
            member.org_id = org_id
            member.save()
            roles = request.POST.getlist('role')
            for role_id in roles:
                role = get_object_or_404(Role, id=role_id)
                MemberOrganizationRole.objects.create(
                    member=member,
                    org_id = org_id,
                    role_id=role.id
                )
            messages.success(request, 'Member and roles have been successfully assigned.')
            return redirect('list_members', org_id=org_id)
        else:
            print(f">>> === member_form.errors: {member_form.errors} === <<<")
            print(f">>> === org_role_form.errors: {org_role_form.errors} === <<<")
    else:
        member_form = MemberAdminForm()
        org_role_form = MemberOrganizationRoleForm(org_id=org_id)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'member_admin',
        'organization': organization,
        'org_id': org_id,
        'member_form': member_form,
        'org_role_form': org_role_form,
        'module_path': module_path,
        'page_title': f'Member Admin',
    }
    template_file = f"{app_name}/{module_path}/member_admin.html"
    return render(request, template_file, context)


# Create View
@login_required
def create_member_backup1(request, org_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            member = form.save(commit=False)
            member.author = request.user
            selected_org_id = form.cleaned_data['org'].id
            member.org_id = selected_org_id
            
            member.save()
            # Save the roles
            
            print(f">>> === selected_org_id: {selected_org_id} === <<<")
            print(f">>> === form.cleaned_data['roles']: {form.cleaned_data['roles']} === <<<")
            form.save_m2m() 
            messages.success(request, 'Member has been successfully assigned.')
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_members', org_id=org_id)
    else:
        form = MemberForm()

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'create_member',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,
        'form': form,
        'page_title': f'Create Member',
    }
    template_file = f"{app_name}/{module_path}/create_member.html"
    return render(request, template_file, context)


# Edit
@login_required
def edit_member(request, org_id, member_id):
    user = request.user
    organization = get_object_or_404(Organization, id=org_id, active=True)
    member = get_object_or_404(Member, pk=member_id, active=True)
    member_roles = MemberOrganizationRole.objects.filter(member=member)
    
    if request.method == 'POST':
        member_form = EditMemberForm(request.POST, instance=member)
        org_role_form = MemberOrganizationRoleForm(request.POST, org_id=org_id)
        
        if member_form.is_valid() :
            member = member_form.save(commit=False)
            member.user_id = request.POST.get('user_id')
            member.org_id = org_id
            member.save()
            MemberOrganizationRole.objects.filter(member=member).delete()
            roles = request.POST.getlist('role')
            for role_id in roles:
                role = get_object_or_404(Role, id=role_id)
                MemberOrganizationRole.objects.create(
                    member=member,
                    org_id=org_id,
                    role_id=role.id
                )
            messages.success(request, 'Member and roles have been successfully updated.')
            return redirect('list_members', org_id=org_id)
        else:
            print(f">>> === member_form.errors: {member_form.errors} === <<<")
            print(f">>> === org_role_form.errors: {org_role_form.errors} === <<<")
    else:
        initial_roles = member_roles.values_list('role', flat=True)
        member_form = EditMemberForm(instance=member)
        org_role_form = MemberOrganizationRoleForm(initial={'role': initial_roles}, org_id=org_id)


    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'edit_member',
        'organization': organization,
        'org_id': org_id,
        'member_form': member_form,
        'org_role_form': org_role_form,
        'req_user': user,
        'module_path': module_path,
        'object': object,
        'page_title': f'Edit Member',
    }
    template_file = f"{app_name}/{module_path}/edit_member.html"
    return render(request, template_file, context)



@login_required
def delete_member(request, org_id, member_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(Member, pk=member_id, active=True,**viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.save()
        return redirect('list_members', org_id=org_id)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'delete_member',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,        
        'object': object,
        'page_title': f'Delete Member',
    }
    template_file = f"{app_name}/{module_path}/delete_member.html"
    return render(request, template_file, context)


@login_required
def permanent_deletion_member(request, org_id, member_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(Member, pk=member_id, active=False, deleted=False, **viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.deleted = True
        object.save()
        return redirect('list_members', org_id=org_id)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'permanent_deletion_member',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,        
        'object': object,
        'page_title': f'Permanent Deletion Member',
    }
    template_file = f"{app_name}/{module_path}/permanent_deletion_member.html"
    return render(request, template_file, context)


@login_required
def restore_member(request,  org_id, member_id):
    user = request.user
    object = get_object_or_404(Member, pk=member_id, active=False,**viewable_dict)
    object.active = True
    object.save()
    return redirect('list_members', org_id=org_id)
   


@login_required
def view_member(request, org_id, member_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(Member, pk=member_id, active=True,**viewable_dict)    

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'view_member',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,
        'object': object,
        'page_title': f'View Member',
    }
    template_file = f"{app_name}/{module_path}/view_member.html"
    return render(request, template_file, context)

@login_required
def ajax_get_roles_for_organization(request):
    if request.method == 'POST':
        org_id = request.POST.get('org_id')
        organization = get_object_or_404(Organization, id=org_id)
        roles = organization.org_roles.filter(active=True)
        roles_list = list(roles.values('id', 'name'))
        print(f">>> === roles_list: {roles_list} === <<<")
        return JsonResponse(roles_list, safe=False)
    return JsonResponse({'error': 'Invalid request method'}, status=400)