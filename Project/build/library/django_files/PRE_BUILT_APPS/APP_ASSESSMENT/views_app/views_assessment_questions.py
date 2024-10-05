
from app_assessment.views_app.all_view_imports import *
from app_assessment.models_app.models_templates import *
from app_assessment.models_app.models_assessment_questions import *
from app_assessment.models_app.models_assessment_answers import *
from app_assessment.forms_app.forms_assessment_questions import *

from app_assessment.models_app.models_question_types import *

app_name = 'app_assessment'
app_version = 'v1'

module_name = 'assessment_questions'
module_path = f'configure/assessment_questions'

# ============================================================= #
@login_required
def list_assessment_questions(request, areas_id):
    # take inputs
    # process inputs
    user = request.user   
    objects_count = 0
    objects_per_page = 50
    area = AssessmentAreas.objects.get(id=areas_id, active=True)
    org_id = area.template.org_id
    org =  Organization.objects.get(id=org_id, active=True)
    search_query = request.GET.get('search', '')
    if search_query:
        tobjects = AssessmentQuestions.objects.filter(name__icontains=search_query, 
                                            areas_id=areas_id, author=user).order_by('position')
    else:
        tobjects = AssessmentQuestions.objects.filter(active=True, areas_id=areas_id).order_by('position')
    
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
        'page': 'list_assessment_questions',
        'area': area,
        'areas_id': areas_id,
        'org': org,
        'org_id': org_id,
        'module_path': module_path,
        'user': user,
        'tobjects': tobjects,
        'page_obj': page_obj,
        'objects_count': objects_count,
        'objects_per_page': objects_per_page,
        'show_all': show_all,

        'page_title': f'Assessment_questions List',
    }       
    template_file = f"{app_name}/{module_path}/list_assessment_questions.html"
    return render(request, template_file, context)





# Create View
@login_required
def create_assessment_question(request, areas_id):
    correct_answers = None
    user = request.user
    area = AssessmentAreas.objects.get(id=areas_id, active=True)
    org_id = area.template.org_id
    org =  Organization.objects.get(id=org_id, active=True)
    if request.method == 'POST':
        form = AssessmentQuestionsForm(request.POST)
        if form.is_valid():
            form.instance.author = user
            form.instance.areas_id = areas_id
            form.instance.name = form.instance.text[0:50]
            object = form.save()
            
            question_type = request.POST.get('question_type')
            question_text = AssessmentQuestionTypes.objects.get(id=question_type).name
            print(f">>> === question_text: {question_text} === <<<")
            if question_text in ['SCQ', 'MCQ']:
                answers = request.POST.getlist('answers')
                correct_answers = request.POST.getlist('correct_answer')  # This now contains indices like ['1', '2']

                # Convert correct answer indices from string to integer for comparison
                correct_indices = [int(idx) - 1 for idx in correct_answers]  # subtract 1 to match zero-based index

                for index, answer_text in enumerate(answers):
                    is_correct = index in correct_indices
                    print(f">>> Answer Index: {index}, Answer Text: '{answer_text}' Is Correct: {is_correct}")
                    AssessmentAnswers.objects.create(
                        question=object,
                        text=answer_text.strip(),
                        is_correct=is_correct
                    )
            elif question_text == 'YN' or question_text == 'True/False':  # Assuming 'Yes/No' is stored as 'YN'
                # Create predefined answers for Yes and No
                AssessmentAnswers.objects.create(question=object, text='Yes', is_correct=request.POST.get('answers') == 'Yes')
                AssessmentAnswers.objects.create(question=object, text='No', is_correct=request.POST.get('answers') == 'No')

            elif question_text in ['Rating5', 'Rating10']:  # Rating type
                answers = request.POST.getlist('answers')
                correct_answers = request.POST.getlist('correct_answer')  # This now contains indices like ['1', '2']

                # Convert correct answer indices from string to integer for comparison
                correct_indices = [int(idx) - 1 for idx in correct_answers]  # subtract 1 to match zero-based index

                for index, answer_text in enumerate(answers):
                    is_correct = index in correct_indices
                    print(f">>> Answer Index: {index}, Answer Text: '{answer_text}' Is Correct: {is_correct}")
                    AssessmentAnswers.objects.create(
                        question=object,
                        text=answer_text.strip(),
                        is_correct=is_correct
                    )

            elif question_text == 'Text':  # Text answer type
                # No predefined correct answer for text responses
                AssessmentAnswers.objects.create(question=object, text=request.POST.get('answers'))
            print(f">>> === correct_answers: {correct_answers} === <<<")
            
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_assessment_questions', areas_id=areas_id)
    else:
        form = AssessmentQuestionsForm()
        
        

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'create_assessment_question',
        'area': area,
        'areas_id': areas_id,
        'org': org,
        'org_id': org_id,
        'module_path': module_path,
        'form': form,
        'page_title': f'Create Assessment Question',
    }
    template_file = f"{app_name}/{module_path}/create_assessment_question.html"
    return render(request, template_file, context)




