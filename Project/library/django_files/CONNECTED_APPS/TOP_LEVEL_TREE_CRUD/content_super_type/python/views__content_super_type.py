
from __appname__.mod_app.all_view_imports import *
from __appname__.models_app.models___singularmodname__ import *
from __appname__.forms_app.forms___singularmodname__ import *
# import the other two models root/content, content types 
from __appname__.mod___lcsingularrootmodulename__.models___lcsingularrootmodulename__ import *
from __appname__.mod___rootmodulename___type.models___rootmodulename___type import *

app_name = '__appname__'
app_version = '__version__'

module_name = '__modulename__'
module_path = f'__modulepath__'

# viewable flag
first_viewable_flag = '__ALL__'  # 'all' or '__OWN__'
viewable_flag = '__ALL__'  # 'all' or '__OWN__'
# Setup dictionaries based on flags
viewable_dict = {} if viewable_flag == '__ALL__' else {'author': user}
first_viewable_dict = {} if first_viewable_flag == '__ALL__' else {'author': user}
# ============================================================= #
@login_required
def list___pluralmodname__(request):
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
        tobjects = __modelname__.objects.filter(name__icontains=search_query, 
                                            active=True,deleted=False, **viewable_dict ).order_by('position')
        deleted = __modelname__.objects.filter(active=False, deleted=False,**viewable_dict).order_by('position')
        deleted_count = deleted.count()
    else:
        tobjects = __modelname__.objects.filter(active=True).order_by('position')
        deleted = __modelname__.objects.filter(active=False, deleted=False,**viewable_dict).order_by('position')
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
                    return redirect('list___pluralmodname__')
            return redirect('list___pluralmodname__')
    
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list___pluralmodname__',
        
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

        'page_title': f'__displaymodulename__ List',
    }       
    template_file = f"{app_name}/{module_path}/list____pluralmodname__.html"
    return render(request, template_file, context)



# list the deleted objects
# ============================================================= #
@login_required
def list_deleted___pluralmodname__(request):
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
        tobjects = __modelname__.objects.filter(name__icontains=search_query, 
                                            **viewable_dict, active=False, deleted=False).order_by('position')
    else:
        tobjects = __modelname__.objects.filter(active=False, deleted=False, **viewable_dict).order_by('position')
    
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
                        object = get_object_or_404(__modelname__, pk=item, active=False, **viewable_dict)
                        object.active = True               
                        object.save()
                    elif bulk_operation == 'bulk_erase':
                        object = get_object_or_404(__modelname__, pk=item, active=False, **viewable_dict)
                        object.active = False  
                        object.deleted = True             
                        object.save()
                    else:
                        return redirect('list_deleted___pluralmodname__')
                return redirect('list_deleted___pluralmodname__')
    
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_deleted___pluralmodname__',
        
        'module_path': module_path,
        'user': user,
        'tobjects': tobjects,
        'page_obj': page_obj,
        'objects_count': objects_count,
        'objects_per_page': objects_per_page,
        'show_all': show_all,
        'pagination_options': pagination_options,
        'selected_bulk_operations': selected_bulk_operations,

        'page_title': f'__displaymodulename__ Deleted List',
    }       
    template_file = f"{app_name}/{module_path}/list_deleted____pluralmodname__.html"
    return render(request, template_file, context)

# Create View
@login_required
def create___singularmodname__(request):
    user = request.user
    
    if request.method == 'POST':
        form = __dbmodelnameprimary__SuperTypeForm(request.POST)
        if form.is_valid():
            form.instance.author = user
            super_type = form.save()
            
            # create content type
            content_type = __dbmodelnameprimary__Type.objects.create(
                parent=None,
                name = super_type.name,
                super_type = super_type,
                author = user
            )
            content_type.save()
            # create content
            content = __dbmodelnameprimary__.objects.create(
                parent=None,
                name = super_type.name,
                type = content_type,
                author = user
            )
            content.save()
            print(f">>> === super_type: {super_type}{content_type}{content} === <<<")
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list___pluralmodname__')
    else:
        form = __dbmodelnameprimary__SuperTypeForm()

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'create_super_type',
        
        'module_path': module_path,
        'form': form,
        'page_title': f'Create __displaymodulename__',
    }
    template_file = f"{app_name}/{module_path}/create____singularmodname__.html"
    return render(request, template_file, context)


# Edit
@login_required
def edit___singularmodname__(request, super_type_id):
    user = request.user
    
    object = get_object_or_404(__modelname__, pk=super_type_id, active=True, **viewable_dict)
    if request.method == 'POST':
        form = __dbmodelnameprimary__SuperTypeForm(request.POST, instance=object)
        if form.is_valid():
            form.instance.author = user
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list___pluralmodname__')
    else:
        form = __dbmodelnameprimary__SuperTypeForm(instance=object)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'edit___singularmodname__',
        
        'module_path': module_path,
        'form': form,
        'object': object,
        'page_title': f'Edit __displaymodulename__',
    }
    template_file = f"{app_name}/{module_path}/edit____singularmodname__.html"
    return render(request, template_file, context)



@login_required
def delete___singularmodname__(request, super_type_id):
    user = request.user
    
    object = get_object_or_404(__modelname__, pk=super_type_id, active=True, **viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.save()
        return redirect('list___pluralmodname__')

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'delete___singularmodname__',
        
        'module_path': module_path,        
        'object': object,
        'page_title': f'Delete __displaymodulename__',
    }
    template_file = f"{app_name}/{module_path}/delete____singularmodname__.html"
    return render(request, template_file, context)


@login_required
def permanent_deletion___singularmodname__(request, super_type_id):
    user = request.user
    
    object = get_object_or_404(__modelname__, pk=super_type_id, active=False, 
                               deleted=False, **viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.deleted = True
        object.save()
        return redirect('list___pluralmodname__')

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'permanent_deletion___singularmodname__',
        
        'module_path': module_path,        
        'object': object,
        'page_title': f'Permanent Deletion __displaymodulename__',
    }
    template_file = f"{app_name}/{module_path}/permanent_deletion____singularmodname__.html"
    return render(request, template_file, context)


@login_required
def restore___singularmodname__(request, super_type_id):
    user = request.user
    object = get_object_or_404(__modelname__, pk=super_type_id, active=False, **viewable_dict)
    object.active = True
    object.save()
    return redirect('list___pluralmodname__')
   


@login_required
def view___singularmodname__(request,  super_type_id):
    user = request.user
    
    object = get_object_or_404(__modelname__, pk=super_type_id, active=True, **viewable_dict)    

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'view___singularmodname__',
        
        'module_path': module_path,
        'object': object,
        'page_title': f'View __displaymodelname__',
    }
    template_file = f"{app_name}/{module_path}/view____singularmodname__.html"
    return render(request, template_file, context)


