from app_zweb1.views_zweb1.view_imports import *
from app_zweb1.models.models_personal_kanban import *
from app_zweb1.forms.forms_personal_kanban import *

app_name = 'app_zweb1'
app_version = 'v1'

@login_required
def ajax_update_kanban_board_state(request):
    if request.method == 'POST':
        user = request.user
        cards = None
        print(f">>> === AJAX UPDATE KANBAN BOARD STATE:TEST_ITEM< === <<<")
        card_id = request.POST['card_id']
        state_id = request.POST['state_id']
        cards = json.loads(request.POST['cards'])        
        print(f">>> === CARDS:{cards} === <<<")
        card = Card.objects.get(pk=card_id, author=user)
        state = BoardState.objects.get(pk=state_id, author=user)

         # Using Django’s transaction.atomic to ensure data integrity
        from django.db import transaction
        with transaction.atomic():
            for card_data in cards:
                card = Card.objects.get(id=card_data['id'])
                card.position = card_data['position'] + 1
                card.state_id = state_id
                card.save()

        
        print(f">>> === >CARD:{card_id}{card}{state_id}{state}< === <<<")
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@login_required
def ajax_update_model_list_sorted(request):
    if request.method == 'POST':
        ajax_data = request.POST['sorted_list_data']
        model_name = request.POST['model_name']
        given_app_name = app_name
        if 'app_name' in request.POST:            
            given_app_name = request.POST['app_name']
        new_data = ajax_data.replace("[",'')
        new_data = new_data.replace("]",'')
        sorted_list = new_data.split(",")
        seq = 1
        
        #model_class = globals()[model_name]
        model_class = apps.get_model(given_app_name, model_name)
        print(f">>> === AJAX UPDATE SORTED === <<<")
        for item in sorted_list:
            str = item.replace('"','')
            position = str.split('_')
            print(f">>> === AJAX UPDATE SORTED {position} === <<<")
            model_class.objects.filter(pk=position[0]).update(position=seq, author=request.user)
            seq = seq + 1
        context = {'page': 'Sorted Value', 
                   'active_tab': 'sorted_value',
                   'ajax_data': ajax_data}
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


# ============================================================= #
@login_required
def personal_kanban(request):
    # take inputs
    # process inputs
    user = request.user   
    boards = KanbanBoard.objects.filter(active=True, author=user).order_by('position')
    objects_count = boards.count()
    objects_per_page = 10
    search_query = request.GET.get('search', '')
    if search_query:
        boards = KanbanBoard.objects.filter(name__icontains=search_query, author=user).order_by('position')
    else:
        boards = KanbanBoard.objects.filter(active=True, author=user).order_by('position')
    
    show_all = request.GET.get('all', 'false').lower() == 'true'
    if show_all:
        # No pagination, show all records
        page_obj = boards
    else:
        paginator = Paginator(boards, objects_per_page)  # Show 10 boards per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    # send outputs (info, template,
    context = {
        'parent_page': 'loggedin_home_page',
        'page': 'personal_kanban',
        'user': user,
        'boards': boards,
        'page_obj': page_obj,
        'objects_count': objects_count,
        'objects_per_page': objects_per_page,
        'show_all': show_all,
        
        'page_title': f'Personal Kanban',
    }       
    template_file = f"{app_name}/personal_kanban/personal_kanban.html"
    return render(request, template_file, context)

def internal_create_board_states(request,  board_id):
    user = request.user
    board = KanbanBoard.objects.get(pk=board_id, author=user)
    board_states = BoardState.objects.filter(board=board, author=user).order_by('position')
    count = board_states.count()
    if count == 0:
        board_states = BoardState.objects.create(board=board, name='Backlog', description='Backlog', exclude_wip_limit=True, position=1, author=user)
        BoardState.objects.create(board=board, name='To Do', description='To Do', wip_limit=1,position=2, author=user)
        BoardState.objects.create(board=board, name='In Progress', description='In Progress', wip_limit=1, position=3, author=user)
        BoardState.objects.create(board=board, name='Review', description='Review', position=4, author=user)
        BoardState.objects.create(board=board, name='Done', description='Done', exclude_wip_limit=True, done_column=True, position=5, author=user)
    
    return board_states

