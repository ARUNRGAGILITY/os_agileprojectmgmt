from app_backlog.mod_app.all_view_imports import *
from app_organization.mod_organization.models_organization import *

from app_backlog.mod_backlog_super_type.models_backlog_super_type import *
from app_backlog.mod_backlog_super_type.forms_backlog_super_type import *
# import the other two models root/content, content types 
from app_backlog.mod_backlog.models_backlog import *
from app_backlog.mod_backlog_type.models_backlog_type import *

app_name = 'app_backlog'
app_version = 'v1'

module_name = 'backlog_super_type'
module_path = f'mod_backlog_super_type'

# viewable flag
first_viewable_flag = '__ALL__'  # 'all' or '__OWN__'
viewable_flag = '__ALL__'  # 'all' or '__OWN__'
# Setup dictionaries based on flags
viewable_dict = {} if viewable_flag == '__ALL__' else {'author': user}
first_viewable_dict = {} if first_viewable_flag == '__ALL__' else {'author': user}
# ============================================================= #
@login_required
def list_backlog_super_types(request, org_id):
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
    # connect with connect id
    org = get_object_or_404(Organization, pk=org_id, **viewable_dict)
    if search_query:
        tobjects = BacklogSuperType.objects.filter(name__icontains=search_query, 
                                                org_id=org_id,
                                            active=True,deleted=False, **viewable_dict ).order_by('position')
        deleted = BacklogSuperType.objects.filter(active=False, deleted=False,
                                               org_id=org_id, 
                                               **viewable_dict).order_by('position')
        deleted_count = deleted.count()
    else:
        tobjects = BacklogSuperType.objects.filter(active=True, org_id=org_id, **viewable_dict).order_by('position')
        deleted = BacklogSuperType.objects.filter(active=False, deleted=False,**viewable_dict).order_by('position')
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
                    object = get_object_or_404(BacklogSuperType, pk=item, active=True, **viewable_dict)
                    object.active = False
                    object.save()
                    
                elif bulk_operation == 'bulk_done':
                    object = get_object_or_404(BacklogSuperType, pk=item, active=True, **viewable_dict)
                    object.done = True
                    object.save()
                    
                elif bulk_operation == 'bulk_not_done':
                    object = get_object_or_404(BacklogSuperType, pk=item, active=True, **viewable_dict)
                    object.done = False
                    object.save()
                    
                elif bulk_operation == 'bulk_blocked':  # Correct the operation check here
                    object = get_object_or_404(BacklogSuperType, pk=item, active=True, **viewable_dict)
                    object.blocked = True
                    object.save()
                    
                else:
                    return redirect('list_backlog_super_types')
            return redirect('list_backlog_super_types')
    
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_backlog_super_types',
        'org_id': org_id,
        'org': org,
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

        'page_title': f'Backlog Super Type List',
    }       
    template_file = f"{app_name}/{module_path}/list__backlog_super_types.html"
    return render(request, template_file, context)



# list the deleted objects
# ============================================================= #
@login_required
def list_deleted_backlog_super_types(request, org_id):
    # take inputs
    # process inputs
    user = request.user        
    objects_count = 0    
    show_all = request.GET.get('all', '25')
    objects_per_page = int(show_all) if show_all != 'all' else 25
    pagination_options = [5, 10, 15, 25, 50, 100, 'all']
    selected_bulk_operations = None
    # connect with connect id
    org = get_object_or_404(Organization, pk=org_id, **viewable_dict)
    show_all = request.GET.get('all', '25')
    objects_per_page = int(show_all) if show_all != 'all' else 25
    
    search_query = request.GET.get('search', '')
    if search_query:
        tobjects = BacklogSuperType.objects.filter(name__icontains=search_query, 
                                                org_id=org_id,
                                            **viewable_dict, active=False, deleted=False).order_by('position')
    else:
        tobjects = BacklogSuperType.objects.filter(active=False, deleted=False, 
                                                org_id=org_id,
                                                **viewable_dict).order_by('position')
    
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
                        object = get_object_or_404(BacklogSuperType, pk=item, active=False, **viewable_dict)
                        object.active = True               
                        object.save()
                    elif bulk_operation == 'bulk_erase':
                        object = get_object_or_404(BacklogSuperType, pk=item, active=False, **viewable_dict)
                        object.active = False  
                        object.deleted = True             
                        object.save()
                    else:
                        return redirect('list_deleted_backlog_super_types')
                return redirect('list_deleted_backlog_super_types')
    
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_deleted_backlog_super_types',
        'org_id': org_id,
        'org': org,
        'module_path': module_path,
        'user': user,
        'tobjects': tobjects,
        'page_obj': page_obj,
        'objects_count': objects_count,
        'objects_per_page': objects_per_page,
        'show_all': show_all,
        'pagination_options': pagination_options,
        'selected_bulk_operations': selected_bulk_operations,

        'page_title': f'Backlog Super Type Deleted List',
    }       
    template_file = f"{app_name}/{module_path}/list_deleted__backlog_super_types.html"
    return render(request, template_file, context)