# Edit
@login_required
def edit_assessment_question(request, areas_id, question_id):
    user = request.user
    area = AssessmentAreas.objects.get(id=areas_id, active=True)
    org_id = area.template.org_id
    org =  Organization.objects.get(id=org_id, active=True)
    object = get_object_or_404(AssessmentQuestions, pk=question_id, active=True)
    question = get_object_or_404(AssessmentQuestions, id=question_id)
    question_type = question.question_type
    answers = list(AssessmentAnswers.objects.filter(question=question))
    if request.method == 'POST':
        form = AssessmentQuestionsForm(request.POST, instance=object)
        if form.is_valid():
            form.instance.author = user
            form.instance.areas_id = areas_id
            form.save()
            
            current_question_type = request.POST.get('question_type')
            question_text = AssessmentQuestionTypes.objects.get(id=current_question_type).name
            print(f">>> === question_type: {question_type}:{current_question_type} === <<<")
            existing_answers = None
            if question_text in ['SCQ', 'MCQ']:
                answers = request.POST.getlist('answers')
                correct_answers = request.POST.getlist('correct_answer')  # Indices like ['1', '2']

                # Assuming Answer instances are related to the AssessmentQuestion instance `object`
                existing_answers = object.question_answers.filter(active=True)

                for idx, answer_text in enumerate(answers):
                    # Check if there's an existing answer or it's a new entry
                    if idx < len(existing_answers):
                        answer = existing_answers[idx]
                    else:
                        answer = AssessmentAnswers(question=object)

                    answer.text = answer_text
                    answer.is_correct = (str(idx) in correct_answers)  # Correctly map string indices
                    answer.save()

            if question_text in ['Yes/No', 'True/False']:
                answers = request.POST.getlist('answers')
                correct_answers = request.POST.getlist('correct_answer')  # Indices like ['1', '2']

                # Assuming Answer instances are related to the AssessmentQuestion instance `object`
                existing_answers = object.question_answers.filter(active=True)

                for idx, answer_text in enumerate(answers):
                    # Check if there's an existing answer or it's a new entry
                    if idx < len(existing_answers):
                        answer = existing_answers[idx]
                    else:
                        answer = AssessmentAnswers(question=object)

                    answer.text = answer_text
                    answer.is_correct = (str(idx) in correct_answers)  # Correctly map string indices
                    answer.save()
            if question_text in ['Rating5', 'Rating10']:
                answers = request.POST.getlist('answers')
                correct_answers = request.POST.getlist('correct_answer')  # Indices like ['1', '2']

                # Assuming Answer instances are related to the AssessmentQuestion instance `object`
                existing_answers = object.question_answers.filter(active=True)

                for idx, answer_text in enumerate(answers):
                    # Check if there's an existing answer or it's a new entry
                    if idx < len(existing_answers):
                        answer = existing_answers[idx]
                    else:
                        answer = AssessmentAnswers(question=object)

                    answer.text = answer_text
                    answer.is_correct = (str(idx) in correct_answers)  # Correctly map string indices
                    answer.save()

            elif question_text == 'Text':  # Text answer type
                answers = request.POST.getlist('answers')
                correct_answers = request.POST.getlist('correct_answer')  # Indices like ['1', '2']

                # Assuming Answer instances are related to the AssessmentQuestion instance `object`
                existing_answers = object.question_answers.filter(active=True)

                for idx, answer_text in enumerate(answers):
                    # Check if there's an existing answer or it's a new entry
                    if idx < len(existing_answers):
                        answer = existing_answers[idx]
                    else:
                        answer = AssessmentAnswers(question=object)

                    answer.text = answer_text
                    answer.is_correct = (str(idx) in correct_answers)  # Correctly map string indices
                    answer.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_assessment_questions', areas_id=areas_id)
    else:
        form = AssessmentQuestionsForm(instance=object)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'edit_assessment_question',
        'area': area,
        'areas_id': areas_id,
        'org': org,
        'org_id': org_id,
        'module_path': module_path,
        'form': form,
        'object': object,
        'question': question,
        'question_type': question_type,  # Added to pass the question type to the template
        'answers': answers,

        'page_title': f'Edit Assessment Question',
    }
    template_file = f"{app_name}/{module_path}/edit_assessment_question.html"
    return render(request, template_file, context)