# Create View
@login_required
def create_kanban_board(request):
    user = request.user
    if request.method == 'POST':
        form = KanbanBoardForm(request.POST)
        if form.is_valid():
            form.instance.author = user
            form.save()
            internal_create_board_states(request, form.instance.id)
            return redirect('personal_kanban')
    else:
        form = KanbanBoardForm()

    context = {
        'parent_page': 'personal_kanban',
        'page': 'create_kanban_board',
        'form': form,
        'page_title': f'Created Kanban Board',
    }
    template_file = f"{app_name}/personal_kanban/create_kanban_board.html"
    return render(request, template_file, context)

# Edit View
@login_required
def edit_kanban_board(request, pk):
    user = request.user
    board = get_object_or_404(KanbanBoard, pk=pk, author=user)
    if request.method == 'POST':
        form = KanbanBoardForm(request.POST, instance=board)
        if form.is_valid():
            form.instance.author = user
            form.save()
            return redirect('personal_kanban')
    else:
        form = KanbanBoardForm(instance=board)
    context = {
        'parent_page': 'loggedin_home_page',
        'page': 'add_kanban_board',
        'form': form,
        'board': board,
        'page_title': f'Edit Kanban Board',
    }
    template_file = f"{app_name}/personal_kanban/edit_kanban_board.html"
    return render(request, template_file, context)

# View
@login_required
def view_kanban_board(request, pk):
    user = request.user
    board = get_object_or_404(KanbanBoard, pk=pk, author=user)
    board_states = BoardState.objects.filter(board=board, author=user).order_by('position')
    
    context = {
        'parent_page': 'loggedin_home_page',
        'page': 'view_kanban_board',
        'board': board,
        'board_states': board_states,
        'page_title': f'View Kanban Board',
    }
    template_file = f"{app_name}/personal_kanban/view_kanban_board.html"
    return render(request, template_file, context)

# Delete View
@login_required
def delete_kanban_board(request, pk):
    user = request.user
    board = get_object_or_404(KanbanBoard, pk=pk, author=user)
    if request.method == 'POST':
        # board.delete()
        board.active = False
        board.save()
        return redirect('personal_kanban')
    context = {
        'parent_page': 'loggedin_home_page',
        'page': 'delete_kanban_board',
        'board': board,
        'page_title': f'Delete Kanban Board',
    }
    template_file = f"{app_name}/personal_kanban/delete_kanban_board.html"
    return render(request, template_file, context)


def internal_get_default_state_id(request, board, default_state):
    user = request.user
    backlog_state = BoardState.objects.get(board=board, name='Backlog', author=user)
    return backlog_state.id
# addition

################ INTERNAL #################
# find and fill
def fill_missing_entries(request, board_id):
    missing_dates = find_missing_entries(request, board_id)
    if not missing_dates:
        print("No missing dates to fill.")
        return

    # Sort missing dates to handle them in sequence
    missing_dates.sort()

    # Check for data before the first missing date
    first_missing_date = missing_dates[0]
    last_missing_date = missing_dates[-1]

    # Find entries from the closest date before the first missing date
    entry_before = CardStateCount.objects.filter(
        date__lt=first_missing_date, 
        vstate__board__id=board_id
    ).order_by('-date').first()

    # Find entries from the closest date after the last missing date if no previous entries are found
    if entry_before:
        source_date = entry_before.date
    else:
        entry_after = CardStateCount.objects.filter(
            date__gt=last_missing_date, 
            vstate__board__id=board_id
        ).order_by('date').first()
        if entry_after:
            source_date = entry_after.date
        else:
            print("No entries available to copy from.")
            return

    # Retrieve all entries from the source date
    source_entries = CardStateCount.objects.filter(date=source_date, vstate__board__id=board_id)

    # Fill in missing dates with data from all source entries
    for date in missing_dates:
        for entry in source_entries:
            CardStateCount.objects.update_or_create(
                vstate=entry.vstate,
                date=date,
                defaults={'vcount': entry.vcount}
            )
            print(f"Filled date {date} for state {entry.vstate} with count {entry.vcount} from {source_date}")

# CFD generation 
def random_color():
    #return f"rgba({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)}, 0.5)"
    return f"rgba({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)}, _opacity_)"

