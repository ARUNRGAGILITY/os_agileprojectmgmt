from app_zweb1.views_zweb1.view_imports import *
from app_zweb1.models.models_personal_todolist import *
from app_zweb1.forms.form_personal_todolist import *
from app_zweb1.forms.form_treedb_and_typedb import *
from app_zweb1.models.models_treedb_and_typedb import *

app_name = 'app_zweb1'
app_version = 'v1'

@login_required
def ajax_update_todolist_done_state(request):
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


# ============================================================= #
@login_required
def personal_todolist(request):
    # take inputs
    # process inputs
    user = request.user   
    objects_count = 0
    objects_per_page = 10
    search_query = request.GET.get('search', '')
    if search_query:
        topics = TodoListTopic.objects.filter(name__icontains=search_query, author=user, template=False).order_by('position')
    else:
        topics = TodoListTopic.objects.filter(active=True, author=user, template=False).order_by('position')
    
    show_all = request.GET.get('all', 'false').lower() == 'true'
    if show_all:
        # No pagination, show all records
        page_obj = topics

    else:
        paginator = Paginator(topics, objects_per_page)  # Show 10 topics per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    
    objects_count = topics.count()
    topic_details = []
    for topic in page_obj:
        map = TopicTodoListMap.objects.filter(topic=topic, author=user).first()
        if map:
            treedb = map.treedb
            todolist = treedb.get_active_descendants().order_by('position')
            topic_completion_stats = treedb.get_completion_stats()
            todo_items = []
            for item in todolist:
                item_stats = item.get_completion_stats()
                todo_items.append({
                    'item': item,
                    'completion_stats': item_stats
                })
            topic_details.append({
                'topic': topic,
                'topic_completion_stats': topic_completion_stats,
                'todo_items': todo_items
            })

    # send outputs (info, template,
    context = {
        'parent_page': 'loggedin_home_page',
        'page': 'personal_todolist',
        'user': user,
        'topics': topics,
        'page_obj': page_obj,
        'objects_count': objects_count,
        'objects_per_page': objects_per_page,
        'show_all': show_all,
        'topic_details': topic_details,
        'page_title': f'Personal To Do List',
    }       
    template_file = f"{app_name}/personal_todolist/personal_todolist.html"
    return render(request, template_file, context)

@login_required
def internal_create_map(request, topic):
    user = request.user
    # NOTE: Parent = None for TreeDB root element
    treedb = TreeDB.objects.create(parent=None, name=topic.name, 
                                    description=topic.description, 
                                    author=user)
    treedb.save()
    map = TopicTodoListMap.objects.create(topic=topic, treedb=treedb, author=user)
    map.save()
    return map, treedb

@login_required
def internal_copy_template_items(request, template_id, dest_topic, dest_map, dest_treedb):
    src_topic = TodoListTopic.objects.filter(id=template_id).first()
    src_map = TopicTodoListMap.objects.filter(topic=src_topic).first()
    src_treedb = src_map.treedb
    for item in src_treedb.get_active_descendants():
        TreeDB.objects.create(parent=dest_treedb, name=item.name, 
                              description=item.description, author=request.user)
    return True
# Create View
@login_required
def create_todolist_topic(request):
    user = request.user
    templates = TodoListTopic.objects.filter(template=True, active=True, author=user)
    if request.method == 'POST':
        form = TodoListTopicForm(request.POST)
        if form.is_valid():
            template_id = request.POST.get('template', None)
            form.instance.author = user
            form.save()
            # any pre-processing for the todo list topic
            ## Create the Maping for the topic and tree todolist
            topic = form.instance
            map, treedb = internal_create_map(request, topic)
            if template_id:
                internal_copy_template_items(request, template_id, topic, map, treedb)
            
            return redirect('personal_todolist')
    else:
        form = TodoListTopicForm()

    context = {
        'parent_page': 'loggedin_home_page',
        'page': 'create_todolist_topic',
        'form': form,
        'templates': templates,
        'page_title': f'Created Todo List Topic',
    }
    template_file = f"{app_name}/personal_todolist/create_todolist_topic.html"
    return render(request, template_file, context)