@login_required
def copy_assessment_question(request, areas_id, question_id):
    user = request.user
    area = AssessmentAreas.objects.get(id=areas_id, active=True)
    org_id = area.template.org_id
    org =  Organization.objects.get(id=org_id, active=True)
    original_question = get_object_or_404(AssessmentQuestions, pk=question_id, active=True)
    
    # Create a new question copying the original
    new_question = AssessmentQuestions(
        areas=original_question.areas,
        text = original_question.text,
        question_type=original_question.question_type,
        instructions=original_question.instructions,
        author=request.user  # or `original_question.author` if you want to keep the same author
    )
    new_question.save()
    
    # Copy each answer related to the original question
    answers = AssessmentAnswers.objects.filter(question=original_question, active=True)
    for answer in answers:
        AssessmentAnswers.objects.create(
            question=new_question,
            text=answer.text,
            is_correct=answer.is_correct,
            author=request.user  # or `answer.author` if you want to keep the same author
        )
    
    # Redirect to a new URL, for example, the detail view of the new question
    return redirect('list_assessment_questions', areas_id=areas_id)


@login_required
def delete_assessment_question(request, areas_id, question_id):
    user = request.user
    area = AssessmentAreas.objects.get(id=areas_id, active=True)
    org_id = area.template.org_id
    org =  Organization.objects.get(id=org_id, active=True)
    object = get_object_or_404(AssessmentQuestions, pk=question_id, active=True)
    if request.method == 'POST':
        object.active = False
        object.save()
        return redirect('list_assessment_questions', areas_id=areas_id)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'delete_assessment_question',
        'area': area,
        'org': org,
        'org_id': org_id,
        'module_path': module_path,
        'areas_id': areas_id,
        'object': object,
        'page_title': f'Delete Assessment Question',
    }
    template_file = f"{app_name}/{module_path}/delete_assessment_question.html"
    return render(request, template_file, context)


@login_required
def view_assessment_question(request, areas_id, question_id):
    user = request.user
    area = AssessmentAreas.objects.get(id=areas_id, active=True)
    org_id = area.template.org_id
    org =  Organization.objects.get(id=org_id, active=True)
    object = get_object_or_404(AssessmentQuestions, pk=question_id, active=True)    

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'view_assessment_question',
        'area': area,
        'areas_id': areas_id,
        'org': org,
        'org_id': org_id,
        'module_path': module_path,
        'object': object,
        'page_title': f'View Assessment Question',
    }
    template_file = f"{app_name}/{module_path}/view_assessment_question.html"
    return render(request, template_file, context)