@login_required
def generate_cfd(request, board_id):
    user = request.user
    board = KanbanBoard.objects.get(pk=board_id, author=user)
    
    update_card_state_counts(request, board_id)
    
    end_date = timezone.localdate()
    start_date = end_date - timedelta(days=30)

    board_states = BoardState.objects.filter(board__id=board_id, active=True).order_by('position')  # Ensure states are ordered
    board_states_count = board_states.count()
    date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]
    labels = [date.strftime('%b %d') for date in date_range]

    # Prepare a dictionary to hold total counts for each date
    total_counts_per_date = {date: 0 for date in date_range}

    # First calculate total counts from all states per date
    for state in board_states:
        for date in date_range:
            day_count = CardStateCount.objects.filter(vstate=state, date=date).aggregate(Sum('vcount')).get('vcount__sum') or 0
            total_counts_per_date[date] += day_count

    datasets = []
    order_counter = board_states_count  
    opacity_counter = 0.1
    for state in board_states:
        state_counts = []
        cumulative_count = 0
        if state.position == 1:  # Assuming position 0 is Backlog
            # Backlog state takes the total count of all cards from other states
            for date in date_range:
                state_counts.append(total_counts_per_date[date])
        else:
            # Normal cumulative count for other states
            for date in date_range:
                day_count = CardStateCount.objects.filter(vstate=state, date=date).aggregate(Sum('vcount')).get('vcount__sum') or 0
                cumulative_count += day_count
                state_counts.append(cumulative_count)

        color = random_color().replace('_opacity_', str(opacity_counter))
        datasets.append({
            'label': state.name,
            'data': state_counts,
            'backgroundColor': color,
            'borderColor': color,
            'borderWidth': 1,
            'fill': True,
            'order': order_counter,
        })
        order_counter -= 1
        opacity_counter += 0.1

    labels_json = json.dumps(labels)
    datasets_json = json.dumps(datasets)

    # send outputs (info, template,
    context = {
        'parent_page': 'loggedin_home_page',
        'page': 'generate_cfd',
        'user': user,
        'board': board,

        'labels': labels_json,
        'datasets': datasets_json,
        
        'page_title': f'Board States or Columns',
    }       
    template_file = f"{app_name}/personal_kanban/generate_cfd.html"
    return render(request, template_file, context)

# Make sure to include an appropriate view URL and template path

# backdate incomplete to complete
@login_required
def find_missing_entries(request, board_id):
    today = timezone.localdate()
    ten_days_ago = today - timedelta(days=10)

    # Create a list of all dates from ten days ago to yesterday
    all_dates = [ten_days_ago + timedelta(days=x) for x in range((today - ten_days_ago).days)]

    # Fetch all entries for these dates for the specified board
    existing_dates = CardStateCount.objects.filter(
        date__range=(ten_days_ago, today), 
        vstate__board__id=board_id
    ).dates('date', 'day')

    # Convert QuerySet of dates to a list
    existing_dates = list(existing_dates)

    # Find which dates are missing entries
    missing_dates = [date for date in all_dates if date not in existing_dates]

    print("All dates checked:", all_dates)
    print("Existing entries found for dates:", existing_dates)
    print("Missing dates with no entries:", missing_dates)
    
    return missing_dates

# backdate main
# this is to help a CFD check
@login_required
def daily_update_card_state_counts(request, board_id):
    #find_missing_entries(request, board_id)
    fill_missing_entries(request, board_id)  # Assume 123 is your board_id
    #generate_cfd(request, board_id)

################ INTERNAL #################
@login_required
def update_card_state_counts(request, board_id, date=None):
    user = request.user
    if date is None:
        date = timezone.localdate()
    board = KanbanBoard.objects.get(pk=board_id, active=True, author=user)
    today = timezone.localdate()
    states = BoardState.objects.filter(active=True, board=board)  # Assuming you have a model for CardState
    for state in states:
        count = state.state_cards.count()  # Assuming a ForeignKey from Card to CardState
        obj, created = CardStateCount.objects.update_or_create(
            vstate=state, 
            date=date, 
            defaults={'vcount': count}
        )



