from app_zweb1.views_zweb1.view_imports import *
from app_zweb1.models.models_personal_todolist import *
from app_zweb1.forms.form_personal_todolist import *
from app_zweb1.forms.form_treedb_and_typedb import *
from app_zweb1.forms.forms_personal_workspace import *
from app_zweb1.models.models_treedb_and_typedb import *
from app_zweb1.models.models_personal_workspace import *

app_name = 'app_zweb1'
app_version = 'v1'

@login_required
def ajax_update_wslist_done_state(request):
    if request.method == 'POST':
        user = request.user
        id = request.POST.get('id', None)
        done = request.POST.get('done', None)
        if id and done:
            todolist = TreeDB.objects.filter(id=id, author=user).first()
            if todolist:
                todolist.done = done.lower() == 'true'
                todolist.save()
                return JsonResponse({'success': True})      

    return JsonResponse({'success': False})


@login_required
def personal_workspace(request):
    # take inputs
    # process inputs
    user = request.user   
    objects_count = 0
    objects_per_page = 50
    search_query = request.GET.get('search', '')
    list_templates = request.GET.get('list_templates', 'hide')
    if search_query:
        workspaces = Workspace.objects.filter(name__icontains=search_query, author=user, template=False).order_by('position')
    else:
        if list_templates == "show":
            workspaces = Workspace.objects.filter(template=True, active=True, author=user).order_by('position')
        else:
            workspaces = Workspace.objects.filter(active=True, author=user, template=False).order_by('position')
    
    show_all = request.GET.get('all', 'false').lower() == 'true'
    if show_all:
        # No pagination, show all records
        page_obj = workspaces

    else:
        paginator = Paginator(workspaces, objects_per_page)  # Show 10 topics per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    
    objects_count = workspaces.count()
    ws_details = []
    for workspace in page_obj:
        map = WorkspaceMap.objects.filter(workspace=workspace, author=user).first()
        if map:
            treedb = map.treedb
            wslist = treedb.get_active_descendants().order_by('position')
            ws_completion_stats = treedb.get_completion_stats()
            ws_items = []
            for item in wslist:
                item_stats = item.get_completion_stats()
                ws_items.append({
                    'item': item,
                    'completion_stats': item_stats
                })
            ws_details.append({
                'workspace': workspace,
                'ws_completion_stats': ws_completion_stats,
                'ws_items': ws_items
            })

    # send outputs (info, template,
    context = {
        'parent_page': 'loggedin_home_page',
        'page': 'personal_workspace',
        'user': user,
        'workspaces': workspaces,
        'page_obj': page_obj,
        'objects_count': objects_count,
        'objects_per_page': objects_per_page,
        'show_all': show_all,
        'list_templates': list_templates,
        'ws_details': ws_details,
        'page_title': f'Personal Workspace',
    }       
    template_file = f"{app_name}/personal_workspace/ws/personal_workspace.html"
    return render(request, template_file, context)


@login_required
def internal_create_ws_map(request, workspace):
    user = request.user
    # NOTE: Parent = None for TreeDB root element
    treedb = TreeDB.objects.create(parent=None, name=workspace.name, 
                                    description=workspace.description, 
                                    author=user)
    treedb.save()
    map = WorkspaceMap.objects.create(workspace=workspace, treedb=treedb, author=user)
    map.save()
    return map, treedb

@login_required
def internal_copy_ws_template_items(request, template_id, workspace, dest_map, dest_treedb):
    src_ws = Workspace.objects.filter(id=template_id).first()
    src_map = WorkspaceMap.objects.filter(workspace=src_ws).first()
    src_treedb = src_map.treedb
    for item in src_treedb.get_active_descendants():
        TreeDB.objects.create(parent=dest_treedb, name=item.name, 
                              description=item.description, author=request.user)
    return True