# Edit View
@login_required
def edit_todolist_topic(request, pk):
    user = request.user
    topic = get_object_or_404(TodoListTopic, pk=pk, author=user)
    if request.method == 'POST':
        form = TodoListTopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.instance.author = user
            form.save()
            return redirect('personal_todolist')
    else:
        form = TodoListTopicForm(instance=topic)
    context = {
        'parent_page': 'loggedin_home_page',
        'page': 'edit_todolist_topic',
        'form': form,
        'topic': topic,
        'page_title': f'Edit Todolist Topic',
    }
    template_file = f"{app_name}/personal_todolist/edit_todolist_topic.html"
    return render(request, template_file, context)

# View
@login_required
def view_todolist_topic(request, pk):
    user = request.user
    topic = get_object_or_404(TodoListTopic, pk=pk, author=user)
    topic_details = []
    map = TopicTodoListMap.objects.filter(topic=topic, author=user).first()
    if map:
        treedb = map.treedb
        todolist = treedb.get_active_descendants().order_by('position')
        topic_completion_stats = treedb.get_completion_stats()
        todo_items = []
        for item in todolist:
            item_stats = item.get_completion_stats()
            todo_items.append({
                'item': item,
                'completion_stats': item_stats
            })
        topic_details.append({
            'topic': topic,
            'topic_completion_stats': topic_completion_stats,
            'todo_items': todo_items
        })
    context = {
        'parent_page': 'loggedin_home_page',
        'page': 'view_todolist_topic',
        'topic': topic,
        'topic_details': topic_details,
        'page_title': f'View Todo List Topic',
    }
    template_file = f"{app_name}/personal_todolist/view_todolist_topic.html"
    return render(request, template_file, context)

# Delete View
@login_required
def delete_todolist_topic(request, pk):
    user = request.user
    topic = get_object_or_404(TodoListTopic, pk=pk, author=user)
    if request.method == 'POST':
        topic.active = False
        topic.save()
        return redirect('personal_todolist')
    context = {
        'parent_page': 'loggedin_home_page',
        'page': 'delete_todolist_topic',
        'topic': topic,
        'page_title': f'Delete Todo List Topic',
    }
    template_file = f"{app_name}/personal_todolist/delete_todolist_topic.html"
    return render(request, template_file, context)

# Configure Kanban Board
@login_required
def configure_todolist_topic(request, pk):
    user = request.user
    topic = get_object_or_404(TodoListTopic, pk=pk, author=user)
    
    context = {
        'parent_page': 'loggedin_home_page',
        'page': 'configure_todolist_topic',
        'topic': topic,
        'page_title': f'Configure To Do List Topic',
    }
    template_file = f"{app_name}/personal_todolist/configure_todolist_topic.html"
    return render(request, template_file, context)

# Copy View
# Configure Kanban Board
@login_required
def copy_todolist_topic(request, pk):
    user = request.user
    topic = get_object_or_404(TodoListTopic, pk=pk, author=user)
    
    context = {
        'parent_page': 'loggedin_home_page',
        'page': 'copy_todolist_topic',
        'topic': topic,
        'page_title': f'Copy To Do List Topic',
    }
    template_file = f"{app_name}/personal_todolist/copy_todolist_topic.html"
    return render(request, template_file, context)


################################################ TODO LIST ################################################

