from __appname__.mod_app.all_view_imports import *
from __appname__.mod___singularmodname__.models___singularmodname__ import *
from __appname__.mod___singularmodname__.forms___singularmodname__ import *

app_name = '__appname__'
app_version = 'v1'

module_name = '__modulename__'
module_path = f'__modulepath__'

# viewable flag
first_viewable_flag = '__ALL__'  # 'all' or '__OWN__'
viewable_flag = '__ALL__'  # 'all' or '__OWN__'
# Setup dictionaries based on flags
# viewable_dict = {} if viewable_flag == '__ALL__' else {'author': user}
# first_viewable_dict = {} if first_viewable_flag == '__ALL__' else {'author': user}

def get_viewable_dicts(user, viewable_flag, first_viewable_flag):
    viewable_dict = {} if viewable_flag == '__ALL__' else {'author': user}
    first_viewable_dict = {} if first_viewable_flag == '__ALL__' else {'author': user}
    return viewable_dict, first_viewable_dict
# ============================================================= #
@login_required
def list___pluralmodname__(request, parent_id):
    # take inputs
    ref_parent_id = parent_id
    parent_id = None if parent_id == 0 else parent_id
    viewable_dict, first_viewable_dict = get_viewable_dicts(request.user, 
                                viewable_flag, first_viewable_flag)
    parent = None
    ctypes = None
    if parent_id !=0 and parent_id is not None:
        parent = get_object_or_404(__modelname__, pk=parent_id, **viewable_dict)
        ctypes = __modelname__Type.objects.filter(pk=parent.type_id).order_by('position')
        print(f">>> === parent: {parent}:{ctypes} === <<<")
    # process inputs
    user = request.user       
    objects_count = 0    
    show_all = request.GET.get('all', '25')
    objects_per_page = int(show_all) if show_all != 'all' else 25
    pagination_options = [5, 10, 15, 25, 50, 100, 'all']
    selected_bulk_operations = None
    search_query = request.GET.get('search', '')
    deleted_count = 0
    
    # breadcrumbs 
    # Get the current content object if not at root
    current_content = None
    breadcrumbs = []
    if parent_id:
        current_content = get_object_or_404(__modelname__, pk=parent_id)
        breadcrumbs = list(current_content.get_ancestors(include_self=True))
        
    if search_query:
        tobjects = __modelname__.objects.filter(name__icontains=search_query, 
                                            parent_id=parent_id,
                                            active=True,deleted=False, **viewable_dict ).order_by('position')
        deleted = __modelname__.objects.filter(active=False, deleted=False,**viewable_dict).order_by('position')
        deleted_count = deleted.count()
    else:
        tobjects = __modelname__.objects.filter(active=True, parent_id=parent_id,**viewable_dict).order_by('position')
        deleted = __modelname__.objects.filter(active=False,  parent_id=parent_id, deleted=False,**viewable_dict).order_by('position')
        deleted_count = deleted.count()
    
    if show_all == 'all':
        # No pagination, show all records
        page_obj = tobjects
        objects_per_page = tobjects.count()
    else:
        #print(f">>> === show_all: {show_all} === <<<")   
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
                    object = get_object_or_404(__modelname__, pk=item, active=True, **viewable_dict)
                    object.active = False
                    object.save()
                    
                elif bulk_operation == 'bulk_done':
                    object = get_object_or_404(__modelname__, pk=item, active=True, **viewable_dict)
                    object.done = True
                    object.save()
                    
                elif bulk_operation == 'bulk_not_done':
                    object = get_object_or_404(__modelname__, pk=item, active=True, **viewable_dict)
                    object.done = False
                    object.save()
                    
                elif bulk_operation == 'bulk_blocked':  # Correct the operation check here
                    object = get_object_or_404(__modelname__, pk=item, active=True, **viewable_dict)
                    object.blocked = True
                    object.save()
                    
                else:
                    return redirect('list___pluralmodname__', parent_id=ref_parent_id)
            return redirect('list___pluralmodname__', parent_id=ref_parent_id)
    
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list___pluralmodname__',
        'ref_parent_id': ref_parent_id,  
        'parent': parent,
        'parent_id': parent_id,  
        'ctypes': ctypes,
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
        'breadcrumbs': breadcrumbs,
        'page_title': f'__displaymodulename__ List',
    }       
    template_file = f"{app_name}/{module_path}/list____pluralmodname__.html"
    return render(request, template_file, context)



