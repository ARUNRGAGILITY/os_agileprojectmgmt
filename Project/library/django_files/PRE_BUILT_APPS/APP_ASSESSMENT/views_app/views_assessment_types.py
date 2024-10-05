
from app_assessment.views_app.all_view_imports import *
from app_assessment.models_app.models_assessment_types import *
from app_assessment.forms_app.forms_assessment_types import *

app_name = 'app_assessment'
app_version = 'v1'

module_name = 'assessment_types'
module_path = f'configure/assessment_types'

# ============================================================= #
@login_required
def list_assessment_types(request, org_id):
    # take inputs
    # process inputs
    user = request.user   
    objects_count = 0
    objects_per_page = 50
    org = Organization.objects.get(id=org_id, active=True)
    
    search_query = request.GET.get('search', '')
    if search_query:
        tobjects = AssessmentTypes.objects.filter(name__icontains=search_query, 
                                            org_id=org_id, author=user).order_by('position')
    else:
        tobjects = AssessmentTypes.objects.filter(active=True, org_id=org_id).order_by('position')
    
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
        'page': 'list_assessment_types',
        'org': org,
        'org_id': org_id,
        
        'module_path': module_path,
        'user': user,
        'tobjects': tobjects,
        'page_obj': page_obj,
        'objects_count': objects_count,
        'objects_per_page': objects_per_page,
        'show_all': show_all,

        'page_title': f'Assessment_types List',
    }       
    template_file = f"{app_name}/{module_path}/list_assessment_types.html"
    return render(request, template_file, context)





# Create View
@login_required
def create_assessment_type(request, org_id):
    user = request.user
    org = Organization.objects.get(id=org_id, active=True)
    
    if request.method == 'POST':
        form = AssessmentTypesForm(request.POST)
        if form.is_valid():
            form.instance.author = user
            form.instance.org_id = org_id
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_assessment_types', org_id=org_id)
    else:
        form = AssessmentTypesForm()

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'create_assessment_type',
        'org': org,
        'org_id': org_id,
        
        'module_path': module_path,
        'form': form,
        'page_title': f'Create Assessment Type',
    }
    template_file = f"{app_name}/{module_path}/create_assessment_type.html"
    return render(request, template_file, context)




# Edit
@login_required
def edit_assessment_type(request, org_id, type_id):
    user = request.user
    org = Organization.objects.get(id=org_id, active=True)
    
    object = get_object_or_404(AssessmentTypes, pk=type_id, active=True)
    if request.method == 'POST':
        form = AssessmentTypesForm(request.POST, instance=object)
        if form.is_valid():
            form.instance.author = user
            form.instance.org_id = org_id
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_assessment_types', org_id=org_id)
    else:
        form = AssessmentTypesForm(instance=object)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'edit_assessment_type',
        'org': org,
        'org_id': org_id,
        
        'module_path': module_path,
        'form': form,
        'object': object,
        'page_title': f'Edit Assessment Type',
    }
    template_file = f"{app_name}/{module_path}/edit_assessment_type.html"
    return render(request, template_file, context)



@login_required
def delete_assessment_type(request, org_id, type_id):
    user = request.user
    org = Organization.objects.get(id=org_id, active=True)
    
    object = get_object_or_404(AssessmentTypes, pk=type_id, active=True)
    if request.method == 'POST':
        object.active = False
        object.save()
        return redirect('list_assessment_types', org_id=org_id)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'delete_assessment_type',
        'org': org,
        'org_id': org_id,
        
        'module_path': module_path,        
        'object': object,
        'page_title': f'Delete Assessment Type',
    }
    template_file = f"{app_name}/{module_path}/delete_assessment_type.html"
    return render(request, template_file, context)


@login_required
def view_assessment_type(request, org_id, type_id):
    user = request.user
    org = Organization.objects.get(id=org_id, active=True)
    
    object = get_object_or_404(AssessmentTypes, pk=type_id, active=True)    

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'view_assessment_type',
        'org': org,
        'org_id': org_id,
        
        'module_path': module_path,
        'object': object,
        'page_title': f'View Assessment Type',
    }
    template_file = f"{app_name}/{module_path}/view_assessment_type.html"
    return render(request, template_file, context)