# Create View
@login_required
def create_workspace(request):
    user = request.user
    templates = Workspace.objects.filter(template=True, active=True, author=user)
    if request.method == 'POST':
        form = WorkspaceForm(request.POST)
        if form.is_valid():
            template_id = request.POST.get('template', None)
            form.instance.author = user
            form.save()
            # any pre-processing for the todo list topic
            ## Create the Maping for the topic and tree todolist
            workspace = form.instance
            map, treedb = internal_create_ws_map(request, workspace)
            if template_id:
                internal_copy_ws_template_items(request, template_id, workspace, map, treedb)
            
            return redirect('personal_workspace')
    else:
        form = WorkspaceForm()

    context = {
        'parent_page': 'loggedin_home_page',
        'page': 'create_workspace',
        'form': form,
        'templates': templates,
        'page_title': f'Created Workspace',
    }
    template_file = f"{app_name}/personal_workspace/ws/create_workspace.html"
    return render(request, template_file, context)


# Edit View
@login_required
def edit_workspace(request, pk):
    user = request.user
    workspace = get_object_or_404(Workspace, pk=pk, author=user)
    if request.method == 'POST':
        form = WorkspaceForm(request.POST, instance=workspace)
        if form.is_valid():
            form.instance.author = user
            form.save()
            return redirect('personal_workspace')
    else:
        form = WorkspaceForm(instance=workspace)
    context = {
        'parent_page': 'loggedin_home_page',
        'page': 'edit_todolist_topic',
        'form': form,
        'workspace': workspace,
        'page_title': f'Edit Workspace',
    }
    template_file = f"{app_name}/personal_workspace/ws/edit_workspace.html"
    return render(request, template_file, context)

# View
@login_required
def view_workspace(request, pk):
    user = request.user
    workspace = get_object_or_404(Workspace, pk=pk, author=user)
    ws_details = []
    map = WorkspaceMap.objects.filter(workspace=workspace, author=user).first()
    if map:
        treedb = map.treedb
        ws_list = treedb.get_active_descendants().order_by('position')
        ws_completion_stats = treedb.get_completion_stats()
        ws_items = []
        for item in ws_list:
            item_stats = item.get_completion_stats()
            ws_items.append({
                'item': item,
                'completion_stats': item_stats
            })
        ws_details.append({
            'workspace': workspace,
            'ws_completion_stats': ws_completion_stats,
            'ws_items': ws_items
        })
    context = {
        'parent_page': 'loggedin_home_page',
        'page': 'view_workspace',
        'workspace': workspace,
        'ws_details': ws_details,
        'page_title': f'View Workspace',
    }
    template_file = f"{app_name}/personal_workspace/ws/view_workspace.html"
    return render(request, template_file, context)

# Delete View
@login_required
def delete_workspace(request, pk):
    user = request.user
    workspace = get_object_or_404(Workspace, pk=pk, author=user)
    if request.method == 'POST':
        workspace.active = False
        workspace.save()
        return redirect('personal_workspace')
    context = {
        'parent_page': 'loggedin_home_page',
        'page': 'delete_workspace',
        'workspace': workspace,
        'page_title': f'Delete Workspace',
    }
    template_file = f"{app_name}/personal_workspace/ws/delete_workspace.html"
    return render(request, template_file, context)

# Configure Kanban Board
@login_required
def configure_workspace(request, pk):
    user = request.user
    workspace = get_object_or_404(Workspace, pk=pk, author=user)
    
    context = {
        'parent_page': 'loggedin_home_page',
        'page': 'configure_workspace',
        'workspace': workspace,
        'page_title': f'Configure Workspace',
    }
    template_file = f"{app_name}/personal_workspace/ws/configure_workspace.html"
    return render(request, template_file, context)

