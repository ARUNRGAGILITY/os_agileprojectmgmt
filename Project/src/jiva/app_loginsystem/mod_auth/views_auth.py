from django.shortcuts import render
from django.conf import settings
from app_loginsystem.mod_app.all_view_imports import *

# Create your views here.
app_name = 'app_loginsystem'
app_version = 'v1'
mod_name = 'auth'
mod_dirname = 'mod_auth'
SITE_TITLE = getattr(settings, 'SITE_TITLE', 'MY SITE')

def at_register(request):
    # take inputs
    coding_ai = getattr(settings, 'CODING_AI', 'NOTHERE')
    CORRECT_REG_CODE = coding_ai
    
    # process inputs
    if request.method == 'POST':
        print(f">>> === REGISTER PAGE === <<<")
        reg_code = request.POST.get('reg_code', '')  
        print(f">>> === {reg_code}::REGISTER PAGE === <<<")
        
        form = UserCreationForm(request.POST)
        
        if CORRECT_REG_CODE != 'NOTHERE':
            if reg_code.isalnum() and reg_code == CORRECT_REG_CODE:
                print(f">>> === {reg_code}::CORRECT CODE === <<<")       
                
                if form.is_valid():
                    user = form.save()
                    login(request, user)
                    messages.success(request, "Registration successful!")
                    return redirect('index')
                else:
                    # Iterate over all errors in the form
                    for field, errors in form.errors.items():
                        for error in errors:
                            messages.error(request, f"{field}: {error}")
            else:
                messages.error(request, "Invalid or incorrect registration code.")
                return redirect("at_register")
        else:
             messages.error(request, "Administration: Registration code is not set up correctly.")
    else:
        form = UserCreationForm()


    context = {
        'parent_page': 'home',
        'page': 'at_register',
        'form': form,
        'page_title': f'Register - {SITE_TITLE}',
    }
    template_url = f'{app_name}/{mod_dirname}/at_register.html'
    return render(request, template_url, context)

def at_login(request):
    # take inputs
    # process inputs
    form = AuthenticationForm()
    if request.method == 'POST': 
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            print(f">>> === {app_name}::LOGIN PAGE === <<<")
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next', 'index') 
            return redirect(next_url)
        else:
            print(f">>> === form invalid {form.errors} === <<<")
            messages.error(request, 'Username or password is incorrect')
    context = {
        'parent_page': 'home',
        'page': 'at_login',
        'form': form,
        'page_title': f'Login - {SITE_TITLE}',
    }
    template_url = f'{app_name}/{mod_dirname}/at_login.html'
    return render(request, template_url, context)


# Logout page
def at_logout(request):
    print(f">>> === {app_name}:{request.user}:Logout === <<<")
    logout(request)
    return redirect(f'/')

@login_required
def user_logged_in(request):
    user = request.user
    context = {
        'parent_page': 'home',
        'page': 'user_logged_in',
        
        'page_title': f'Welcome {user} - {SITE_TITLE}',
    }
    template_url = f'app_common/common_files/specific/user_logged_in.html'
    return render(request, template_url, context)