@login_required
def view_todolist(request, pk):
    # take inputs
    # process inputs
    user = request.user   
    topic = None
    todolist = None
    objects_per_page = 10
    search_query = request.GET.get('search', '')
    if search_query:
        topic = TodoListTopic.objects.filter(name__icontains=search_query, author=user).order_by('position')
    else:
        topic = TodoListTopic.objects.filter(active=True, author=user, id=pk).order_by('position').first()
        
    # todolist 
    map = None    
    treedb = None
    if topic:
        map = TopicTodoListMap.objects.filter(topic=topic, author=user).first()
        treedb = map.treedb
        todolist = treedb.get_active_descendants().order_by('position')
    objects_count = todolist.count()
    show_all = request.GET.get('all', 'false').lower() == 'true'
    theme = request.GET.get('theme', map.todolist_theme)
    if request.method == 'GET':
        if 'theme' in request.GET:
            map.todolist_theme = theme
            map.save()
    if show_all:
        # No pagination, show all records
        page_obj = todolist
    else:
        paginator = Paginator(todolist, objects_per_page)  # Show 10 topics per page
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
            return redirect('view_todolist', pk=pk)
        else:
            print(f">>> === {form.errors} === <<<")
    else:
        form = TreeDBForm()            
    
    # send outputs (info, template,
    context = {
        'parent_page': 'loggedin_home_page',
        'page': 'todolist',
        'user': user,
        'topic': topic,
        'page_obj': page_obj,
        'objects_count': objects_count,
        'objects_per_page': objects_per_page,
        'show_all': show_all,
        'theme': theme,
        
        'map': map,
        'treedb': treedb,
        
        'page_title': f'Personal To Do List',
    }       
    template_file = f"{app_name}/personal_todolist/view_todolist.html"
    return render(request, template_file, context)


# Delete To Do
@login_required
def edit_list_item(request, pk):
    user = request.user
    todolist = get_object_or_404(TreeDB, pk=pk, author=user)
    parent = todolist.parent
    map = TopicTodoListMap.objects.filter(treedb=parent).first()
    topic = map.topic
    form = None
    if request.method == 'POST':
        form = ListItemForm(request.POST, instance=todolist)
        if form.is_valid():
            form.instance.author = user
            form.save()
            return redirect('view_todolist', pk=topic.id)
    else:
        form = ListItemForm(instance=todolist)
    context = {
        'parent_page': 'loggedin_home_page',
        'page': 'edit_list_item',
        'todolist': todolist,
        'topic': topic,
        'form': form,
        'page_title': f'Edit To Do Item',
    }
    template_file = f"{app_name}/personal_todolist/edit_list_item.html"
    return render(request, template_file, context)


# view list item
@login_required
def view_list_item(request, pk):
    user = request.user
    todolist = get_object_or_404(TreeDB, pk=pk, author=user)
    parent = todolist.parent
    map = TopicTodoListMap.objects.filter(treedb=parent).first()
    topic = map.topic
    context = {
        'parent_page': 'loggedin_home_page',
        'page': 'view_list_item',
        'todolist': todolist,
        'topic': topic,
        'page_title': f'View To Do Item',
    }
    template_file = f"{app_name}/personal_todolist/view_list_item.html"
    return render(request, template_file, context)

# view list item
@login_required
def delete_list_item(request, pk):
    user = request.user
    todolist = get_object_or_404(TreeDB, pk=pk, author=user)
    parent = todolist.parent
    map = TopicTodoListMap.objects.filter(treedb=parent).first()
    topic = map.topic
    if request.method == 'POST':
        todolist.active = False
        todolist.save()
        return redirect('view_todolist', pk=topic.id)
    context = {
        'parent_page': 'loggedin_home_page',
        'page': 'delete_list_item',
        'todolist': todolist,
        'topic': topic,
        'page_title': f'Delete To Do Item',
    }
    template_file = f"{app_name}/personal_todolist/delete_list_item.html"
    return render(request, template_file, context)
   

# ============================================================= #
@login_required
def create_todolist_templates(request):
    # take inputs
    # process inputs
    user = request.user   
    objects_count = 0
    objects_per_page = 10
    search_query = request.GET.get('search', '')
    if search_query:
        topics = TodoListTopic.objects.filter(name__icontains=search_query, author=user, template=True).order_by('position')
    else:
        topics = TodoListTopic.objects.filter(active=True, author=user, template=True).order_by('position')
    
    show_all = request.GET.get('all', 'false').lower() == 'true'
    if show_all:
        # No pagination, show all records
        page_obj = topics

    else:
        paginator = Paginator(topics, objects_per_page)  # Show 10 topics per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    
    objects_count = topics.count()
    topic_details = []
    for topic in page_obj:
        map = TopicTodoListMap.objects.filter(topic=topic, author=user).first()
        if map:
            treedb = map.treedb
            todolist = treedb.get_active_descendants().order_by('position')
            topic_completion_stats = treedb.get_completion_stats()
            todo_items = []
            for item in todolist:
                item_stats = item.get_completion_stats()
                todo_items.append({
                    'item': item,
                    'completion_stats': item_stats
                })
            topic_details.append({
                'topic': topic,
                'topic_completion_stats': topic_completion_stats,
                'todo_items': todo_items
            })

    # send outputs (info, template,
    context = {
        'parent_page': 'loggedin_home_page',
        'page': 'create_todolist_templates',
        'user': user,
        'topics': topics,
        'page_obj': page_obj,
        'objects_count': objects_count,
        'objects_per_page': objects_per_page,
        'show_all': show_all,
        'topic_details': topic_details,
        'page_title': f'To Do List Templates',
    }       
    template_file = f"{app_name}/personal_todolist/create_todolist_templates.html"
    return render(request, template_file, context)



