
from app_assessment.views_app.all_view_imports import *
from app_assessment.models_app.models_templates import *
from app_assessment.models_app.models_assessment_questions import *
from app_assessment.models_app.models_assessment_answers import *
from app_assessment.models_app.models_templates import *

from app_assessment.forms_app.forms_templates import *

app_name = 'app_assessment'
app_version = 'v1'

module_name = 'configure/assessments'

# ============================================================= #
@login_required
def list_assessments(request, org_id):
    # take inputs
    # process inputs
    user = request.user   
    objects_count = 0
    objects_per_page = 10
    org = Organization.objects.get(id=org_id, active=True)
    search_query = request.GET.get('search', '')
    if search_query:
        tobjects = AssessmentTemplates.objects.filter(name__icontains=search_query, 
                                            org_id=org_id, author=user, template_flag=False).order_by('position')
    else:
        tobjects = AssessmentTemplates.objects.filter(active=True, org_id=org_id, template_flag=False).order_by('position')
    
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
        'page': 'list_assessments',
        'org': org,
        'org_id': org_id,
        'user': user,
        'tobjects': tobjects,
        'page_obj': page_obj,
        'objects_count': objects_count,
        'objects_per_page': objects_per_page,
        'show_all': show_all,

        'page_title': f'Assessments List',
    }       
    template_file = f"{app_name}/{module_name}/list_assessments.html"
    return render(request, template_file, context)


@login_required
def __internal_copy_template_details(request, selected_template, new_template):
    # Copy the remaining areas, questions and answers from this selected_template
    user = request.user
    areas = AssessmentAreas.objects.filter(template=selected_template, active=True).order_by('position')

    for area in areas:
        new_area = AssessmentAreas(
            template=new_template,
            name=f"{area.name}",
            text=area.text,  # Assuming 'text' is a field in 'AssessmentAreas'; adjust if incorrect
            author=user
        )
        new_area.save()        
        # Copy each question and its answers related to the original area
        questions = AssessmentQuestions.objects.filter(areas=area, active=True)
        for question in questions:
            new_question = AssessmentQuestions(
                areas=new_area,
                question_type=question.question_type,
                text=question.text,
                instructions=question.instructions,
                author=user
            )
            new_question.save()            
            # Copy each answer related to the question
            answers = AssessmentAnswers.objects.filter(question=question, active=True)
            for answer in answers:
                new_answer = AssessmentAnswers.objects.create(
                    question=new_question,
                    text=answer.text,
                    is_correct=answer.is_correct,
                    author=user
                )
# Create View
@login_required
def create_assessment(request, org_id):
    user = request.user
    org = Organization.objects.get(id=org_id, active=True)
    assessment_templates = AssessmentTemplates.objects.filter(org_id=org_id, 
                                                    active=True, 
                                                    template_flag=True).order_by('position')
    if request.method == 'POST':
        form = AssessmentTemplatesForm(request.POST)
        selected_template_id = request.POST.get('assessment_template')
        selected_template = get_object_or_404(AssessmentTemplates, 
                                              pk=selected_template_id, 
                                              active=True, template_flag=True)
        if form.is_valid():
            form.instance.author = user
            form.instance.org_id = org_id
            form.instance.template_flag = False
            new_template = form.save()
            
            # copy the remaining areas, questions and answers from this selected_template
            __internal_copy_template_details(request, selected_template, new_template)
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_assessments', org_id=org_id)
    else:
        form = AssessmentTemplatesForm()

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'create_assessment',
        'org': org,
        'org_id': org_id,
        'assessment_templates': assessment_templates,  
        'form': form,
        'page_title': f'Create Template',
    }
    template_file = f"{app_name}/{module_name}/create_assessment.html"
    return render(request, template_file, context)



