from app_assessment.views_app.all_view_imports import *
from app_assessment.models_app.models_templates import *
from app_assessment.models_app.models_assessment_questions import *
from app_assessment.models_app.models_assessment_answers import *
from app_assessment.models_app.models_templates import *

from app_assessment.forms_app.forms_templates import *

app_name = 'app_assessment'
app_version = 'v1'

module_name = 'configure/conduct_assessments'

@login_required
def test_tab(request, org_id):
    user = request.user
    org = Organization.objects.get(id=org_id, active=True)
     

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'test_tab',
        'org': org,
        'org_id': org_id,
        'page_title': f'Testing Tab',
    }
    template_file = f"{app_name}/{module_name}/test_tab.html"
    return render(request, template_file, context)

@login_required
def conduct_assessments(request, org_id):
    user = request.user
    org = Organization.objects.get(id=org_id, active=True)
     

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'conduct_assessments',
        'org': org,
        'org_id': org_id,
        'page_title': f'Conduct Assessments',
    }
    template_file = f"{app_name}/{module_name}/conduct_assessments.html"
    return render(request, template_file, context)

@login_required
def select_assessment(request, org_id):
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
        'page': 'select_assessment',
        'org': org,
        'org_id': org_id,
        'user': user,
        'tobjects': tobjects,
        'page_obj': page_obj,
        'objects_count': objects_count,
        'objects_per_page': objects_per_page,
        'show_all': show_all,

        'page_title': f'Select Assessment',
    }       
    template_file = f"{app_name}/{module_name}/select_assessment.html"
    return render(request, template_file, context)

# Step2: Configure
@login_required
def configure_assessment(request, org_id, template_id):
    user = request.user
    org = Organization.objects.get(id=org_id, active=True)
    object = get_object_or_404(AssessmentTemplates, pk=template_id, 
                               active=True, template_flag=False)    

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'configure_assessment',
        'org': org,
        'org_id': org_id,
        'object': object,
        'page_title': f'Scheduled Assessments',
    }
    template_file = f"{app_name}/{module_name}/configure_assessment.html"
    return render(request, template_file, context)

# Step3: Schedule Assessment
@login_required
def schedule_assessment(request, org_id, template_id):
    user = request.user
    org = Organization.objects.get(id=org_id, active=True)
    object = get_object_or_404(AssessmentTemplates, pk=template_id, 
                               active=True, template_flag=False)    

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'schedule_assessment',
        'org': org,
        'org_id': org_id,
        'object': object,
        'page_title': f'Schedule Assessments',
    }
    template_file = f"{app_name}/{module_name}/schedule_assessment.html"
    return render(request, template_file, context)

# Step4: Assessment
@login_required
def review_assessment(request, org_id, template_id):
    user = request.user
    org = Organization.objects.get(id=org_id, active=True)
    object = get_object_or_404(AssessmentTemplates, pk=template_id, 
                               active=True, template_flag=False)    

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'review_assessment',
        'org': org,
        'org_id': org_id,
        'object': object,
        'page_title': f'Review Assessments',
    }
    template_file = f"{app_name}/{module_name}/review_assessment.html"
    return render(request, template_file, context)

# Step5: Assessment
@login_required
def assessment(request, org_id, template_id):
    user = request.user
    org = Organization.objects.get(id=org_id, active=True)
    template = get_object_or_404(AssessmentTemplates, pk=template_id, 
                               active=True, template_flag=False)  
    areas = AssessmentAreas.objects.filter(template=template, active=True).prefetch_related('area_questions').order_by('position')
    # Build a structured list of areas and their questions
    total_questions = 0
    area_list = []

    for area in areas:
        # Fetching questions with their related answers preloaded to optimize queries
        questions = area.area_questions.filter(active=True).order_by('position').prefetch_related('question_answers')
        question_count = questions.count()
        total_questions += question_count
        
        question_details = []
        for question in questions:
            # Collecting each question's answers
            answers = question.question_answers.filter(active=True).order_by('position')    
            question_details.append({
                'question': question,
                'answers': answers
            })
        
        area_list.append({
            'area': area,
            'question_details': question_details,  # Including questions with their answers
            'question_count': question_count
        })
    # process the request POST
    if request.method == 'POST':
        submitted_answers = {}  # Dictionary to hold answers grouped by question_id

        # Iterate through each key in POST data
        for key in request.POST:
            if key.isdigit():  # Checking if the key is question_id (adjust this check if needed)
                answers = request.POST.getlist(key)  # Using getlist to handle multiple selections for MCQs
                submitted_answers[key] = answers

        # Optional: Print or log submitted answers for debugging
        print("Submitted Answers:", submitted_answers)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'assessment',
        'org': org,
        'org_id': org_id,
        'object': template,  
        'area_list': area_list,
        'total_questions': total_questions,
        'template': template,
        'page_title': f'Assessment',
    }
    template_file = f"{app_name}/{module_name}/assessment.html"
    return render(request, template_file, context)

# Step3: Schedule Assessment
@login_required
def analyze_assessment(request, org_id, template_id):
    user = request.user
    org = Organization.objects.get(id=org_id, active=True)
    object = get_object_or_404(AssessmentTemplates, pk=template_id, 
                               active=True, template_flag=False)    

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'analyze_assessment',
        'org': org,
        'org_id': org_id,
        'object': object,
        'page_title': f'Analyze Assessments',
    }
    template_file = f"{app_name}/{module_name}/analyze_assessment.html"
    return render(request, template_file, context)


# Step3: Schedule Assessment
@login_required
def action_and_coaching_plan(request, org_id, template_id):
    user = request.user
    org = Organization.objects.get(id=org_id, active=True)
    object = get_object_or_404(AssessmentTemplates, pk=template_id, 
                               active=True, template_flag=False)    

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'action_and_coaching_plan',
        'org': org,
        'org_id': org_id,
        'object': object,
        'page_title': f'Coaching/Action Plan for Assessments',
    }
    template_file = f"{app_name}/{module_name}/action_and_coaching_plan.html"
    return render(request, template_file, context)

