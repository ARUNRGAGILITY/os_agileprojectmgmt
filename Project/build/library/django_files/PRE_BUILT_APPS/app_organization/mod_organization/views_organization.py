
from app_organization.mod_app.all_view_imports import *
from app_organization.mod_organization.models_organization import *
from app_organization.mod_organization.forms_organization import *

app_name = 'app_organization'
app_version = 'v1'

module_name = 'organizations'
module_path = f'mod_organization'

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
def list_organizations(request):
    # take inputs
    # process inputs
    user = request.user       
    objects_count = 0    
    show_all = request.GET.get('all', '25')
    objects_per_page = int(show_all) if show_all != 'all' else 25
    pagination_options = [5, 10, 15, 25, 50, 100, 'all']
    selected_bulk_operations = None
    search_query = request.GET.get('search', '')
    deleted_count = 0
    
    if search_query:
        tobjects = Organization.objects.filter(name__icontains=search_query, 
                                            active=True,deleted=False, **viewable_dict ).order_by('position')
        deleted = Organization.objects.filter(active=False, deleted=False,**viewable_dict).order_by('position')
        deleted_count = deleted.count()
    else:
        tobjects = Organization.objects.filter(active=True).order_by('position')
        deleted = Organization.objects.filter(active=False, deleted=False,**viewable_dict).order_by('position')
        deleted_count = deleted.count()
    
    if show_all == 'all':
        # No pagination, show all records
        page_obj = tobjects
        objects_per_page = tobjects.count()
    else:
        print(f">>> === show_all: {show_all} === <<<")   
        objects_per_page = int(show_all)     
        paginator = Paginator(tobjects, objects_per_page)  # Show 10 tobjects per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    
    objects_count = tobjects.count()
    
    ## processing the POST
    if request.method == 'POST':
        selected_bulk_operations = request.POST.getlist('bulk_operations')
        bulk_operation = str(selected_bulk_operations[0].strip()) if selected_bulk_operations else None
            
        if 'selected_item' in request.POST:  
            selected_items = request.POST.getlist('selected_item')  # Use getlist to ensure all are captured
            for item_id in selected_items:
                item = int(item_id)  
                if bulk_operation == 'bulk_delete':
                    object = get_object_or_404(Organization, pk=item, active=True, **viewable_dict)
                    object.active = False
                    object.save()
                    
                elif bulk_operation == 'bulk_done':
                    object = get_object_or_404(Organization, pk=item, active=True, **viewable_dict)
                    object.done = True
                    object.save()
                    
                elif bulk_operation == 'bulk_not_done':
                    object = get_object_or_404(Organization, pk=item, active=True, **viewable_dict)
                    object.done = False
                    object.save()
                    
                elif bulk_operation == 'bulk_blocked':  # Correct the operation check here
                    object = get_object_or_404(Organization, pk=item, active=True, **viewable_dict)
                    object.blocked = True
                    object.save()
                    
                else:
                    return redirect('list_organizations')
            return redirect('list_organizations')
    
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_organizations',
        
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

        'page_title': f'Organization List',
    }       
    template_file = f"{app_name}/{module_path}/list_organizations.html"
    return render(request, template_file, context)



