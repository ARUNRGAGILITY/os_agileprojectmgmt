from app_zweb1.views_zweb1.view_imports import *
app_name = 'app_zweb1'
app_version = 'v1'
@login_required
def blog_details(request):
    # take inputs
    # process inputs
    user = request.user   

    # send outputs (info, template,
    context = {
        'parent_page': 'blogs',
        'page': 'blog_details',
        'user': user,

        'page_title': f'Blog Details - {SITE_TITLE}',
    }       
    template_file = f"{app_name}/blogs/blog_details.html"
    return render(request, template_file, context)