# Create View
@login_required
def create_template(request):
    user = request.user
    if request.method == 'POST':
        form = TodoListTopicForm(request.POST)
        if form.is_valid():
            form.instance.author = user
            form.instance.template = True
            form.save()
            # any pre-processing for the todo list topic
            ## Create the Maping for the topic and tree todolist
            topic = form.instance
            map, treedb = internal_create_map(request, topic)
            
            return redirect('create_todolist_templates')
    else:
        form = TodoListTopicForm()

    context = {
        'parent_page': 'loggedin_home_page',
        'page': 'create_template',
        'form': form,
        'page_title': f'Created Template',
    }
    template_file = f"{app_name}/personal_todolist/create_template.html"
    return render(request, template_file, context)

# Edit View
@login_required
def edit_template(request, pk):
    user = request.user
    topic = get_object_or_404(TodoListTopic, pk=pk, author=user)
    if request.method == 'POST':
        form = TodoListTopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.instance.author = user
            form.save()
            return redirect('create_todolist_templates')
    else:
        form = TodoListTopicForm(instance=topic)
    context = {
        'parent_page': 'loggedin_home_page',
        'page': 'edit_template',
        'form': form,
        'topic': topic,
        'page_title': f'Edit Template',
    }
    template_file = f"{app_name}/personal_todolist/edit_template.html"
    return render(request, template_file, context)

# View
@login_required
def view_template(request, pk):
    user = request.user
    topic = get_object_or_404(TodoListTopic, pk=pk, author=user)
   
    context = {
        'parent_page': 'loggedin_home_page',
        'page': 'view_template',
        'topic': topic,
        'page_title': f'View Template',
    }
    template_file = f"{app_name}/personal_todolist/view_template.html"
    return render(request, template_file, context)

# Delete View
@login_required
def delete_template(request, pk):
    user = request.user
    topic = get_object_or_404(TodoListTopic, pk=pk, author=user)
    if request.method == 'POST':
        topic.active = False
        topic.save()
        return redirect('create_todolist_templates')
    context = {
        'parent_page': 'loggedin_home_page',
        'page': 'delete_template',
        'topic': topic,
        'page_title': f'Delete Template',
    }
    template_file = f"{app_name}/personal_todolist/delete_template.html"
    return render(request, template_file, context)

# Edit View
@login_required
def copy_template(request, pk):
    user = request.user
    # Get the topic
    topic = get_object_or_404(TodoListTopic, pk=pk, author=user)
    topic_copy_name = f"{topic.name} - Copy"      
    # Get the Map
    map = TopicTodoListMap.objects.filter(topic=topic, author=user).first()    
    # Get the treedb
    treedb = map.treedb
    
    # Create a topic
    topic_copy = TodoListTopic.objects.create(name=topic_copy_name, 
                                              description=topic.description, 
                                              author=user, template=True)
    
    # Create a Map
    map_copy, treedb_copy = internal_create_map(request, topic_copy)
    # Create the TreeDB entries and map to the new topic
    for item in treedb.get_active_descendants():
        TreeDB.objects.create(parent=treedb_copy, name=item.name, 
                              description=item.description, author=user)
        
    # send the message to the page
    return redirect('create_todolist_templates')
    