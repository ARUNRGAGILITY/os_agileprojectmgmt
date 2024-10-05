from app_assessment.views_app.all_view_imports import *
from app_assessment.models_app.models_templates import *
from app_assessment.models_app.models_assessment_questions import *
from app_assessment.models_app.models_assessment_answers import *
from app_assessment.forms_app.forms_templates import *

app_name = 'app_assessment'
app_version = 'v1'

module_name = 'areas'

# ============================================================= #
@login_required
def list_areas(request, template_id):
    # take inputs
    # process inputs
    user = request.user   
    objects_count = 0
    objects_per_page = 50
    org_id = None
    template = AssessmentTemplates.objects.get(id=template_id, active=True)
    org_id = template.org_id
    org = Organization.objects.get(id=org_id, active=True)
    search_query = request.GET.get('search', '')
    if search_query:
        tobjects = AssessmentAreas.objects.filter(name__icontains=search_query, 
                                            template_id=template_id, author=user).order_by('position')
    else:
        tobjects = AssessmentAreas.objects.filter(active=True, template_id=template_id).order_by('position')
    
    show_all = request.GET.get('all', 'false').lower() == 'true'
    if show_all:
        # No pagination, show all records
        page_obj = tobjects

    else:
        paginator = Paginator(tobjects, objects_per_page)  # Show 10 tobjects per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    
    objects_count = tobjects.count()
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_areas',
        'template': template,
        'template_id': template_id,
        'org': org,
        'org_id': org_id,
        'user': user,
        'tobjects': tobjects,
        'page_obj': page_obj,
        'objects_count': objects_count,
        'objects_per_page': objects_per_page,
        'show_all': show_all,

        'page_title': f'Areas List',
    }       
    template_file = f"{app_name}/{module_name}/list_areas.html"
    return render(request, template_file, context)

# Create View
@login_required
def create_area(request, template_id):
    user = request.user
    template = AssessmentTemplates.objects.get(id=template_id, active=True)
    org_id = template.org_id
    org = Organization.objects.get(id=org_id, active=True)
    if request.method == 'POST':
        form = AssessmentAreasForm(request.POST)
        if form.is_valid():
            form.instance.author = user
            form.instance.template_id = template_id
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_areas', template_id=template_id)
    else:
        form = AssessmentAreasForm()

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'create_area',
        'template': template,
        'template_id': template_id,
        'org': org,
        'org_id': org_id,
        'form': form,
        'page_title': f'Create Area',
    }
    template_file = f"{app_name}/{module_name}/create_area.html"
    return render(request, template_file, context)



# Edit
@login_required
def edit_area(request, template_id, area_id):
    user = request.user
    template = AssessmentTemplates.objects.get(id=template_id, active=True)
    org_id = template.org_id
    org = Organization.objects.get(id=org_id, active=True)
    object = get_object_or_404(AssessmentAreas, pk=area_id, active=True)
    if request.method == 'POST':
        form = AssessmentAreasForm(request.POST, instance=object)
        if form.is_valid():
            form.instance.author = user
            form.instance.template_id = template_id
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_areas', template_id=template_id)
    else:
        form = AssessmentAreasForm(instance=object)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'edit_area',
        'template': template,
        'template_id': template_id,
        'org': org,
        'org_id': org_id,
        'form': form,
        'object': object,
        'page_title': f'Edit Area',
    }
    template_file = f"{app_name}/{module_name}/edit_area.html"
    return render(request, template_file, context)


@login_required
def delete_area(request, template_id, area_id):
    user = request.user
    template = AssessmentTemplates.objects.get(id=template_id, active=True)
    org_id = template.org_id
    org = Organization.objects.get(id=org_id, active=True)
    object = get_object_or_404(AssessmentAreas, pk=area_id, active=True)
    if request.method == 'POST':
        object.active = False
        object.save()
        return redirect('list_areas', template_id=template_id)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'delete_area',
        'template': template,
        'template_id': template_id,
        'org': org,
        'org_id': org_id,
        'object': object,
        'page_title': f'Delete Area',
    }
    template_file = f"{app_name}/{module_name}/delete_area.html"
    return render(request, template_file, context)

@login_required
def view_area(request, template_id, area_id):
    user = request.user
    template = AssessmentTemplates.objects.get(id=template_id, active=True)
    org_id = template.org_id
    org = Organization.objects.get(id=org_id, active=True)
    object = get_object_or_404(AssessmentAreas, pk=area_id, active=True)    

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'view_area',
        'template': template,
        'template_id': template_id,
        'org': org,
        'org_id': org_id,
        'object': object,
        'page_title': f'View Area',
    }
    template_file = f"{app_name}/{module_name}/view_area.html"
    return render(request, template_file, context)


# copy area
@login_required
def copy_area(request, template_id, area_id):
    # Fetch the original area
    original_area = get_object_or_404(AssessmentAreas, pk=area_id, active=True)
    print(f">>> === original_area: {original_area} === <<<")
    # Create a new area copying the original
    new_area = AssessmentAreas(
        # Copy relevant fields from the original area
        name=original_area.name + " (Copy)",  # Example to differentiate the name
        text=original_area.text,
        description=original_area.description,
        template=original_area.template,
        # Add more fields as necessary
        author=request.user  # or `original_area.author` if you want to keep the same author
    )
    new_area.save()
    print(f">>> === new_area: {new_area}:{new_area.active} === <<<")
    # Copy each question and its answers related to the original area
    questions = AssessmentQuestions.objects.filter(areas=original_area, active=True)
    for question in questions:
        new_question = AssessmentQuestions(
            areas=new_area,
            question_type=question.question_type,
            text=question.text,
            instructions=question.instructions,
            author=request.user  # or `question.author` if you want to keep the same author
        )
        new_question.save()
        print(f">>> === new_question: {new_question}:{new_question.active} === <<<")
        
        # Copy each answer related to the question
        answers = AssessmentAnswers.objects.filter(question=question, active=True)
        for answer in answers:
            AssessmentAnswers.objects.create(
                question=new_question,
                text=answer.text,
                is_correct=answer.is_correct,
                author=request.user  # or `answer.author` if you want to keep the same author
            )
            print(f">>> === answer: {answer.text}:{answer.active} === <<<")
    
    # Redirect to a new URL, for example, the detail view of the new area
    return redirect('list_areas', template_id=template_id)
