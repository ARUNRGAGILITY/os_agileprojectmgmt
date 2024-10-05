from django.shortcuts import render
from app_web.imports.all_view_imports import *
from . models import *
from . forms import *

# Create your views here.
app_name = "app_user"

class CustomPasswordChangeView(PasswordChangeView):
    template_url = f"{app_name}/user/password_change.html"
    template_name = f"{template_url}"
    success_url = reverse_lazy('user_home')

@login_required
def user_home(request):
    context = {'page': 'user_home'}
    template_file = f"{app_name}/user/user_home.html"
    return render(request, template_file, context)

def logout_page(request):
    logout(request)
    return redirect('/')

@login_required
def home(request):
    context = {'page': 'home'}
    template_file = f"{app_name}/user/home_page.html"
    return render(request, template_file, context)

@login_required
def user_settings(request):
    context = {'page': 'user_settings'}
    template_file = f"{app_name}/user/user_settings.html"
    return render(request, template_file, context)

@login_required
def profile(request):    
    # check if user has profile or create one
    user_profile = None 
    try:
        user_profile = Profile.objects.get(user=request.user)
    except:
        print(f"UserProfile does not exists")
        user_profile = Profile(user=request.user, bio='Enter Bio')
        user_profile.save()
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('user_home')
        else:
            print(f"error in the profile updation {user_form} {profile_form}")

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    template_file = f"{app_name}/user/profile.html"
    return render(request, template_file, context)

# Login Page
def login_page(request):
    # take inputs
    # process inputs
    if request.method == 'POST': 
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next', 'user_home') # Provide a default redirect URL
            return redirect(next_url)
        else:
            print(f">>> === form invalid {form.errors} === <<<")
            # If you want to display form errors, ensure your template can display them
            messages.error(request, 'Username or password is incorrect')
    # send outputs (info, template, request)
    context = {
        'page': 'login',
    }
    template_file = f"{app_name}/user/login.html"
    return render(request, template_file, context)

# help function
def check_reg_code(reg_code):
    reg_codes = RegCode.objects.filter(active=True)
    for code in reg_codes:
        if reg_code == code.reg_code:
            print(f">>> === valid reg code: reg_code:{reg_code}={code.reg_code} === <<<")
            return True
    return False    

# Registration Page (updated)
def register_page(request):
    # take inputs
    reg_codes = RegCode.objects.filter(active=True)
    # process inputs
    if request.method == 'POST':
        reg_code = request.POST.get('reg_code', '')     
        p1 = request.POST.get('password1', '')
        p2 = request.POST.get('password2', '')
        if p1 != p2:
            messages.error(request, f"Passwords do not match.")
            return redirect("register_page")   
        if not check_reg_code(reg_code):
            messages.error(request, f"Invalid or incorrect registration code.")
            return redirect("register_page")        
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('user_home')
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
    # send outputs (info, template, request)
    context = {
        'page': 'register',
    }
    template_file = f"{app_name}/user/register.html"
    return render(request, template_file, context)
