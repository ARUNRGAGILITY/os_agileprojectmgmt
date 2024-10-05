from app_assessment.views_app.all_view_imports import *
from app_assessment.models_app.models_templates import *
from app_assessment.models_app.models_assessment_questions import *
from app_assessment.models_app.models_assessment_answers import *
from app_assessment.models_app.models_assessment_score import *
from app_assessment.models_app.models_assessment_types import *
from app_assessment.models_app.models_maturity_assessments import *
from app_assessment.models_app.models_assessments import *
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
    assessment_types = AssessmentTypes.objects.filter(active=True).order_by('position')
    
    if request.method == 'POST':
        assessment_type = request.POST.get('assessment_type')
        assessment_duration = request.POST.get('assessment_duration')
        print(type(assessment_duration))
        print(f">>> === Assessment Duration: |{assessment_duration}| === <<<")
        
        assessment_details = None
        if assessment_duration != "":
            assessment_duration = str(assessment_duration).strip()
            if assessment_duration in ["15", "30", "45", "60", "90", "120"]:
                try:
                    assessment_details, created = AssessmentDetails.objects.get_or_create(
                                                        org_id = org_id,
                                                        assessment_id = template_id,
                                                        total_time_given=assessment_duration,
                                                        author=user,
                                                        )
                    if created:
                        print("A new AssessmentDetails object was created.")
                    else:
                        print("An existing AssessmentDetails object was retrieved.")
                except Exception as e:
                    print(f">>> === An error occurred: {e} === <<<")

        
        if assessment_type:
            assessment_type = get_object_or_404(AssessmentTypes, pk=assessment_type, active=True)
            object.assessment_type = assessment_type
            object.save()
            messages.success(request, f'Assessment Type updated successfully!')
            print(f'Assessment Type updated successfully!')
            return redirect('schedule_assessment', org_id=org_id, template_id=template_id)
        
    
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'configure_assessment',
        'org': org,
        'org_id': org_id,
        'object': object,
        'assessment_types': assessment_types,
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
    display_assessment_type = object.assessment_type.name.replace('_', ' ').title().strip()
    
    if request.method == 'POST':
        if display_assessment_type == "Agile Team Maturity Assessment":
            return redirect('assessment_maturity_type', org_id=org_id, template_id=template_id)
        return redirect('assessment', org_id=org_id, template_id=template_id)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'schedule_assessment',
        'org': org,
        'org_id': org_id,
        'object': object,
        'display_assessment_type': display_assessment_type,
        'page_title': f'Schedule Assessments',
    }
    template_file = f"{app_name}/{module_name}/schedule_assessment.html"
    return render(request, template_file, context)

# internal calculation
def get_average_ratings(assessment_template_id):
    # Fetch all ratings for a specific assessment template
    ratings = AssessmentMaturityTypeRating5.objects.filter(assessment_id=assessment_template_id)

    # Compute average ratings for each area
    area_averages = ratings.values('area__name').annotate(average_rating=Avg('rating')).order_by('area__name')

    # Compute average ratings for each question
    question_averages = ratings.values('question__text').annotate(average_rating=Avg('rating')).order_by('question__text')

    return area_averages, question_averages



def boolean_check_answer_text(response_answers_str, correct_answers_str):
    def safe_convert_to_ints(str_ids):
        if str_ids is None:
            return set()
        return set(int(item.strip()) for item in str_ids.split(',') if item.strip().isdigit())

    response_answers = safe_convert_to_ints(response_answers_str)
    correct_answers = safe_convert_to_ints(correct_answers_str)

    correct = response_answers.intersection(correct_answers)
    additional = response_answers.difference(correct_answers)
    incorrect = response_answers.difference(correct).difference(additional)

    # Check if the response is correct (strict)
    is_response_correct_strict = not incorrect and correct == correct_answers
    print(f">>> === Is Response Correct Strict: {is_response_correct_strict}{list(correct_answers)} === <<<")
    result = {
        'correct': list(correct),
        'additional': list(additional),
        'incorrect': list(incorrect),
        'is_correct_strict': is_response_correct_strict
    }
    return result