# Visuzalize Kanban workflow 
@login_required
def visualize_kanban_workflow(request, pk):
    user = request.user
    board = get_object_or_404(KanbanBoard, pk=pk, author=user)
    board_states = BoardState.objects.filter(board=board, author=user).order_by('position')
    default_state = 'Backlog'
    default_state_id = internal_get_default_state_id(request, board, default_state)
    
    cards = Card.objects.filter(board=board, author=user).order_by('position')
    
    board_states = BoardState.objects.prefetch_related('state_cards').filter(board=board, author=user).order_by('position')
    # You cannot assign directly, so we prepare data to send to template without modification of the original queryset
    board_states_data = [
        {
            'state': state,
            'cards': state.state_cards.filter(board=board, active=True, author=user).order_by('position'),
            'card_count': state.state_cards.filter(board=board, active=True, author=user).count(),  # Counting cards
        }
        for state in board_states
    ]    
    
    ## special  / important
    update_card_state_counts(request, pk)
    ## backdate the updates if necessary
    # ==> latest TODOFIX 28052024 #  daily_update_card_state_counts(request, pk)
    
    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():
            form.instance.board_id = pk
            form.instance.state_id = default_state_id
            form.instance.author = user
            form.save()
            # update the cardstaterecords
            CardStateRecord.objects.create(card=form.instance, state_id=default_state_id)
            return redirect('visualize_kanban_workflow', pk=pk)
        else:
            print(f">>> === FORM INVALID {form.errors} === <<<")
    else:
        form = CardForm()
    context = {
        'parent_page': 'loggedin_home_page',
        'page': 'visualize_kanban_workflow',
        'form': form,
        'board': board,
        'board_states': board_states,
        'cards': cards,
        'board_states_data': board_states_data,
        
        'page_title': f'Visualize Kanban Workflow',
    }
    template_file = f"{app_name}/personal_kanban/visualize_kanban_workflow.html"
    return render(request, template_file, context)
## ====================================== Board configuration ==================================== #
# Configure Kanban Board
@login_required
def configure_kanban_board(request, pk):
    user = request.user
    board = get_object_or_404(KanbanBoard, pk=pk, author=user)
    
    context = {
        'parent_page': 'loggedin_home_page',
        'page': 'configure_kanban_board',
        'board': board,
        'page_title': f'Configure Kanban Board',
    }
    template_file = f"{app_name}/personal_kanban/configure_kanban_board.html"
    return render(request, template_file, context)

# ====================================== BOARD STATE ==================================== #
@login_required
def board_states(request, board_id):
    # take inputs
    # process inputs
    user = request.user   
    board = KanbanBoard.objects.get(pk=board_id, author=user)
    board_states = BoardState.objects.filter(active=True, board=board, author=user).order_by('position')
    objects_count = board_states.count()
    objects_per_page = 12
    search_query = request.GET.get('search', '')
    if search_query:
        board_states = BoardState.objects.filter(name__icontains=search_query, board=board, author=user).order_by('position')
    else:
        board_states = BoardState.objects.filter(active=True, board=board, author=user).order_by('position')
    
    show_all = request.GET.get('all', 'false').lower() == 'true'
    if show_all:
        # No pagination, show all records
        page_obj = board_states
    else:
        paginator = Paginator(board_states, objects_per_page)  # Show 10 boards per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    # send outputs (info, template,
    context = {
        'parent_page': 'loggedin_home_page',
        'page': 'board_states',
        'user': user,
        'board': board,
        'board_states': board_states,
        'page_obj': page_obj,
        'objects_count': objects_count,
        'objects_per_page': objects_per_page,
        'show_all': show_all,
        
        'page_title': f'Board States or Columns',
    }       
    template_file = f"{app_name}/personal_kanban/board_states.html"
    return render(request, template_file, context)

# Create View
@login_required
def create_board_state(request, board_id):
    user = request.user
    board = KanbanBoard.objects.get(pk=board_id, author=user)
    if request.method == 'POST':
        form = BoardStateForm(request.POST)
        if form.is_valid():
            form.instance.board_id = board_id
            form.instance.author = user
            form.save()
            return redirect('board_states', board_id=board_id)
    else:
        form = BoardStateForm()
    context = {
        'parent_page': 'loggedin_home_page',
        'page': 'board_states',
        'user': user,
        'form': form,
        'board': board,
        
        'page_title': f'Create Board State',
    }       
    template_file = f"{app_name}/personal_kanban/create_board_state.html"
    return render(request, template_file, context)