# list the deleted objects
# ============================================================= #
@login_required
def list_deleted___pluralmodname__(request, parent_id):
    # take inputs
    ref_parent_id = parent_id
    parent_id = None if parent_id == 0 else parent_id
    viewable_dict, first_viewable_dict = get_viewable_dicts(request.user, 
                                viewable_flag, first_viewable_flag)
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
    
    # breadcrumbs 
    # Get the current content object if not at root
    current_content = None
    breadcrumbs = []
    if parent_id:
        current_content = get_object_or_404(__modelname__, pk=parent_id)
        breadcrumbs = list(current_content.get_ancestors(include_self=True))
    
    if search_query:
        tobjects = __modelname__.objects.filter(name__icontains=search_query, 
                                            parent_id=parent_id,
                                            **viewable_dict, active=False, deleted=False).order_by('position')
    else:
        tobjects = __modelname__.objects.filter(parent_id=parent_id, active=False, deleted=False, **viewable_dict).order_by('position')
    
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
                selected_items = request.POST.getlist('selected_item')  
                for item_id in selected_items:
                    item = int(item_id)  
                    if bulk_operation == 'bulk_restore':
                        object = get_object_or_404(__modelname__, pk=item, active=False, **viewable_dict)
                        object.active = True               
                        object.save()
                        print(f">>> === bulk_restore: {object}{object.active}{object.deleted} === <<<")
                    elif bulk_operation == 'bulk_erase':
                        object = get_object_or_404(__modelname__, pk=item, active=False, **viewable_dict)
                        object.active = False  
                        object.deleted = True             
                        object.save()
                        print(f">>> === bulk_erase: {object}{object.active}{object.deleted} === <<<")
                    else:
                        return redirect('list_deleted___pluralmodname__', parent_id=ref_parent_id)
                return redirect('list_deleted___pluralmodname__', parent_id=ref_parent_id)
    
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_deleted___pluralmodname__',
        'ref_parent_id': ref_parent_id,  
        'parent_id': parent_id,  
        'module_path': module_path,
        'user': user,
        'tobjects': tobjects,
        'page_obj': page_obj,
        'objects_count': objects_count,
        'objects_per_page': objects_per_page,
        'show_all': show_all,
        'pagination_options': pagination_options,
        'selected_bulk_operations': selected_bulk_operations,
        'breadcrumbs': breadcrumbs,
        'page_title': f'__displaymodulename__ List',
    }       
    template_file = f"{app_name}/{module_path}/list_deleted____pluralmodname__.html"
    return render(request, template_file, context)



# Create View
@login_required
def create___singularmodname__(request, parent_id):
    user = request.user
    ref_parent_id = parent_id
    parent_id = None if parent_id == 0 else parent_id
    viewable_dict, first_viewable_dict = get_viewable_dicts(request.user, 
                                viewable_flag, first_viewable_flag)
    stored_selected_id = None
    if request.method == 'POST':
        action = request.POST.get('action', None)
        if action == 'select_id':
            selected_id = request.POST.get('selected_id')
            request.session['selected_id'] = selected_id
            stored_selected_id = selected_id
            ctype = __modelname__Type.objects.get(pk=selected_id)
            print(f">>> === selected_id: {selected_id} === <<<")
            form = __modelname__Form(initial={'type': ctype})
            context = {
                'parent_page': '___PARENTPAGE___',
                'page': 'create___singularmodname__',
                'ref_parent_id': ref_parent_id,
                'parent_id': parent_id,
                'selected_id': selected_id,
                'ctype': ctype,
                'form': form,
                'page_title': f'Create __displaymodulename__',
            }
            template_file = f"{app_name}/{module_path}/create____singularmodname__.html"
            return render(request, template_file, context)
        
        elif action == 'create_content':
            form = __modelname__Form(request.POST)
            if form.is_valid():
                print(f">>> === stored id : {stored_selected_id} === <<<")
                selected_id = request.session.get('selected_id')
                request.session['selected_id'] = None
                form.instance.type_id = selected_id
                form.instance.parent_id = parent_id
                form.instance.author = user
                form.save()
                return redirect('list___pluralmodname__', parent_id=ref_parent_id)
            else:
                print(f">>> === form.errors: {form.errors} === <<<")
            
    # if request.method == 'POST':
    #     form = ContentForm(request.POST)
    #     if form.is_valid():
    #         form.instance.parent_id = parent_id
    #         form.instance.author = user
    #         form.save()
    #     else:
    #         print(f">>> === form.errors: {form.errors} === <<<")
    #     return redirect('list_contents', parent_id=ref_parent_id)
    else:
        form = ContentForm()

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'create___singularmodname__',
        'ref_parent_id': ref_parent_id,  
        'parent_id': parent_id,  
        'module_path': module_path,
        'form': form,
        'page_title': f'Create __displaymodulename__',
    }
    template_file = f"{app_name}/{module_path}/create____singularmodname__.html"
    return render(request, template_file, context) 