# Edit
@login_required
def edit_assessment(request, org_id, template_id):
    user = request.user
    org = Organization.objects.get(id=org_id, active=True)
    object = get_object_or_404(AssessmentTemplates, pk=template_id, active=True)
    if request.method == 'POST':
        form = AssessmentTemplatesForm(request.POST, instance=object)
        if form.is_valid():
            form.instance.author = user
            form.instance.org_id = org_id
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_assessments', org_id=org_id)
    else:
        form = AssessmentTemplatesForm(instance=object)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'edit_assessment',
         'org': org,
        'org_id': org_id,
        'form': form,
        'object': object,
        'page_title': f'Edit Instance',
    }
    template_file = f"{app_name}/{module_name}/edit_assessment.html"
    return render(request, template_file, context)

@login_required
def delete_assessment(request, org_id, template_id):
    user = request.user
    org = Organization.objects.get(id=org_id, active=True)
    object = get_object_or_404(AssessmentTemplates, pk=template_id, active=True)
    if request.method == 'POST':
        object.active = False
        object.save()
        return redirect('list_assessments', org_id=org_id)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'delete_assessment',
         'org': org,
        'org_id': org_id,
        'object': object,
        'page_title': f'Delete Assessment',
    }
    template_file = f"{app_name}/{module_name}/delete_assessment.html"
    return render(request, template_file, context)

@login_required
def view_assessment(request, org_id, template_id):
    user = request.user
    org = Organization.objects.get(id=org_id, active=True)
    object = get_object_or_404(AssessmentTemplates, pk=template_id, active=True)    

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'view_assessment',
        'org': org,
        'org_id': org_id,
        'object': object,
        'page_title': f'View Assessment',
    }
    template_file = f"{app_name}/{module_name}/view_assessment.html"
    return render(request, template_file, context)


@login_required
def view_assessment_tree(request, org_id, template_id):
    org = get_object_or_404(Organization, id=org_id, active=True)
    template = get_object_or_404(AssessmentTemplates, pk=template_id, active=True)    

    areas = AssessmentAreas.objects.filter(template=template, active=True).prefetch_related('area_questions').order_by('position')
    # Build a structured list of areas and their questions
    total_questions = 0
    area_list = []

    for area in areas:
        questions = area.area_questions.filter(active=True).order_by('position')
        question_count = questions.count()
        total_questions += question_count
        area_list.append({
            'area': area,
            'questions': questions,
            'question_count': question_count  # Adding count here
        })

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'view_assessment_tree',
        'org': org,
        'org_id': org_id,
        'object': template,  
        'area_list': area_list,
        'total_questions': total_questions,
        'template': template,
        'area_list': area_list,
        'page_title': 'View Assessment Tree',
    }
    template_file = f"{app_name}/{module_name}/view_assessment_tree.html"
    return render(request, template_file, context)

@login_required
def copy_assessment(request, org_id, template_id):
    user = request.user
    org = get_object_or_404(Organization, id=org_id, active=True)  # Use get_object_or_404 for safety
    original_template = get_object_or_404(AssessmentTemplates, pk=template_id, active=True)
        
    # Create a new template copying the original
    new_template = AssessmentTemplates(
        org=org,  # Use org fetched by get_object_or_404
        name=f"{original_template.name}",
        text=original_template.text,
        description=original_template.description,
        template_flag=False,
        author=user
    )
    new_template.save()    
    # Copy areas related to the original template
    areas = AssessmentAreas.objects.filter(template=original_template, active=True)
    for area in areas:
        new_area = AssessmentAreas(
            template=new_template,
            name=f"{area.name}",
            text=area.text,  # Assuming 'text' is a field in 'AssessmentAreas'; adjust if incorrect
            author=user
        )
        new_area.save()        
        # Copy each question and its answers related to the original area
        questions = AssessmentQuestions.objects.filter(areas=area, active=True)
        for question in questions:
            new_question = AssessmentQuestions(
                areas=new_area,
                question_type=question.question_type,
                text=question.text,
                instructions=question.instructions,
                author=user
            )
            new_question.save()            
            # Copy each answer related to the question
            answers = AssessmentAnswers.objects.filter(question=question, active=True)
            for answer in answers:
                new_answer = AssessmentAnswers.objects.create(
                    question=new_question,
                    text=answer.text,
                    is_correct=answer.is_correct,
                    author=user
                )


    return redirect('list_assessments', org_id=org_id)