# Create View
@login_required
def create_backlog_super_type(request, org_id):
    user = request.user
    # connect with connect id
    org = get_object_or_404(Organization, pk=org_id, **viewable_dict)
    if request.method == 'POST':
        form = BacklogSuperTypeForm(request.POST)
        if form.is_valid():
            form.instance.org_id = org_id
            form.instance.author = user
            super_type = form.save()
            
            # create content type
            content_type = BacklogType.objects.create(
                parent=None,
                org = org,
                name = super_type.name,
                super_type = super_type,
                author = user
            )
            content_type.save()
            # create content
            content = Backlog.objects.create(
                parent=None,
                org = org,
                name = super_type.name,
                type = content_type,
                author = user
            )
            content.save()
            print(f">>> === super_type: {super_type}{content_type}{content} === <<<")
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_backlog_super_types', org_id=org_id)
    else:
        form = BacklogSuperTypeForm()

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'create_super_type',
        'org_id': org_id,
        'org': org,
        'module_path': module_path,
        'form': form,
        'page_title': f'Create Backlog Super Type',
    }
    template_file = f"{app_name}/{module_path}/create__backlog_super_type.html"
    return render(request, template_file, context)


# Edit
@login_required
def edit_backlog_super_type(request, org_id , super_type_id):
    user = request.user
    # connect with connect id
    org = get_object_or_404(Organization, pk=org_id, **viewable_dict)
    object = get_object_or_404(BacklogSuperType, pk=super_type_id, active=True, **viewable_dict)
    if request.method == 'POST':
        form = BacklogSuperTypeForm(request.POST, instance=object)
        if form.is_valid():
            form.instance.author = user
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_backlog_super_types', org_id=org_id)
    else:
        form = BacklogSuperTypeForm(instance=object)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'edit_backlog_super_type',
        'org_id': org_id,
        'org': org,
        'module_path': module_path,
        'form': form,
        'object': object,
        'page_title': f'Edit Backlog Super Type',
    }
    template_file = f"{app_name}/{module_path}/edit__backlog_super_type.html"
    return render(request, template_file, context)



@login_required
def delete_backlog_super_type(request, org_id ,super_type_id):
    user = request.user
    # connect with connect id
    org = get_object_or_404(Organization, pk=org_id, **viewable_dict)
    object = get_object_or_404(BacklogSuperType, pk=super_type_id, active=True, **viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.save()
        return redirect('list_backlog_super_types', org_id=org_id)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'delete_backlog_super_type',
        'org_id': org_id,
        'org': org,
        'module_path': module_path,        
        'object': object,
        'page_title': f'Delete Backlog Super Type',
    }
    template_file = f"{app_name}/{module_path}/delete__backlog_super_type.html"
    return render(request, template_file, context)


@login_required
def permanent_deletion_backlog_super_type(request, org_id ,super_type_id):
    user = request.user
    # connect with connect id
    org = get_object_or_404(Organization, pk=org_id, **viewable_dict)
    object = get_object_or_404(BacklogSuperType, pk=super_type_id, active=False, 
                               deleted=False, **viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.deleted = True
        object.save()
        return redirect('list_backlog_super_types', org_id=org_id)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'permanent_deletion_backlog_super_type',
        'org_id': org_id,
        'org': org,
        'module_path': module_path,        
        'object': object,
        'page_title': f'Permanent Deletion Backlog Super Type',
    }
    template_file = f"{app_name}/{module_path}/permanent_deletion__backlog_super_type.html"
    return render(request, template_file, context)


@login_required
def restore_backlog_super_type(request, org_id, super_type_id):
    user = request.user
    # connect with connect id
    org = get_object_or_404(Organization, pk=org_id, **viewable_dict)
    object = get_object_or_404(BacklogSuperType, pk=super_type_id, active=False, **viewable_dict)
    object.active = True
    object.save()
    return redirect('list_backlog_super_types', org_id=org_id)
   


@login_required
def view_backlog_super_type(request,  org_id, super_type_id):
    user = request.user
    # connect with connect id
    org = get_object_or_404(Organization, pk=org_id, **viewable_dict)
    object = get_object_or_404(BacklogSuperType, pk=super_type_id, active=True, **viewable_dict)    

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'view_backlog_super_type',
        'org_id': org_id,
        'org': org,
        'module_path': module_path,
        'object': object,
        'page_title': f'View __displaymodelname__',
    }
    template_file = f"{app_name}/{module_path}/view__backlog_super_type.html"
    return render(request, template_file, context)