# copy workspace
SHARE_USER_INFO = None
@login_required
def copy_workspace(request, pk):
    user = request.user
    workspace = get_object_or_404(Workspace, pk=pk, author=user)
    map = WorkspaceMap.objects.filter(workspace=workspace, author=user).first()
    treedb = map.treedb
    
    # clone the workspace first
    new_workspace = Workspace.objects.create(name=f"{workspace.name} - Copy", 
                                             description=workspace.description, 
                                             author=user)
    new_workspace.save()
    
    # clone the tree db given
    SHARE_USER_INFO = user
    fields_to_copy = ['name', 'description', 'type', 'position', 'author']  # Specify fields you want to copy
    cloned_treedb = clone_mptt_tree(TreeDB, treedb, fields=fields_to_copy)
    # print(f">>> === Original Tree: {treedb.id}  === <<<")
    # print(f">>> === Cloned Tree: {cloned_treedb.id} === <<<")

    # map the workspace to the new tree db
    new_map = WorkspaceMap.objects.create(workspace=new_workspace, treedb=cloned_treedb, author=user)
    new_map.save()
    # print(f">>> === Original Map: {map.id} === <<<")
    # print(f">>> === Original Workspace: {workspace.id} === <<<")
    # print(f">>> === Original Tree: {treedb.id} === <<<")
    
    # print(f">>> === New Map: {new_map.id} === <<<")
    # print(f">>> === New Workspace: {new_workspace.id} === <<<")
    # print(f">>> === New Tree: {cloned_treedb.id} === <<<")
    # print(f">>> === New Tree Name: {cloned_treedb.name} === <<<")
    # done
    
    return redirect('personal_workspace')
    
    
    # context = {
    #     'parent_page': 'loggedin_home_page',
    #     'page': 'copy_workspace',
    #     'workspace': workspace,
    #     'page_title': f'Copy Workspace',
    # }
    # template_file = f"{app_name}/personal_workspace/ws/personal_workspace.html"
    # return render(request, template_file, context)

############################################################################
# view workspace details

@login_required
def view_workspace_details(request, pk):
    # take inputs
    # process inputs
    user = request.user   
    workspace = None
    wslist = None
    objects_count = 0
    objects_per_page = 100
    search_query = request.GET.get('search', '')
    if search_query:
        workspace = Workspace.objects.filter(name__icontains=search_query, author=user).order_by('position')
    else:
        workspace = Workspace.objects.filter(active=True, author=user, id=pk).order_by('position').first()
        
    # todolist 
    map = None    
    treedb = None
    if workspace:
        map = WorkspaceMap.objects.filter(workspace=workspace, author=user).first()
        print(f">>> === Getting Map: {map} === <<<")
        treedb = map.treedb
        wslist = treedb.get_active_children().order_by('position')
        objects_count = wslist.count()
    show_all = request.GET.get('all', 'false').lower() == 'true'
    theme = request.GET.get('theme', map.ws_theme if map.ws_theme else 'default')
    if request.method == 'GET':
        if 'theme' in request.GET:
            map.ws_theme = theme
            map.save()
    if show_all:
        # No pagination, show all records
        page_obj = wslist
    else:
        paginator = Paginator(wslist, objects_per_page)  # Show 10 topics per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    
    ## processing add
    if request.method == 'POST':
        form = TreeDBForm(request.POST)
        if form.is_valid():
            form.instance.author = user
            form.instance.parent = treedb
            print(f">>> === {form.instance.done} === <<<")
            form.save()
            return redirect('view_workspace_details', pk=pk)
        else:
            print(f">>> === {form.errors} === <<<")
    else:
        form = TreeDBForm()            
    
    # send outputs (info, template,
    context = {
        'parent_page': 'loggedin_home_page',
        'page': 'view_workspace_details',
        'user': user,
        'workspace': workspace,
        'page_obj': page_obj,
        'objects_count': objects_count,
        'objects_per_page': objects_per_page,
        'show_all': show_all,
        'theme': theme,
        
        'map': map,
        'treedb': treedb,
        
        'page_title': f'Workspace Details',
    }       
    template_file = f"{app_name}/personal_workspace/ws/view_workspace_details.html"
    return render(request, template_file, context)