# this will evaluate the given question answers with the response answers
def evaluate_responses_v1(response_answers_str, correct_answers_str):
    # Helper function to convert and validate strings to integers
    def safe_convert_to_ints(str_ids):
        if str_ids is None:
            print("Received NoneType for str_ids, defaulting to empty string.")
            str_ids = ''  # Default to empty string if None is received
        valid_ids = []
        for item in str_ids.split(','):
            item = item.strip()
            if item.isdigit():  # Check if the string is numeric
                try:
                    valid_ids.append(int(item))
                except ValueError:
                    print(f"Invalid entry found and skipped: {item}")
            else:
                print(f"Non-integer value skipped: {item}")
        return set(valid_ids)

    # Convert the comma-separated string of IDs into sets of integers
    response_answers = safe_convert_to_ints(response_answers_str)
    correct_answers = safe_convert_to_ints(correct_answers_str)

    # Determine correct answers
    correct = response_answers.intersection(correct_answers)
    
    # Determine additional answers
    if correct:
        additional = response_answers.difference(correct_answers)
    else:
        additional = set()

    # Determine incorrect answers
    if correct:
        incorrect = response_answers.difference(correct).difference(additional)
    else:
        incorrect = response_answers.difference(correct_answers)

    # # Print results for verification
    # print(f">>> === Correct: {correct} === <<<")
    # print(f">>> === Additional: {additional} === <<<")
    # print(f">>> === Incorrect: {incorrect} === <<<")
    
    # Prepare the result dictionary
    result = {
        'correct': list(correct),
        'additional': list(additional),
        'incorrect': list(incorrect)
    }
    return result

# # Example call to the function
# response_str = "929"
# correct_str = "912,914"
# evaluate_responses(response_str, correct_str)

def evaluate_responses(response_answers_str, correct_answers_str):
    # Helper function to convert and validate strings to integers
    def safe_convert_to_ints(str_ids):
        if str_ids is None:
            print("Received NoneType for str_ids, defaulting to empty string.")
            str_ids = ''  # Default to empty string if None is received
        valid_ids = []
        for item in str_ids.split(','):
            item = item.strip()
            if item.isdigit():  # Check if the string is numeric
                try:
                    valid_ids.append(int(item))
                except ValueError:
                    print(f"Invalid entry found and skipped: {item}")
            else:
                print(f"Non-integer value skipped: {item}")
        return set(valid_ids)

    # Convert the comma-separated string of IDs into sets of integers
    response_answers = safe_convert_to_ints(response_answers_str)
    correct_answers = safe_convert_to_ints(correct_answers_str)

    # Determine correct answers
    correct = response_answers.intersection(correct_answers)

    # Determine if the response is partially correct
    partially_correct = bool(correct) and (response_answers != correct_answers)

    # Determine additional answers
    additional = response_answers.difference(correct_answers)

    # Determine incorrect answers
    incorrect = response_answers.difference(correct_answers).difference(additional)

    # # Print results for verification
    # print(f">>> === Correct: {correct} === <<<")
    # print(f">>> === Partially Correct: {partially_correct} === <<<")
    # print(f">>> === Additional: {additional} === <<<")
    # print(f">>> === Incorrect: {incorrect} === <<<")

    # Prepare the result dictionary
    result = {
        'correct': list(correct),
        'partially_correct': partially_correct,
        'additional': list(additional),
        'incorrect': list(incorrect)
    }
    return result

# # Example call to the function
# response_str = "912,915"
# correct_str = "912,914"
# evaluate_responses(response_str, correct_str)



