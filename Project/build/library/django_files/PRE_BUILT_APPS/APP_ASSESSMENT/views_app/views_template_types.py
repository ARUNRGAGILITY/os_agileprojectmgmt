
from app_assessment.views_app.all_view_imports import *
from app_assessment.models_app.models_template_types import *
from app_assessment.forms_app.forms_template_types import *

app_name = 'app_assessment'
app_version = 'v1'

module_name = 'configure/template_types'

# ============================================================= #
@login_required
def list_template_types(request, org_id):
    # take inputs
    # process inputs
    user = request.user   
    objects_count = 0
    objects_per_page = 50
    org = Organization.objects.get(id=org_id, active=True)

    search_query = request.GET.get('search', '')
    if search_query:
        tobjects = AssessmentTemplateTypes.objects.filter(name__icontains=search_query, 
                                            org_id=org_id, author=user).order_by('position')
    else:
        tobjects = AssessmentTemplateTypes.objects.filter(active=True, org_id=org_id).order_by('position')
    
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
        'page': 'list_template_types',
        'org': org,
        'org_id': org_id,
        'user': user,
        'tobjects': tobjects,
        'page_obj': page_obj,
        'objects_count': objects_count,
        'objects_per_page': objects_per_page,
        'show_all': show_all,

        'page_title': f'Template_types List',
    }       
    template_file = f"{app_name}/{module_name}/list_template_types.html"
    return render(request, template_file, context)




# Create View
@login_required
def create_template_type(request, org_id):
    user = request.user
    org = Organization.objects.get(id=org_id, active=True)
    if request.method == 'POST':
        form = AssessmentTemplateTypesForm(request.POST)
        if form.is_valid():
            form.instance.author = user
            form.instance.org_id = org_id
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_template_types', org_id=org_id)
    else:
        form = AssessmentTemplateTypesForm()

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'create_template_type',
        'org': org,
        'org_id': org_id,
        'form': form,
        'page_title': f'Create Template_type',
    }
    template_file = f"{app_name}/{module_name}/create_template_type.html"
    return render(request, template_file, context)



# Edit
@login_required
def edit_template_type(request, org_id, template_type_id):
    user = request.user
    org = Organization.objects.get(id=org_id, active=True)
    object = get_object_or_404(AssessmentTemplateTypes, pk=template_type_id, active=True)
    if request.method == 'POST':
        form = AssessmentTemplateTypesForm(request.POST, instance=object)
        if form.is_valid():
            form.instance.author = user
            form.instance.org_id = org_id
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_template_types', org_id=org_id)
    else:
        form = AssessmentTemplateTypesForm(instance=object)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'edit_template_type',
        'org': org,
        'org_id': org_id,
        'form': form,
        'object': object,
        'page_title': f'Edit Template_type',
    }
    template_file = f"{app_name}/{module_name}/edit_template_type.html"
    return render(request, template_file, context)


@login_required
def delete_template_type(request, org_id, template_type_id):
    user = request.user
    org = Organization.objects.get(id=org_id, active=True)
    object = get_object_or_404(AssessmentTemplateTypes, pk=template_type_id, active=True)
    if request.method == 'POST':
        object.active = False
        object.save()
        return redirect('list_template_types', org_id=org_id)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'delete_template_type',
        'org': org,
        'org_id': org_id,
        'object': object,
        'page_title': f'Delete Template_type',
    }
    template_file = f"{app_name}/{module_name}/delete_template_type.html"
    return render(request, template_file, context)

@login_required
def view_template_type(request, org_id, template_type_id):
    user = request.user
    org = Organization.objects.get(id=org_id, active=True)
    object = get_object_or_404(AssessmentTemplateTypes, pk=template_type_id, active=True)    

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'view_template_type',
        'org': org,
        'org_id': org_id,
        'object': object,
        'page_title': f'View Template_type',
    }
    template_file = f"{app_name}/{module_name}/view_template_type.html"
    return render(request, template_file, context)