@login_required
def view_workspace_level(request, pk):
    # take inputs
    # process inputs
    user = request.user   
    workspace = None
    wslist = None
    objects_per_page = 100
    objects_count = 0
    theme = None
    parent = get_object_or_404(TreeDB, pk=pk, author=user)
    children = None 
    ancestors = None
    root = parent.get_root()
    root_workspace = None
    map = WorkspaceMap.objects.filter(treedb=root, author=user).first()
    if map:
        root_workspace = map.workspace
        theme = request.GET.get('theme', map.ws_theme if map.ws_theme else 'default')
    if not parent.is_leaf_node():
        children = parent.get_active_children()    
    if not children:
        ancestors = parent.get_ancestors()
        
    if children != None:
        for child in children:
            ancestors = child.get_ancestors()
            if ancestors:
                parent = ancestors[0]
    
    ## identify the workspace details
    ## Check whether an workspace item exists in treedb
    treedb = TreeDB.objects.filter(id=pk, author=user).first()
    workspace = treedb
    print(f">>> === Getting Tree: {treedb.id}:{treedb} === <<<")
    if treedb:
        wslist = treedb.get_active_children().order_by('position')
        objects_count = wslist.count()
        print(f">>> === Getting Tree wslist: {wslist} === <<<")
    show_all = request.GET.get('all', 'false').lower() == 'true'
   
    if show_all:
        # No pagination, show all records
        page_obj = wslist
    else:
        paginator = Paginator(wslist, objects_per_page)  # Show 10 topics per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    
    ## processing add
    if request.method == 'POST':
        form = TreeDBForm(request.POST)
        print(f">>> === Start processing === <<<")
        if form.is_valid():
            form.instance.author = user
            parent_id = request.POST.get('parent_id', None)
            form.instance.parent_id = parent_id
            form.save()
            return redirect('view_workspace_level', pk=pk)
        else:
            print(f">>> === {form.errors} === <<<")
    else:
        form = TreeDBForm()            
    # send outputs (info, template,
    context = {
        'parent_page': 'loggedin_home_page',
        'page': 'view_workspace_level',
        'user': user,
        'ancestors': ancestors,
        'theme': theme,
        'workspace': workspace,
        'wslist': wslist,
        'treedb': treedb,
        'root': root,
        'root_workspace': root_workspace,
        'form': form,
        'page_obj': page_obj,
        'objects_count': objects_count,
        'objects_per_page': objects_per_page,
        'show_all': show_all,
        'page_title': f'Workspace Level',
    }       
    template_file = f"{app_name}/personal_workspace/ws/view_workspace_level.html"
    return render(request, template_file, context)


# Delete To Do
@login_required
def edit_ws_item(request, pk):
    user = request.user
    ws_item = get_object_or_404(TreeDB, pk=pk, author=user)
    parent = ws_item.parent
    root = ws_item.get_root()
    map = WorkspaceMap.objects.filter(treedb=root, author=user).first()
    ws_details = None
    if map:
        ws_details = map.workspace
    form = None
    if request.method == 'POST':
        form = ListItemForm(request.POST, instance=ws_item)
        page_from = request.GET.get('page_from', None)
        if form.is_valid():
            form.instance.author = user
            form.save()
            print(f">>> === page_from {page_from} === <<<")
            if page_from == 'view_workspace_details':
                return redirect(page_from, pk=ws_details.id)
            return redirect(page_from, pk=pk)
    else:
        form = ListItemForm(instance=ws_item)
    context = {
        'parent_page': 'loggedin_home_page',
        'page': 'edit_ws_item',
        'ws_item': ws_item,
        'parent': parent,
        'workspace': root,
        'form': form,
        'page_title': f'Edit To Do Item',
    }
    template_file = f"{app_name}/personal_workspace/ws/edit_ws_item.html"
    return render(request, template_file, context)


# view list item
@login_required
def view_ws_item(request, pk):
    user = request.user
    ws_item = get_object_or_404(TreeDB, pk=pk, author=user)
    parent = ws_item.parent
    root = ws_item.get_root()
    map = WorkspaceMap.objects.filter(treedb=root, author=user).first()
    ws_root = None
    if map:
        ws_root = map.workspace
    ws_details = []
    ws_list = ws_item.get_active_descendants().order_by('position')
    ws_completion_stats = ws_item.get_completion_stats()
    ws_items = []
    for item in ws_list:
        item_stats = item.get_completion_stats()
        ws_items.append({
            'item': item,
            'completion_stats': item_stats
        })
    ws_details.append({
        'workspace': ws_item,
        'ws_completion_stats': ws_completion_stats,
        'ws_items': ws_items
    })
    context = {
        'parent_page': 'loggedin_home_page',
        'page': 'view_ws_item',
        'ws_details': ws_details,
        'ws_item': ws_item,
        'parent': parent,
        'workspace': ws_root,
        'page_title': f'View To Do Item',
    }
    template_file = f"{app_name}/personal_workspace/ws/view_ws_item.html"
    return render(request, template_file, context)