# list the deleted objects
# ============================================================= #
@login_required
def list_deleted_organizations(request):
    # take inputs
    # process inputs
    user = request.user        
    objects_count = 0    
    show_all = request.GET.get('all', '25')
    objects_per_page = int(show_all) if show_all != 'all' else 25
    pagination_options = [5, 10, 15, 25, 50, 100, 'all']
    selected_bulk_operations = None

    show_all = request.GET.get('all', '25')
    objects_per_page = int(show_all) if show_all != 'all' else 25
    
    search_query = request.GET.get('search', '')
    if search_query:
        tobjects = Organization.objects.filter(name__icontains=search_query, 
                                            **viewable_dict, active=False, deleted=False).order_by('position')
    else:
        tobjects = Organization.objects.filter(active=False, deleted=False, **viewable_dict).order_by('position')
    
    if show_all == 'all':
        # No pagination, show all records
        page_obj = tobjects
        objects_per_page = tobjects.count()
    else:
        print(f">>> === show_all: {show_all} === <<<")   
        objects_per_page = int(show_all)     
        paginator = Paginator(tobjects, objects_per_page)  # Show 10 tobjects per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    objects_count = tobjects.count()
    
    ## processing the POST
    if request.method == 'POST':
        selected_bulk_operations = request.POST.getlist('bulk_operations')
        bulk_operation = str(selected_bulk_operations[0].strip()) if selected_bulk_operations else None
            
        if 'selected_item' in request.POST:  
                selected_items = request.POST.getlist('selected_item')  # Use getlist to ensure all are captured
                for item_id in selected_items:
                    item = int(item_id)  
                    if bulk_operation == 'bulk_restore':
                        object = get_object_or_404(Organization, pk=item, active=False, **viewable_dict)
                        object.active = True               
                        object.save()
                    elif bulk_operation == 'bulk_erase':
                        object = get_object_or_404(Organization, pk=item, active=False, **viewable_dict)
                        object.active = False  
                        object.deleted = True             
                        object.save()
                    else:
                        return redirect('list_deleted_organizations')
                return redirect('list_deleted_organizations')
    
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_deleted_organizations',
        
        'module_path': module_path,
        'user': user,
        'tobjects': tobjects,
        'page_obj': page_obj,
        'objects_count': objects_count,
        'objects_per_page': objects_per_page,
        'show_all': show_all,
        'pagination_options': pagination_options,
        'selected_bulk_operations': selected_bulk_operations,

        'page_title': f'Organization List',
    }       
    template_file = f"{app_name}/{module_path}/list_deleted_organizations.html"
    return render(request, template_file, context)





# Create View
@login_required
def create_organization(request):
    user = request.user
    
    if request.method == 'POST':
        form = OrganizationForm(request.POST)
        if form.is_valid():
            form.instance.author = user
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_organizations')
    else:
        form = OrganizationForm()

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'create_organization',
        
        'module_path': module_path,
        'form': form,
        'page_title': f'Create Organization',
    }
    template_file = f"{app_name}/{module_path}/create_organization.html"
    return render(request, template_file, context)




# Edit
@login_required
def edit_organization(request, organization_id):
    user = request.user
    
    object = get_object_or_404(Organization, pk=organization_id, active=True, **viewable_dict)
    if request.method == 'POST':
        form = OrganizationForm(request.POST, instance=object)
        if form.is_valid():
            form.instance.author = user
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_organizations')
    else:
        form = OrganizationForm(instance=object)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'edit_organization',
        
        'module_path': module_path,
        'form': form,
        'object': object,
        'page_title': f'Edit Organization',
    }
    template_file = f"{app_name}/{module_path}/edit_organization.html"
    return render(request, template_file, context)



@login_required
def delete_organization(request, organization_id):
    user = request.user
    
    object = get_object_or_404(Organization, pk=organization_id, active=True, **viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.save()
        return redirect('list_organizations')

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'delete_organization',
        
        'module_path': module_path,        
        'object': object,
        'page_title': f'Delete Organization',
    }
    template_file = f"{app_name}/{module_path}/delete_organization.html"
    return render(request, template_file, context)


@login_required
def permanent_deletion_organization(request, organization_id):
    user = request.user
    
    object = get_object_or_404(Organization, pk=organization_id, active=False, deleted=False, **viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.deleted = True
        object.save()
        return redirect('list_organizations')

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'permanent_deletion_organization',
        
        'module_path': module_path,        
        'object': object,
        'page_title': f'Permanent Deletion Organization',
    }
    template_file = f"{app_name}/{module_path}/permanent_deletion_organization.html"
    return render(request, template_file, context)


@login_required
def restore_organization(request, organization_id):
    user = request.user
    object = get_object_or_404(Organization, pk=organization_id, active=False, **viewable_dict)
    object.active = True
    object.save()
    return redirect('list_organizations')
   


@login_required
def view_organization(request,  organization_id):
    user = request.user
    
    object = get_object_or_404(Organization, pk=organization_id, active=True, **viewable_dict)    

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'view_organization',
        
        'module_path': module_path,
        'object': object,
        'page_title': f'View Organization',
    }
    template_file = f"{app_name}/{module_path}/view_organization.html"
    return render(request, template_file, context)


@login_required
def configure_organization(request,  organization_id):
    user = request.user
    
    object = get_object_or_404(Organization, pk=organization_id, active=True, **viewable_dict)    

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'configure_organization',
        
        'module_path': module_path,
        'object': object,
        'page_title': f'Configure Organization',
    }
    template_file = f"{app_name}/{module_path}/configure_organization.html"
    return render(request, template_file, context)