# Edit View
@login_required
def edit_board_state(request, pk, board_id):
    user = request.user
    board = KanbanBoard.objects.get(pk=board_id, author=user)
    state = get_object_or_404(BoardState, pk=pk, author=user)
    if request.method == 'POST':
        form = BoardStateForm(request.POST, instance=state)
        if form.is_valid():
            form.instance.board_id = board_id
            form.instance.author = user
            form.save()
            return redirect('board_states', board_id=board_id)
    else:
        form = BoardStateForm(instance=state)
    context = {
        'parent_page': 'loggedin_home_page',
        'page': 'edit_board_state',
        'user': user,
        'board': board,
        'form': form,
        'page_title': f'Edit Board State',
    }       
    template_file = f"{app_name}/personal_kanban/create_board_state.html"
    return render(request, template_file, context)
# View
@login_required
def view_board_state(request, pk, board_id):
    user = request.user
    board = KanbanBoard.objects.get(pk=board_id, author=user)
    state = get_object_or_404(BoardState, pk=pk, author=user)
    
    context = {
        'parent_page': 'loggedin_home_page',
        'page': 'view_board_state',
        'user': user,
        'state': state,
        'board': board,
        'page_title': f'View Board State',
    }       
    template_file = f"{app_name}/personal_kanban/view_board_state.html"
    return render(request, template_file, context)

# Delete View
@login_required
def delete_board_state(request, pk, board_id):
    user = request.user
    board = KanbanBoard.objects.get(pk=board_id, author=user)
    state = get_object_or_404(BoardState, pk=pk, author=user)
    if request.method == 'POST':
        # state.delete()
        state.active = False
        state.save()
        return redirect('board_states', board_id=board_id)
    context = {
        'parent_page': 'loggedin_home_page',
        'page': 'delete_board_state',
        'user': user,
        'state': state,
        'board': board,
        'page_title': f'Delete Board State',
    }       
    template_file = f"{app_name}/personal_kanban/delete_board_state.html"
    return render(request, template_file, context)


###


# this is internally called function
def plot_cfd(request, board_id):
    user = request.user
    records = CardStateRecord.objects.filter(card__board_id=board_id, author=user).select_related('state').order_by('start_timestamp')
    data = [{'state': record.state.name, 'timestamp': record.start_timestamp.date()} for record in records]
    df = pd.DataFrame(data)
    df['count'] = 1

    pivot_df = df.pivot_table(index='timestamp', columns='state', values='count', aggfunc='sum').fillna(0).cumsum()

    # Create a BytesIO buffer to save image
    buffer = BytesIO()
    pivot_df.plot(kind='area', stacked=True)
    plt.title('Cumulative Flow Diagram')
    plt.xlabel('Date')
    plt.ylabel('Number of Cards')
    plt.savefig(buffer, format='png')
    plt.close()

    # Encode the image to base64 string
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()

    return graph

def CFD_Chart(request, board_id):
    user = request.user
    records = CardStateRecord.objects.filter(card__board_id=board_id, author=user).select_related('state').order_by('start_timestamp')
    data = [{'state': record.state.name, 'timestamp': record.start_timestamp.date()} for record in records]
    df = pd.DataFrame(data)
    df['count'] = 1

    pivot_df = df.pivot_table(index='timestamp', columns='state', values='count', aggfunc='sum').fillna(0).cumsum()

    # Convert the pivot table to a format suitable for Chart.js
    result = {
        'labels': pivot_df.index.tolist(),
        'datasets': []
    }

    for state in pivot_df.columns:
        result['datasets'].append({
            'label': state,
            'data': pivot_df[state].tolist(),
            'fill': 'start'  # Chart.js area fill
        })
    cfd_data_json = json.dumps(result, cls=DjangoJSONEncoder)
    result = cfd_data_json
    return result


# every minute test cfd chart
def TEST_CFD_Chart(request, board_id):
    user = request.user
    records = CardStateRecord.objects.filter(card__board_id=board_id, author=user).select_related('state').order_by('start_timestamp')
    data = [{'state': record.state.name, 'timestamp': record.start_timestamp} for record in records]
    df = pd.DataFrame(data)
    df['count'] = 1

    # Set the timestamp as the index and resample by minute
    df.set_index('timestamp', inplace=True)
    df = df.resample('T').sum().fillna(0)  # 'T' is the offset alias for minute
    pivot_df = df.pivot_table(columns='state', values='count', aggfunc='sum').fillna(0).cumsum()

    # Convert the pivot table to a format suitable for Chart.js
    result = {
        'labels': [str(index) for index in pivot_df.index],  # Convert timestamps to string
        'datasets': []
    }

    for state in pivot_df.columns:
        result['datasets'].append({
            'label': state,
            'data': pivot_df[state].tolist(),
            'fill': 'start'  # Chart.js area fill
        })
    cfd_data_json = json.dumps(result, cls=DjangoJSONEncoder)
    result = cfd_data_json
    return result