# view list item
@login_required
def delete_ws_item(request, pk):
    user = request.user
    ws_item = get_object_or_404(TreeDB, pk=pk, author=user)
    parent = ws_item.parent
    root = ws_item.get_root()
    map = WorkspaceMap.objects.filter(treedb=root, author=user).first()
    ws_details = None
    if map:
        ws_details = map.workspace
    page_from = request.GET.get('page_from', None)
    if request.method == 'POST':
        print(f">>> === Deleting {ws_item} === <<<")
        ws_item.active = False
        ws_item.save()
        if page_from == 'view_workspace_details':
            return redirect(page_from, pk=ws_details.id)
        return redirect(page_from, pk=pk)
    context = {
        'parent_page': 'loggedin_home_page',
        'page': 'delete_ws_item',
        'ws_item': ws_item,
        'parent': parent,
        'workspace': root,
        'page_from': page_from,
        'page_title': f'Delete To Do Item',
    }
    template_file = f"{app_name}/personal_workspace/ws/delete_ws_item.html"
    return render(request, template_file, context)




def build_serial_number_tree(node, current_path=[], serial_no=None):
    if serial_no is None:
        serial_no = defaultdict(int)  # Initializes serial numbers for each level

    # Determine current level from the current path length
    level = len(current_path)

    # Increment the serial number for the current depth
    serial_no[level] += 1

    # Generate the serial number string (e.g., "1.1.2")
    node_serial = '.'.join(map(str, current_path + [serial_no[level]]))

    # Store the node and its serial number
    result = [(node, node_serial)]

    # Reset lower level counts if moving to a new subsection
    child_levels = list(range(level + 1, max(serial_no.keys()) + 1))
    for l in child_levels:
        serial_no[l] = 0

    # Fetch children ordered by 'position'
    children = node.get_children().order_by('position')
    for child in children:
        result.extend(build_serial_number_tree(child, current_path + [serial_no[level]], serial_no))

    return result


# Function to fetch a node by ID and generate its subtree with serial numbers
def get_serialized_subtree_from_node(request, node_id):
    user = request.user
    try:
        node = TreeDB.objects.get(id=node_id, active=True, author=user)
        return build_serial_number_tree(node)
    except TreeDB.DoesNotExist:
        return []


@login_required
def view_workspace_tree(request, pk):
    # take inputs
    # process inputs
    user = request.user   
    workspace = None
    wslist = None
    objects_per_page = 100
    objects_count = 0
    
    parent = get_object_or_404(TreeDB, pk=pk, author=user)
    children = None 
    ancestors = None
    root = parent.get_root()
    root_workspace = None
    map = WorkspaceMap.objects.filter(treedb=root, author=user).first()
    if map:
        root_workspace = map.workspace
    
    if not parent.is_leaf_node():
        children = parent.get_active_children()    
    if not children:
        ancestors = parent.get_ancestors()
        
    if children != None:
        for child in children:
            ancestors = child.get_ancestors()
            if ancestors:
                parent = ancestors[0]
    
    ## identify the workspace details
    ## Check whether an workspace item exists in treedb
    treedb = TreeDB.objects.filter(id=pk, author=user).first()
    workspace = treedb
    #print(f">>> === Getting Tree: {treedb.id}:{treedb} === <<<")
    if treedb:
        wslist = treedb.get_active_children().order_by('position')
        objects_count = wslist.count()
        #print(f">>> === Getting Tree wslist: {wslist} === <<<")
    show_all = request.GET.get('all', 'false').lower() == 'true'
   
    if show_all:
        # No pagination, show all records
        page_obj = wslist
        serialized_nodes = get_serialized_subtree_from_node(request, pk)
    else:
        paginator = Paginator(wslist, objects_per_page)  # Show 10 topics per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        serialized_nodes = get_serialized_subtree_from_node(request, pk)
    
    ## processing add
    if request.method == 'POST':
        form = TreeDBForm(request.POST)
        #print(f">>> === Start processing === <<<")
        if form.is_valid():
            form.instance.author = user
            parent_id = request.POST.get('parent_id', None)
            form.instance.parent_id = parent_id
            form.save()
            return redirect('view_workspace_level', pk=pk)
        else:
            print(f">>> === {form.errors} === <<<")
    else:
        form = TreeDBForm()            
    # send outputs (info, template,
    context = {
        'parent_page': 'loggedin_home_page',
        'page': 'view_workspace_tree',
        'user': user,
        'ancestors': ancestors,
        'workspace': workspace,
        'wslist': wslist,
        'treedb': treedb,
        'root': root,
        'root_workspace': root_workspace,
        'serialized_nodes': serialized_nodes,
        'form': form,
        'page_obj': page_obj,
        'objects_count': objects_count,
        'objects_per_page': objects_per_page,
        'show_all': show_all,
        'page_title': f'Workspace Level',
    }       
    template_file = f"{app_name}/personal_workspace/ws/view_workspace_tree.html"
    return render(request, template_file, context)