# Step5: Assessment
@login_required
def assessment(request, org_id, template_id):
    user = request.user
    # this must be selected from the previous step (there may be multiple assessment which one to pickup)
    assessment_details = AssessmentDetails.objects.filter(assessment_id=template_id, active=True).first()
    result_display_flag = False
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
    candidate_assessment_details = {}
    question_paper = []      
    total_question_count = 0
    total_correct_count = 0
    total_unanswered_count = 0
    percentage = 0
    passing_percentage = 35
    candidate_pass = False
    if request.method == 'POST':
        submitted_answers = {}  # Dictionary to hold answers grouped by question_id

        # Iterate through each key in POST data
        for key in request.POST:
            if key.isdigit():  # Checking if the key is question_id (adjust this check if needed)
                answers = request.POST.getlist(key)  # Using getlist to handle multiple selections for MCQs
                submitted_answers[key] = answers
        
        # read the questions given and answers submitted        
        for area in areas:
            for question in area.area_questions.filter(active=True).order_by('position'):
                if question.question_type.name in ["MCQ", "SCQ", "True/False", "Yes/No"]:
                    total_question_count += 1
                question_id = str(question.id)
                correct_answers_int = question.question_answers.filter(active=True, is_correct=True).values_list('id', flat=True)
                correct_answers = [str(answer_id) for answer_id in correct_answers_int]
                correct_answers_text = ','.join(correct_answers)
                response_answers_text = None
                if question_id in submitted_answers:
                    print(f">>> === Question {question_id} === <<<")
                    answers = submitted_answers[question_id]   
                    response_answers_text = ','.join(answers)
                    print(f">>> === Response Answers {response_answers_text} === <<<")
                    print(f">>> === Correct Answers {correct_answers_text} === <<<")                     
                    question_paper.append({
                        'question': question.id,
                        'answers': answers
                    })      
                    result = evaluate_responses(response_answers_text, correct_answers_text) 
                    correct_answer_input = False
                    if result['correct']:
                        correct_answer_input = True
                   
                    if correct_answer_input:
                        total_correct_count += 1
                    AssessmentResponse.objects.create(
                        question=question,
                        correct_answer_text=correct_answers_text,
                        response_answer_text=answers,
                        response_correct=correct_answer_input,
                        candidate=user,
                        author=user 
                    )          
                else:
                    not_answered = "Not Answered"
                    question_paper.append({
                        'question': question.id,
                        'answers': not_answered,
                    })
                    total_unanswered_count += 1
                    AssessmentResponse.objects.create(
                        question=question,
                        correct_answer_text=correct_answers_text,
                        response_answer_text=not_answered,
                        candidate=user,
                        author=user 
                    )  
                
                # Checking the answers
                response_answers_str = response_answers_text
                correct_answers_str = correct_answers_text
                result = evaluate_responses(response_answers_str, correct_answers_str)
                print(f">>> === Result {result} === <<<")

            # summarize the results
            print(f">>> === Total Questions: {total_question_count} === <<<")
            print(f">>> === Total Correct: {total_correct_count} === <<<")
            print(f">>> === Total Unanswered: {total_unanswered_count} === <<<")

            # Save the assessment score
            percentage = (total_correct_count / total_question_count) * 100
            passing_percentage = 35 # comes from configuration
            candidate_pass = False
            if percentage >= passing_percentage:
                candidate_pass = True
            else:
                candidate_pass = False
            AssessmentScore.objects.create(
                assessment=template,
                candidate=user,
                score=total_correct_count,
                total_score=total_question_count,
                passing_score=total_correct_count,
                passing_percentage=passing_percentage,
                candidate_percentage=percentage,
                candidate_pass=candidate_pass,
                author=user,
            )
            
        candidate_assessment_details = {}
        candidate_assessment_details["total_questions"] = total_question_count
        candidate_assessment_details["total_correct"] = total_correct_count
        candidate_assessment_details["total_unanswered"] = total_unanswered_count
        candidate_assessment_details["percentage"] = percentage
        candidate_assessment_details["passing_percentage"] = passing_percentage
        candidate_assessment_details["candidate_pass"] = candidate_pass
        candidate_assessment_details["question_paper"] = question_paper
        result_display_flag = True
        print(f">>> === Candidate Assessment Details: {candidate_assessment_details} === <<<")

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'assessment',
        'org': org,
        'org_id': org_id,
        'object': template,  
        'area_list': area_list,
        'total_questions': total_questions,
        'candidate_assessment_details': candidate_assessment_details,
        'result_display_flag': result_display_flag,
        'template': template,
        'assessment_details': assessment_details,
        'page_title': f'Assessment',
    }
    template_file = f"{app_name}/{module_name}/assessment.html"
    return render(request, template_file, context)


