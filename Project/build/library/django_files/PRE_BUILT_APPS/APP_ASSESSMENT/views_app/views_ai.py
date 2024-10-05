from app_assessment.views_app.all_view_imports import *
from app_assessment.models_app.models_asmt import *
from app_assessment.forms_app.forms_asmt import *

from app_assessment.models_app.models_templates import *
from app_assessment.models_app.models_assessment_questions import *
from app_assessment.models_app.models_assessment_answers import *
from app_assessment.models_app.models_assessment_score import *

import requests
from django.conf import settings  # Ensure your API key is stored in Django's settings
from django.shortcuts import render
app_name = 'app_assessment'
app_version = 'v1'

module_name = 'ai'
module_title = module_name.capitalize()
module_version = ''

def get_chatgpt_suggestions(score):
    api_url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "gpt-3.5-turbo",  # Choose the appropriate model version
        "messages": [
            {"role": "system", "content": "Provide coaching plan based on assessment score. in a csv format, with topics, description, action plan in bullets, success criteria"},
            {"role": "user", "content": f"My assessment score is {score}. What suggestions do you have?"}
        ]
    }
    
    response = requests.post(api_url, headers=headers, json=data)
    print(f">>> === response: {response.json()} === <<<")
    return response.json()  # This will return the response from ChatGPT


# Step 2: Transform the content into a structured data format
def __parse_coaching_plan(content):
    sections = content.split('\n\n')[1:]  # Skip the introductory text
    structured_content = []
    for section in sections:
        if section.strip():
            # Try to split into title and description safely
            parts = section.split(': ', 1)
            if len(parts) == 2:
                title, desc = parts
                structured_content.append({'title': title.strip(), 'description': desc.strip()})
            else:
                # Handle the case where no ':' is found
                structured_content.append({'title': "*", 'description': section.strip()})
    return structured_content


@login_required
def sample_asmt(request, org_id):
      
    user = request.user
    org = Organization.objects.get(id=org_id)
    parent_page = 'loggedin_home_page'
    
    # Example: Assume 'score' is fetched from user's assessment result
    score = 75  # This would realistically come from the assessment data

    response = get_chatgpt_suggestions(score)
    suggestions = response['choices'][0]['message']['content']   
    
    # Extract content from the response
    content = response['choices'][0]['message']['content']
    coaching_plan = __parse_coaching_plan(content)

    # Now you have a structured list of dictionaries where each dict is a section of the coaching plan
    print(json.dumps(coaching_plan, indent=4))    
  
    context = {
        'parent_page': f"{parent_page}",
        'page': 'sample_asmt',
        'org': org,
        'org_id': org_id,
        'suggestions': suggestions,
        'coaching_plan': coaching_plan,

        'page_title': f'Sample Assessment with AI',
    }
    template_file = f"{app_name}/{module_name}/sample_asmt.html"
    return render(request, template_file, context)



### Question Generation
@login_required
def generate_questions(area, num_questions):
    api_url = "https://api.openai.com/v1/engines/davinci/completions"
    headers = {
        "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    prompt = f"Generate {num_questions} multiple choice questions about {area} in Python."
    data = {
        "prompt": prompt,
        "max_tokens": 100 * num_questions,  # Assuming around 100 tokens per question
        "temperature": 0.7,
        "top_p": 1,
        "n": 1,  # Generate one response containing multiple questions
        "stop": ["\n\n"]  # Use double newline as stop sequence if suitable
    }
    response = requests.post(api_url, headers=headers, json=data)
    return response.json()

# # Example usage
# basics_questions = generate_questions("Basics", 13)
# data_types_questions = generate_questions("Basic Data Types", 12)
@login_required
def save_questions_to_db(questions_text, area_name, template_name):
    template, created = AssessmentTemplates.objects.get_or_create(name=template_name)
    area, created = AssessmentAreas.objects.get_or_create(template=template, name=area_name)
    
    questions = questions_text.split('\n\n')  # Splitting each question by double newline
    for question_text in questions:
        AssessmentQuestions.objects.create(
            template=template,
            area=area,
            text=question_text,
            question_type='Multiple Choice'
        )

# Assuming 'questions' is a string of multiple questions separated by double newlines
# save_questions_to_db(basics_questions['choices'][0]['text'], "Basics", "Python")
# save_questions_to_db(data_types_questions['choices'][0]['text'], "Basic Data Types", "Python")