# Edit
@login_required
def edit___singularmodname__(request, parent_id,  content_id):
    user = request.user
    ref_parent_id = parent_id
    parent_id = None if parent_id == 0 else parent_id
    viewable_dict, first_viewable_dict = get_viewable_dicts(request.user, 
                                viewable_flag, first_viewable_flag)
    object = get_object_or_404(__modelname__, pk=content_id, active=True, **viewable_dict)
    if request.method == 'POST':
        form = __modelname__Form(request.POST, instance=object)
        if form.is_valid():
            form.instance.parent_id = parent_id
            form.instance.author = user
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list___pluralmodname__', parent_id=ref_parent_id)
    else:
        form = __modelname__Form(instance=object)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'edit___singularmodname__',
        'ref_parent_id': ref_parent_id,  
        'parent_id': parent_id,  
        'module_path': module_path,
        'form': form,
        'object': object,
        'page_title': f'Edit __displaymodulename__',
    }
    template_file = f"{app_name}/{module_path}/edit____singularmodname__.html"
    return render(request, template_file, context)



@login_required
def delete___singularmodname__(request, parent_id, content_id):
    user = request.user
    ref_parent_id = parent_id
    parent_id = None if parent_id == 0 else parent_id
    viewable_dict, first_viewable_dict = get_viewable_dicts(request.user, 
                                viewable_flag, first_viewable_flag)
    object = get_object_or_404(__modelname__, pk=content_id, active=True, **viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.save()
        return redirect('list___pluralmodname__', parent_id=ref_parent_id)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'delete___singularmodname__',
        'ref_parent_id': ref_parent_id,  
        'parent_id': parent_id,  
        'module_path': module_path,        
        'object': object,
        'page_title': f'Delete __displaymodulename__',
    }
    template_file = f"{app_name}/{module_path}/delete____singularmodname__.html"
    return render(request, template_file, context)


@login_required
def permanent_deletion___singularmodname__(request, parent_id, content_id):
    user = request.user
    ref_parent_id = parent_id
    parent_id = None if parent_id == 0 else parent_id
    viewable_dict, first_viewable_dict = get_viewable_dicts(request.user, 
                                viewable_flag, first_viewable_flag)
    object = get_object_or_404(__modelname__, pk=content_id, active=False, deleted=False, **viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.deleted = True
        object.save()
        return redirect('list___pluralmodname__', parent_id=ref_parent_id)
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'permanent_deletion___singularmodname__',
        'ref_parent_id': ref_parent_id,  
        'parent_id': parent_id,  
        'module_path': module_path,        
        'object': object,
        'page_title': f'Permanent Deletion __displaymodulename__',
    }
    template_file = f"{app_name}/{module_path}/permanent_deletion____singularmodname__.html"
    return render(request, template_file, context)


@login_required
def restore___singularmodname__(request, parent_id, content_id):
    user = request.user
    ref_parent_id = parent_id
    parent_id = None if parent_id == 0 else parent_id
    viewable_dict, first_viewable_dict = get_viewable_dicts(request.user, 
                                viewable_flag, first_viewable_flag)
    object = get_object_or_404(__modelname__, pk=content_id, active=False, **viewable_dict)
    object.active = True
    object.save()
    return redirect('list___pluralmodname__', parent_id=ref_parent_id)


@login_required
def view___singularmodname__(request, parent_id,  content_id):
    user = request.user
    ref_parent_id = parent_id
    parent_id = None if parent_id == 0 else parent_id
    viewable_dict, first_viewable_dict = get_viewable_dicts(request.user, 
                                viewable_flag, first_viewable_flag)
    object = get_object_or_404(__modelname__, pk=content_id, active=True, **viewable_dict)    

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'view___singularmodname__',
        'ref_parent_id': ref_parent_id,  
        'parent_id': parent_id,  
        'module_path': module_path,
        'object': object,
        'page_title': f'View __displaymodulename__',
    }
    template_file = f"{app_name}/{module_path}/view____singularmodname__.html"
    return render(request, template_file, context)