# Step5.1: Assessment variation/branch for Maturity type
# Step5: Assessment
@login_required
def assessment_maturity_type(request, org_id, template_id):
    user = request.user
    # this must be selected from the previous step (there may be multiple assessment which one to pickup)
    assessment_details = AssessmentDetails.objects.filter(assessment_id=template_id, active=True).first()
    result_display_flag = False
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
    candidate_assessment_details = {}
    question_paper = []      
    total_question_count = 0
    total_correct_count = 0
    total_unanswered_count = 0
    percentage = 0
    passing_percentage = 35
    candidate_pass = False
    if request.method == 'POST':
        question_ids_responded = {}

        for key, value in request.POST.items():
            if key.isdigit():  # Check if the key is a question ID
                question_id = key
                rating = value  # This is the rating from 1 to 5
                question = AssessmentQuestions.objects.get(id=question_id, active=True)
                question_ids_responded[str(question.id)] = int(rating)
        # read the questions given and answers submitted        
        for area in areas:
            for question in area.area_questions.filter(active=True).order_by('position'):
                # Create the date in the maturity assessment model
                if str(question.id) in question_ids_responded:
                    rating = question_ids_responded[str(question.id)]
                    AssessmentMaturityTypeRating5.objects.create(
                        assessment=template,
                        participant=user,
                        area=area,
                        question=question,
                        rating=rating,
                        author=user
                    )
                else:
                    # If the question was not answered
                    AssessmentMaturityTypeRating5.objects.create(
                        assessment=template,
                        participant=user,
                        area=area,
                        question=question,
                        rating=0,
                        author=user
                    )
        # Tell the template to display the results
        result_display_flag = True

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'assessment',
        'org': org,
        'org_id': org_id,
        'object': template,  
        'area_list': area_list,
        'total_questions': total_questions,
       
        'result_display_flag': result_display_flag,
        'template': template,
        'assessment_details': assessment_details,
        'page_title': f'Assessment',
    }
    template_file = f"{app_name}/{module_name}/assessment_maturity_type.html"
    return render(request, template_file, context)



# Step5: Review Assessment
@login_required
def review_assessment(request, org_id, template_id):
    user = request.user
    org = Organization.objects.get(id=org_id, active=True)
    object = get_object_or_404(AssessmentTemplates, pk=template_id, 
                               active=True, template_flag=False)    
    
    # get the data sorted
    area_averages, question_averages = get_average_ratings(template_id)

    # Preparing data for Chart.js
    area_labels = [area['area__name'] for area in area_averages]
    area_data = [float(area['average_rating']) for area in area_averages]
    # area_labels = ['Team Level', 'Individual Level', 'Project Level', 'Process Level', 'Organization Level']
    # area_data = [2.57, 3.25, 4.00, 3.21, 4.11]
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'review_assessment',
        'org': org,
        'org_id': org_id,
        'object': object,
        'area_averages': area_averages,
        'question_averages': question_averages,
        # 'area_labels': area_labels,
        # 'area_data': area_data,
        'area_labels_json': json.dumps(area_labels),
        'area_data_json': json.dumps(area_data),
        'page_title': f'Review Assessments',
    }
    template_file = f"{app_name}/{module_name}/review_assessment.html"
    return render(request, template_file, context)


# Step6: Last step, Analyze Assessment
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


# StepX: Post Assessment Step
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

