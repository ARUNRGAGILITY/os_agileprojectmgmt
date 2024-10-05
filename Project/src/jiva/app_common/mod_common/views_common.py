# this basic import
from app_common.mod_app.all_view_imports import *

# # models
# from app_automate.models_app.models_automate import *
# from app_automate.models_app.models_backlogs import *
# from app_automate.models_app.models_orgs import *
# from app_automate.models_app.models_foundations import *
# # forms
# from app_automate.forms_app.forms_backlogs import *
# from app_automate.forms_app.forms_orgs import *

app_name = 'app_automate'
app_version = 'v1'  
@login_required
def ajax_update_model_list_sorted(request):
    if request.method == 'POST':
        ajax_data = request.POST['sorted_list_data']
        model_name = request.POST['model_name']
        given_app_name = app_name
        if 'app_name' in request.POST:            
            given_app_name = request.POST['app_name']
        new_data = ajax_data.replace("[",'')
        new_data = new_data.replace("]",'')
        sorted_list = new_data.split(",")
        seq = 1
        
        #model_class = globals()[model_name]
        model_class = apps.get_model(given_app_name, model_name)
        print(f">>> === AJAX UPDATE SORTED === <<<")
        for item in sorted_list:
            str = item.replace('"','')
            position = str.split('_')
            print(f">>> === AJAX UPDATE SORTED {position} === <<<")
            model_class.objects.filter(pk=position[0]).update(position=seq, author=request.user)
            seq = seq + 1
        context = {'page': 'Sorted Value', 
                   'active_tab': 'sorted_value',
                   'ajax_data': ajax_data}
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@login_required
def ajax_save_element_text(request):
    if request.method == 'POST':
        text_data = request.POST.get('text')
        object_id = request.POST.get('id')
        model_name = request.POST.get('model_name')
        field_name = request.POST.get('field_name')
        got_app_name = request.POST.get('app_name', app_name)  # Default to a specific app if not provided

        try:
            model_class = apps.get_model(got_app_name, model_name)
            # Update the specified object
            fields_update = {field_name: text_data}
            obj = model_class.objects.filter(id=object_id).update(**fields_update, author=request.user)
            return JsonResponse({'status': 'success', 'updated_records': obj})
        except LookupError:
            return JsonResponse({'status': 'error', 'message': 'Model not found.'})
        except model_class.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Object not found.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

@login_required
def ajax_update_task_done_state(request):
    if request.method == 'POST':
        user = request.user
        id = request.POST.get('id', None)
        done = request.POST.get('done', None)
        
        model_name = request.POST['model_name']
        given_app_name = app_name
        if 'app_name' in request.POST:            
            given_app_name = request.POST['app_name']
        
        model_class = apps.get_model(given_app_name, model_name)
        if id and done:
            object = model_class.objects.filter(id=id, author=user).first()
            if object:
                object.done = done.lower() == 'true'
                object.save()
                return JsonResponse({'success': True})      

    return JsonResponse({'success': False})