# color approach
def CFD_Chart_Color(request, board_id):
    user = request.user
    records = CardStateRecord.objects.filter(card__board_id=board_id, author=user).select_related('state').order_by('start_timestamp')
    data = [{'state': record.state.name, 'timestamp': record.start_timestamp} for record in records]
    df = pd.DataFrame(data)
    df['count'] = 1

    df.set_index('timestamp', inplace=True)
    df = df.resample('T').sum().fillna(0)  # 'T' is the offset alias for minute
    pivot_df = df.pivot_table(columns='state', values='count', aggfunc='sum').fillna(0).cumsum()

    # Define colors for each state, ensure there are enough colors for the states
    colors = [
        "#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF",
        "#FF9F40", "#66FF66", "#C9CBCF", "#FF6384", "#36A2EB"
    ]
    color_background = [f'rgba({int(c[1:3], 16)}, {int(c[3:5], 16)}, {int(c[5:], 16)}, 0.2)' for c in colors]
    color_border = [f'rgba({int(c[1:3], 16)}, {int(c[3:5], 16)}, {int(c[5:], 16)}, 1)' for c in colors]

    result = {
        'labels': [str(index) for index in pivot_df.index],  # Convert timestamps to string
        'datasets': []
    }

    for i, state in enumerate(pivot_df.columns):
        result['datasets'].append({
            'label': state,
            'data': pivot_df[state].tolist(),
            'backgroundColor': color_background[i % len(color_background)],
            'borderColor': color_border[i % len(color_border)],
            'fill': 'start'
        })

    cfd_data_json = json.dumps(result, cls=DjangoJSONEncoder)
    result = cfd_data_json
    return result


@login_required
def display_cfd(request, board_id):
    user = request.user
    board = KanbanBoard.objects.get(pk=board_id, author=user)
   
    # chart js
    #result = CFD_Chart(request, board_id)
    result = CFD_Chart(request, board_id)
    
    # send outputs (info, template,
    context = {
        'parent_page': 'personal_kanban',
        'page': 'display_cfd',
        'user': user,        
        'board': board,
        'cfd_data': result,
        
        'page_title': f'Display CFD',
    }       
    template_file = f"{app_name}/personal_kanban/display_cfd.html"
    return render(request, template_file, context)



############################################################################################################
# CARD related services
@login_required
def view_card(request, pk):
    user = request.user
    card = get_object_or_404(Card, pk=pk, author=user)
    context = {
        'parent_page': 'loggedin_home_page',
        'page': 'view_card',
        'card': card,
        'page_title': f'View Kanban Card',
    }
    template_file = f"{app_name}/personal_kanban/view_card.html"
    return render(request, template_file, context)

# Edit Card
@login_required
def edit_card(request, pk):
    user = request.user
    card = get_object_or_404(Card, pk=pk, author=user)
    board = card.board
    if request.method == 'POST':
        form = CardForm(request.POST, instance=card)
        if form.is_valid():
            form.instance.author = user
            form.save()
            return redirect('visualize_kanban_workflow', pk=board.id)
        else:
            print(f">>> === FORM INVALID {form.errors} === <<<")
    else:
        form = CardForm(instance=card)
    context = {
        'parent_page': 'loggedin_home_page',
        'page': 'edit_card',
        'form': form,
        'card': card,
        'board': board,
        'page_title': f'Edit Kanban Card',
    }
    template_file = f"{app_name}/personal_kanban/edit_card.html"
    return render(request, template_file, context)

# Delete Card
@login_required
def delete_card(request, pk):
    user = request.user
    card = get_object_or_404(Card, pk=pk, author=user)
    if request.method == 'POST':
        # board.delete()
        card.active = False
        card.save()
        return redirect('visualize_kanban_workflow', pk=card.board.id)
    context = {
        'parent_page': 'loggedin_home_page',
        'page': 'delete_card',
        'card': card,
        'page_title': f'Delete Kanban Card',
    }
    template_file = f"{app_name}/personal_kanban/delete_card.html"
    return render(request, template_file, context)