# utility method 
from django.db import transaction
from mptt.models import MPTTModel

# def clone_mptt_instance(instance, parent=None, fields=None):
#     """
#     Clone an MPTT instance and all its descendants, with specified fields.
#     :param instance: The MPTT instance to be cloned.
#     :param parent: The parent instance for the new clone.
#     :param fields: List of fields to be copied.
#     :return: The new cloned instance.
#     """
#     if not instance.pk:
#         raise ValueError("Instance must be saved before it can be cloned.")
    
#     # Create a new instance of the same class
#     instance.pk = None
#     instance._state.adding = True
#     new_instance = instance.__class__()

#     # Copy specified fields
#     if fields is None:
#         fields = [field.name for field in instance._meta.fields if field.name not in ['id', 'lft', 'rght', 'tree_id', 'level', 'parent']]
#     for field in fields:
#         setattr(new_instance, field, getattr(instance, field))
    
#     new_instance.parent = parent
#     new_instance.save()

#     # Recursively clone child instances
#     for child in instance.children():
#         clone_mptt_instance(child, parent=new_instance, fields=fields)
    
#     return new_instance

# @transaction.atomic
# def clone_mptt_tree(root_instance, fields=None):
#     """
#     Initiates the cloning process for a root node and all its descendants, specifying fields to be copied.
#     :param root_instance: The root node of the MPTT tree to clone.
#     :param fields: List of fields to copy.
#     :return: The new root node of the cloned tree.
#     """
#     return clone_mptt_instance(root_instance, fields=fields)


def clone_mptt_instance(model_class, original_instance, parent=None, fields=None):
    """
    Clone an MPTT model instance without using direct instance copying.
    :param model_class: The class of the MPTT model to create a new instance from.
    :param original_instance: The instance to clone.
    :param parent: The parent instance for the new clone.
    :param fields: List of fields to be copied.
    :return: The new cloned instance.
    """
    # Ensure model_class is indeed a model class
    if not issubclass(model_class, MPTTModel):
        raise ValueError("model_class must be a subclass of MPTTModel")

    # Create a new instance of the model class
    new_instance = model_class()  
    
    # Determine which fields to copy if not specified
    if fields is None:
        fields = [field.name for field in original_instance._meta.fields
                  if field.name not in ['id', 'lft', 'rght', 'tree_id', 'level', 'parent']]
    
    # Explicitly set field values from original to new instance
    for field_name in fields:
        setattr(new_instance, field_name, getattr(original_instance, field_name))
    
    # Set parent for the new instance
    new_instance.parent = parent
    new_instance.save()

    # Recursively clone child instances
    for child in original_instance.get_children():
        clone_mptt_instance(model_class, child, parent=new_instance, fields=fields)
    
    return new_instance

@transaction.atomic
def clone_mptt_tree(model_class, root_instance, fields=None):
    """
    Initiates the cloning process for a root node and all its descendants using a model class.
    :param model_class: The MPTT model class for creating new instances.
    :param root_instance: The root node of the MPTT tree to clone.
    :param fields: List of fields to copy.
    :return: The new root node of the cloned tree.
    """
    return clone_mptt_instance(model_class, root_instance, fields=fields)
