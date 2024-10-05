from django.shortcuts import render
from django.conf import settings
from app_zweb1.views_zweb1.view_imports import *
# Create your views here.
app_name = 'app_zweb1'
app_version = 'v1'
SITE_TITLE = getattr(settings, 'SITE_TITLE', 'MY SITE')

def general_home_page(request):
    
    context = {
        'parent_page': 'home',
        'page': 'home',
        
        'page_title': f'Home - {SITE_TITLE}',
    }
    template_url = f'{app_name}/general_home_page.html'
    return render(request, template_url, context)

def get_started(request):
    
    context = {
        'parent_page': 'home',
        'page': 'home',
        
        'page_title': f'Get Started - {SITE_TITLE}',
    }
    template_url = f'{app_name}/get_started.html'
    return render(request, template_url, context)

def at_register(request):
    # take inputs
    coding_ai = getattr(settings, 'CODING_AI', 'NOTHERE')
    print(f">>>=== APP_ZWEB1:CODINGAI: {coding_ai} === <<<")
    CORRECT_REG_CODE = coding_ai
    # process inputs
    if request.method == 'POST':
        # Retrieve the registration code from the form
        reg_code = request.POST.get('reg_code', '')
        
        # Check if the reg_code is alphanumeric and matches the correct registration code
        if CORRECT_REG_CODE != 'NOTHERE':
            if not reg_code.isalnum() or reg_code != CORRECT_REG_CODE:
                messages.error(request, f"Invalid or incorrect registration code.")
                # Return to the registration page with the form and error message
                return redirect("register")
        
        # Proceed with the standard registration process if the reg_code is valid
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            # registered
            profile, created = AWProfile.objects.get_or_create(user=request.user)
            if created:
                if user.is_superuser:
                    site_admin_role = get_or_create_siteadmin_role()
                    profile.roles.add(site_admin_role)                
                profile.save()
            
            # Redirect to a success page after registration            
            return redirect('user_page')
        else:
            # If the form is not valid, show form error messages
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")


    context = {
        'parent_page': 'home',
        'page': 'at_register',
        'form': UserCreationForm(),
        'page_title': f'Register - {SITE_TITLE}',
    }
    template_url = f'{app_name}/at_register.html'
    return render(request, template_url, context)

def at_login(request):
    # take inputs
    # process inputs
    if request.method == 'POST': 
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            print(f">>> === {app_name}::LOGIN PAGE === <<<")
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next', 'loggedin_home_page') # Provide a default redirect URL
            return redirect(next_url)
        else:
            print(f">>> === form invalid {form.errors} === <<<")
            # If you want to display form errors, ensure your template can display them
            messages.error(request, 'Username or password is incorrect')
    context = {
        'parent_page': 'home',
        'page': 'at_login',
        'form': AuthenticationForm(),
        'page_title': f'Login - {SITE_TITLE}',
    }
    template_url = f'{app_name}/at_login.html'
    return render(request, template_url, context)
# Logout page
def at_logout(request):
    print(f">>> === {app_name}:{request.user}:Logout === <<<")
    logout(request)
    return redirect(f'/{app_version}/')


### starting other navbar menus
### Features, Learn, Blogs, FAQs, Contact Support, Provide Feedback, About
def features(request):
    
    # processing POST
    if request.method == 'POST':
        community = request.POST.get('community_edition', '')
        cloud = request.POST.get('cloud_edition', '')
        saas = request.POST.get('saas_edition', '')
        if community == 'Consult for Community Edition':
            return redirect('consult_feature', feature='community_edition')            
        elif cloud == 'Consult for Cloud Edition':
            return redirect('consult_feature', feature='cloud_edition')
        elif saas == 'Consult for SaaS Edition':
            return redirect('consult_feature', feature='saas_edition')
        else:
            print(f">>> === {app_name}::FEATURES PAGE: no edition selected === <<<")
    context = {
        'parent_page': 'home',
        'page': 'features',
        
        'page_title': f'Features - {SITE_TITLE}',
    }
    template_url = f'{app_name}/features.html'
    return render(request, template_url, context)

def consult_feature(request, feature):
    if feature == 'community_edition':
        display_feature = 'Consult for Community Edition'
    elif feature == 'cloud_edition':
        display_feature = 'Consult for Cloud Edition'
    elif feature == 'saas_edition':
        display_feature = 'Consult for SaaS Edition'
    else:
        display_feature = 'No Consulting given'
    # processing POST
    if request.method == 'POST':
        email = request.POST.get('email', '')
        comment = request.POST.get('comment', '')
        print(f">>> === {app_name}::CONSULT FEATURE PAGE: {feature} {email} - {comment} === <<<")
        # Add a message
        messages.success(request, f'Your consultation request for {display_feature} has been submitted successfully!')

        return redirect('features')
    context = {
        'parent_page': 'features',
        'page': 'consult_feature',
        'feature': feature,
        'display_feature': display_feature,
        
        'page_title': f'Consult Feature - {SITE_TITLE}',
    }
    template_url = f'{app_name}/consult_feature.html'
    return render(request, template_url, context)


def learn(request):
    
    context = {
        'parent_page': 'home',
        'page': 'learn',
        
        'page_title': f'Learn - {SITE_TITLE}',
    }
    template_url = f'{app_name}/learn.html'
    return render(request, template_url, context)

def blogs(request):
    
    context = {
        'parent_page': 'home',
        'page': 'blogs',
        
        'page_title': f'Blogs - {SITE_TITLE}',
    }
    template_url = f'{app_name}/blogs.html'
    return render(request, template_url, context)


def about(request):
    
    context = {
        'parent_page': 'home',
        'page': 'about',
        
        'page_title': f'About - {SITE_TITLE}',
    }
    template_url = f'{app_name}/about.html'
    return render(request, template_url, context)

def FAQs(request):
    
    context = {
        'parent_page': 'home',
        'page': 'FAQs',
        
        'page_title': f'FAQs - {SITE_TITLE}',
    }
    template_url = f'{app_name}/FAQs.html'
    return render(request, template_url, context)

def contact_support(request):
    
    context = {
        'parent_page': 'home',
        'page': 'contact_support',
        
        'page_title': f'Contact Support - {SITE_TITLE}',
    }
    template_url = f'{app_name}/contact_support.html'
    return render(request, template_url, context)

def provide_feedback(request):
    
    context = {
        'parent_page': 'home',
        'page': 'provide_feedback',
        
        'page_title': f'Provide Feedback - {SITE_TITLE}',
    }
    template_url = f'{app_name}/provide_feedback.html'
    return render(request, template_url, context)

def loggedin_home_page(request):
    user_ref = request.user
    context = {
        'parent_page': 'home',
        'page': 'loggedin_home_page',
        
        'page_title': f'Welcome {user_ref} - {SITE_TITLE}',
    }
    template_url = f'{app_name}/loggedin_home_page.html'
    return render(request, template_url, context)