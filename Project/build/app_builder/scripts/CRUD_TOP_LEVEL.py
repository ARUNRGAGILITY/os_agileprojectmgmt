

models_x_py = """

from ___APPNAME___.mod_app.all_form_imports import *
from ___APPNAME___.mod____singularmodname___.models____singularmodname___ import *


class BaseModelImpl(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    
    # position for sequence
    position = models.PositiveIntegerField(default=1000)
    
    # date details
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # active or deleted
    active = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)
    
    # blocked
    blocked = models.BooleanField(default=False)
    blocked_count = models.PositiveIntegerField(default=0)
    
    # done and at time
    done = models.BooleanField(default=False)
    done_at = models.DateTimeField(null=True, blank=True)
    
    approved = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['position']
        abstract = True

    def __str__(self):
        return self.name
    
"""

forms_py = """
from ___APPNAME___.mod_app.all_form_imports import *
from ___APPNAME___.mod____singularmodname___.models____singularmodname___ import *

class ___MODELNAME___Form(forms.ModelForm):
    class Meta:
        model = ___MODELNAME___
        fields = ['name', 'description']
    def __init__(self, *args, **kwargs):
        super(___MODELNAME___Form, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False

"""

connected_to_organization_links_html = """
<!-- append the linkd that is linked to this level/model -->
"""


list_objects_html_single_level = """
{% extends 'app_common/common_files/base_template.html' %}
{% load static %}
{% load crispy_forms_tags %}
{% load custom_tags %}
{% load app_web_my_filters %}
{% load markdown_extras  %}
{% block content %}

{% include 'app_common/common_files/navbar.html' %}
<style>
  .trash-icon {
    position: fixed;
    right: 10px;
    bottom: 10px;
    font-size: 24px;  /* Size of the icon */
    cursor: pointer;
    color: #707070;  /* Color of the icon */
  }
</style>
<!-- Begin: Content -->
<div class="container-fluid">
    <div class="row">
        <div class="col col-md-12">
            {% include '___APPNAME___/___modulepath___/breadcrumb____pluralmodname___.html' %}
        </div>
    </div>
</div>
<div class="container-fluid">
    <div class="row">
        <div class="col col-md-12">           
            <!-- display -->
            
            <div class="row">
                <div class="col col-md-12">
                    <div class="container-fluid-width">
                        <div class="row pb-2">
                            <div class="col col-md-5">
                                <b class="h2">___DISPMODNAME___</b>
                                &nbsp;&nbsp;
                                ___DISPMODNAME___ List
                               
                            </div>
                            <div class="col col-md-4">
                                <form method="get">
                                    <input type="text" name="search" placeholder="Search" value="{{ search }}">
                                    &nbsp;&nbsp;  
                                    <button type="submit" class="btn btn-sm btn-primary">Search</button> 
                                    &nbsp;&nbsp;  
                                    <button type="submit" class="btn btn-sm btn-info">Clear</button>   
                                </form>
                            </div>
                            <div class="col col-md-3 text-end">
                                <span class="display_count">{{objects_count}} ___singularmodname___(s)</span>
                                &nbsp;&nbsp;
                                <a href="{% url 'create____singularmodname___'   %}" 
                                class="btn btn-sm btn-success"><b>+ Create ___DISPMODNAMESINGULAR___</b></a>
                            </div>
                        </div>
                    </div>
                    <form method="post">
                    {% csrf_token %}
                    <table class="table table-bordered sortable_table">
                        <thead>
                            <tr>
                                <th width="2%"><i class="bi bi-grip-vertical"></i></th>
                                <th width="2%">
                                    <input type="checkbox" name="select_all" id="select_all" onclick='checkUncheck(this)'>
                                </th>  
                                <th width="2%">#</th>
                                <th>___DISPMODNAMESINGULAR___</th>
                                <th width="20%">Description</th>
                                <th width="10%">Configure</th>
                                <th width="50%">                                    
                                    Actions
                                    &nbsp;&nbsp;
                                    <select name="pagination" id="paginationselect">
                                        <option value="none" {% if selected_pagination == 'none' %}selected{% endif %}>-Page-</option>
                                        {% for option in pagination_options %}
                                            <option value="{{ option }}" {% if show_all|lower == option|lower|stringformat:"s" %}selected{% endif %}>
                                                {{ option|capfirst }}
                                            </option>
                                        {% endfor %}
                                    </select>
                                    &nbsp;&nbsp;
                                    <b>Bulk:</b>&nbsp;&nbsp; 
                                    <select name="bulk_operations" id="bulk_operations"  onchange="this.form.submit()">
                                        <option value="none" {% if 'none' in selected_bulk_operations %}selected{% endif %}>-- Ops --</option>
                                        <option value="bulk_done" {% if 'bulk_done' in selected_bulk_operations %}selected{% endif %}>Done</option>
                                        <option value="bulk_not_done" {% if 'bulk_not_done' in selected_bulk_operations %}selected{% endif %}>Not Done</option>
                                        <option value="bulk_blocked" {% if 'bulk_blocked' in selected_bulk_operations %}selected{% endif %}>Blocked</option>
                                        <option value="bulk_delete" {% if 'bulk_delete' in selected_bulk_operations %}selected{% endif %}>Delete</option>
                                    </select>                  
                                </th>
                            </tr>
                        </thead>

                        <tbody  id="sortable" class="sortable-tbody">
                            {% for tobject in page_obj %}
                            <tr id="{{tobject.id}}_{{ forloop.counter }}" class="sortable-row display_tr">
                                <td class="drag-handle">
                                    <i class="bi bi-grip-vertical"></i>
                                </td>
                                <td width="2%">
                                    <input type="checkbox" name="selected_item" id="selected_item_ids" value="{{tobject.id}}">
                                </td>
                                <td>{{forloop.counter}}</td>
                                <td width="20%" ondblclick="makeEditable(this)"
                                 onblur="save_element_text(this, '{{ tobject.id }}',  '___APPNAME___', '___MODELNAME___', 'name')"
                                ><strong>{{tobject.name}}</strong></td>
                                <td width="" ondblclick="makeEditable(this)"
                                onblur="save_element_text(this, '{{ tobject.id }}',  '___APPNAME___', '___MODELNAME___', 'description')"
                                >{% if tobject.description != None %}{{tobject.description}}{% endif %}</td>
                                <td width="20%">
                                    {% include './connected____pluralmodname___.html' %}
                                </td>
                                <td width="50%">
                                    <a href="{% url 'view____singularmodname___'   tobject.id  %}"
                                    class="btn btn-sm btn-primary"><i class="bi bi-eye"></i></a>
                                    &nbsp;&nbsp;
                                    <a href="{% url 'edit____singularmodname___'   tobject.id %}"
                                    class="btn btn-sm btn-warning"><i class="bi bi-pencil-square"></i></a>
                                    &nbsp;&nbsp;
                                    <a href="{% url 'delete____singularmodname___'   tobject.id %}"
                                    class="btn btn-sm btn-danger"><i class="bi bi-x-square"></i></a>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                            <tr>
                                <td colspan="7">
                                    {% include 'app_common/common_files/pagination.html' %}
                                </td>
                            </tr>                        
                    </table>
                <!-- end display -->
        </div>
    </div>
  
</div>
<div class="trash-icon">
    {% if deleted_count > 0 %}
    <a href="{% url 'list_deleted____pluralmodname___' %}"><i class="bi bi-trash-fill"></i></a>    
    {% endif %}
</div>
</form>
<script>
// Select all / checkbox
function checkUncheck(checkBox) {
    get = document.getElementsByName('selected_item');
    for(var i=0; i<get.length; i++) {
        get[i].checked = checkBox.checked;
    }
}
</script>

<script>
    // pagination select
document.addEventListener("DOMContentLoaded", function () {
  const redirectSelect = document.getElementById("paginationselect");
  redirectSelect.addEventListener("change", function () {
    const selectedValue = redirectSelect.value;
    
    // Redirect the user based on the selected value
    if (selectedValue === "5") {
      window.location.href = "{% url 'list____pluralmodname___'  %}?page=1&all=5";
    } else if (selectedValue === "10") {
      window.location.href = "{% url 'list____pluralmodname___'  %}?page=1&all=10";
    } else if (selectedValue === "15") {
      window.location.href = "{% url 'list____pluralmodname___'  %}?page=1&all=15";
    } else if (selectedValue === "25") {
      window.location.href = "{% url 'list____pluralmodname___'   %}?page=1&all=25";
    } else if (selectedValue === "50") {
      window.location.href = "{% url 'list____pluralmodname___'  %}?page=1&all=50";
    } else if (selectedValue === "100") {
      window.location.href = "{% url 'list____pluralmodname___'  %}?page=1&all=100";
    } else if (selectedValue === "all") {
      window.location.href = "{% url 'list____pluralmodname___'  %}?page=1&all=all";
    } 
    // Add more conditions for other options as needed
  });
});
</script>

<script>
    $(".sortable_table").find("tbody").sortable({
      items: "> tr",
      handle: ".drag-handle",
      appendTo: "parent",
      cancel: "[contenteditable]",
      update: function(event, ui) {
              var serialOrder = $('#sortable').sortable('serialize');
              var arrayOrder = $('#sortable').sortable('toArray');
              //alert(arrayOrder);
              $.ajax({
                url: '/common/common_ajax/ajax_update_model_list_sorted/',
                type: 'POST',
                data : {
                  'csrfmiddlewaretoken': "{{ csrf_token }}",
                  'model_name': '___MODELNAME___',
                  'app_name': '___APPNAME___',
                  'sorted_list_data': JSON.stringify(arrayOrder),
                  
                },
                dataType: 'json',
                success: function(data) {
                  console.log(data);
                }
              })
            }
    });
</script>

<script>
    function makeEditable(element) {
        element.contentEditable = true;
        element.focus();
    }


    function save_element_text(element, id,  appName, modelName, fieldName) {
        element.contentEditable = false;
        $.ajax({
            url: '/common/common_ajax/ajax_save_element_text/',
            type: 'POST',
            data : {
            'csrfmiddlewaretoken': "{{ csrf_token }}",
            'model_name': modelName,
            'app_name': appName,
            'field_name': fieldName,
            'text': element.textContent, 
            'id': id,
            },
            dataType: 'json',
            success: function(data) {
            console.log(data);
            }
        })
    }
</script>
<!-- End: Content -->
{% endblock content %}
"""



list_deleted_objects_html_single_level = """
{% extends 'app_common/common_files/base_template.html' %}
{% load static %}
{% load crispy_forms_tags %}
{% load custom_tags %}
{% load app_web_my_filters %}
{% load markdown_extras  %}
{% block content %}

{% include 'app_common/common_files/navbar.html' %}

<!-- Begin: Content -->
<div class="container-fluid">
    <div class="row">
        <div class="col col-md-12">
            {% include '___APPNAME___/___modulepath___/breadcrumb____pluralmodname___.html' %}
        </div>
    </div>
</div>
<div class="container-fluid">
    <div class="row">
        <div class="col col-md-12">           
            <!-- display -->
            
            <div class="row">
                <div class="col col-md-12">
                    <div class="container-fluid-width">
                        <div class="row pb-2">
                            <div class="col col-md-8">
                                <b class="h2">___DISPMODNAME___</b>
                                &nbsp;&nbsp;
                                ___DISPMODNAME___ Deleted List
                                
                            </div>
                            <div class="col col-md-4 text-end">
                                <span class="display_count">{{objects_count}} ___singularmodname___(s)</span>
                                &nbsp;&nbsp;
                                <a href="{% url 'create____singularmodname___'   %}" 
                                class="btn btn-sm btn-success"><b>+ Create ___DISPMODNAMESINGULAR___</b></a>
                            </div>
                        </div>
                    </div>
                    <form method="post">
                    {% csrf_token %}
                    <table class="table table-bordered sortable_table">
                        <thead>
                            <tr>
                                <th width="2%"><i class="bi bi-grip-vertical"></i></th>
                                <th width="2%">
                                    <input type="checkbox" name="select_all" id="select_all" onclick='checkUncheck(this)'>
                                </th> 
                                <th width="2%">#</th>
                                <th>___DISPMODNAMESINGULAR___</th>
                                <th width="20%">Description</th>
                                <th width="10%">Configure</th>
                                <th width="50%">                                    
                                    Actions
                                    &nbsp;&nbsp;
                                    <select name="pagination" id="paginationselect">
                                        <option value="none" {% if selected_pagination == 'none' %}selected{% endif %}>-Page-</option>
                                        {% for option in pagination_options %}
                                            <option value="{{ option }}" {% if show_all|lower == option|lower|stringformat:"s" %}selected{% endif %}>
                                                {{ option|capfirst }}
                                            </option>
                                        {% endfor %}
                                    </select>
                                    &nbsp;&nbsp;
                                     <b>Bulk:</b>&nbsp;&nbsp; 
                                    <select name="bulk_operations" id="bulk_operations"  onchange="this.form.submit()">
                                        <option value="none" {% if 'none' in selected_bulk_operations %}selected{% endif %}>-- Ops --</option>                                     
                                        <option value="bulk_restore" {% if 'bulk_restore' in selected_bulk_operations %}selected{% endif %}>Restore</option>
                                        <option value="bulk_erase" {% if 'bulk_erase' in selected_bulk_operations %}selected{% endif %}>Erase</option>
                                    </select>                           
                                </th>
                            </tr>
                        </thead>

                        <tbody  id="sortable" class="sortable-tbody">
                            {% for tobject in page_obj %}
                            <tr id="{{tobject.id}}_{{ forloop.counter }}" class="sortable-row display_tr">
                                <td class="drag-handle">
                                    <i class="bi bi-grip-vertical"></i>
                                </td>
                                <td width="2%">
                                    <input type="checkbox" name="selected_item" id="selected_item_ids" value="{{tobject.id}}">
                                </td>
                                <td>{{forloop.counter}}</td>
                                <td width="20%"><strong>{{tobject.name}}</strong></td>
                                <td width="">{% if tobject.description != None %}{{tobject.description}}{% endif %}</td>
                                <td width="20%">
                                
                                </td>
                                <td width="50%">
                                    <a href="{% url 'view____singularmodname___'   tobject.id  %}"
                                    class="btn btn-sm btn-primary"><i class="bi bi-eye"></i></a>
                                    &nbsp;&nbsp;
                                    <a href="{% url 'edit____singularmodname___'   tobject.id %}"
                                    class="btn btn-sm btn-warning"><i class="bi bi-pencil-square"></i></a>
                                    &nbsp;&nbsp;
                                    <a href="{% url 'permanent_deletion____singularmodname___'   tobject.id %}"
                                    class="btn btn-sm btn-danger"><i class="bi bi-x-square"></i></a>
                                     &nbsp;&nbsp;
                                    <a href="{% url 'restore____singularmodname___'   tobject.id %}"
                                    class="btn btn-sm btn-success"><i class="bi bi-x-square"></i></a>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                            <tr>
                                <td colspan="7">
                                    {% include 'app_common/common_files/pagination.html' %}
                                </td>
                            </tr>                        
                    </table>
                <!-- end display -->
        </div>
    </div>
  
</div>
</form>
<script>
// Select all / checkbox
function checkUncheck(checkBox) {
    get = document.getElementsByName('selected_item');
    for(var i=0; i<get.length; i++) {
        get[i].checked = checkBox.checked;
    }
}
</script>

<script>
    // pagination select
document.addEventListener("DOMContentLoaded", function () {
  const redirectSelect = document.getElementById("paginationselect");
  redirectSelect.addEventListener("change", function () {
    const selectedValue = redirectSelect.value;
    
    // Redirect the user based on the selected value
    if (selectedValue === "5") {
      window.location.href = "{% url 'list____pluralmodname___'  %}?page=1&all=5";
    } else if (selectedValue === "10") {
      window.location.href = "{% url 'list____pluralmodname___'  %}?page=1&all=10";
    } else if (selectedValue === "15") {
      window.location.href = "{% url 'list____pluralmodname___'  %}?page=1&all=15";
    } else if (selectedValue === "25") {
      window.location.href = "{% url 'list____pluralmodname___'   %}?page=1&all=25";
    } else if (selectedValue === "50") {
      window.location.href = "{% url 'list____pluralmodname___'  %}?page=1&all=50";
    } else if (selectedValue === "100") {
      window.location.href = "{% url 'list____pluralmodname___'  %}?page=1&all=100";
    } else if (selectedValue === "all") {
      window.location.href = "{% url 'list____pluralmodname___'  %}?page=1&all=all";
    } 
    // Add more conditions for other options as needed
  });
});
</script>

<script>
    $(".sortable_table").find("tbody").sortable({
      items: "> tr",
      handle: ".drag-handle",
      appendTo: "parent",
      cancel: "[contenteditable]",
      update: function(event, ui) {
              var serialOrder = $('#sortable').sortable('serialize');
              var arrayOrder = $('#sortable').sortable('toArray');
              //alert(arrayOrder);
              $.ajax({
                url: '/common/common_ajax/ajax_update_model_list_sorted/',
                type: 'POST',
                data : {
                  'csrfmiddlewaretoken': "{{ csrf_token }}",
                  'model_name': '___MODELNAME___',
                  'app_name': '___APPNAME___',
                  'sorted_list_data': JSON.stringify(arrayOrder),
                  
                },
                dataType: 'json',
                success: function(data) {
                  console.log(data);
                }
              })
            }
    });
    </script>

<!-- End: Content -->
{% endblock content %}
"""



create_object_html_single_level = """
{% extends 'app_common/common_files/base_template.html' %}
{% load static %}
{% load crispy_forms_tags %}
{% load custom_tags %}
{% load app_web_my_filters %}
{% load markdown_extras  %}

{% block content %}
{% include 'app_common/common_files/navbar.html' %}
<div class="container-fluid">
    <div class="row">
        <div class="col col-md-12">
            {% include '___APPNAME___/___modulepath___/breadcrumb____pluralmodname___.html' %}
        </div>
    </div>
</div>
<!-- Begin: Content -->
<form method="post">
    {% csrf_token %}
    <div class="container-fluid">
        <div class="row">
            <div class="col col-md-12">
                <div class="container-fluid-width">
                    <div class="row">
                        <div class="col col-md-8">
                            <h2>{% if form.instance.pk %}Edit{% else %}Create{% endif %} 
                                ___DISPMODNAMESINGULAR___</h2>
                        </div>
                        <div class="col col-md-4 text-end">
                            <a href="{% url 'list____pluralmodname___' %}"
                             class="btn btn-sm btn-primary"><b>List ___DISPMODNAMESINGULAR___(s)</b></a>
                        </div>
                    </div>
                </div>
                <table class="table table-bordered">
                    <thead>
                        <tr>
                            <th colspan="2">{{page_title}}</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td width="15%">
                                <strong>___DISPMODNAMESINGULAR___</strong>
                            </td>
                            <td>
                                {{form.name|as_crispy_field}}
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <strong>Description</strong>
                            </td>
                            <td>
                                {{form.description|as_crispy_field}}
                            </td>
                        </tr>
                       <tr>
                            <td colspan="2" class="text-center"><button type="submit"
                                class="btn btn-sm btn-success">Save</button></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</form>
<script>
    focusField = document.getElementById('id_name');
    focusField.focus();
</script>

<!-- End: Content -->
{% endblock content %}
"""

edit_object_html_single_level = """
{% extends 'app_common/common_files/base_template.html' %}
{% load static %}
{% load crispy_forms_tags %}
{% load custom_tags %}
{% load app_web_my_filters %}
{% load markdown_extras  %}

{% block content %}
{% include 'app_common/common_files/navbar.html' %}

<div class="container-fluid">
    <div class="row">
        <div class="col col-md-12">
            {% include '___APPNAME___/___modulepath___/breadcrumb____pluralmodname___.html' %}
        </div>
    </div>
</div>
<!-- Begin: Content -->
<form method="post">
    {% csrf_token %}
    <div class="container-fluid">
        <div class="row">
            <div class="col col-md-12">
                <div class="container-fluid-width">
                    <div class="row">
                        <div class="col col-md-8">
                            <h2>{% if form.instance.pk %}Edit{% else %}Create{% endif %} 
                                ___DISPMODNAMESINGULAR___</h2>
                        </div>
                        <div class="col col-md-4 text-end">
                            <a href="{% url 'list____pluralmodname___'  %}"
                             class="btn btn-sm btn-primary"><b>List ___DISPMODNAMESINGULAR___(s)</b></a>
                        </div>
                    </div>
                </div>
                <table class="table table-bordered">
                    <thead>
                        <tr>
                            <th colspan="2">
                                <div class="container-fluid-width">
                                    <div class="row">
                                        <div class="col col-md-5">
                                            {{page_title}}:: {{form.instance}}
                                        </div>
                                        <div class="col col-md-7">
                                            <div class="text-end">
                                                <a href="{% url 'view____singularmodname___'  form.instance.id %}" class="btn btn-sm btn-primary"><b>View</b></a>
                                                &nbsp;&nbsp;&nbsp;
                                                <a href="{% url 'delete____singularmodname___'  form.instance.id %}" class="btn btn-sm btn-danger"><b>Delete</b></a>
                                                
                                            </div>
    
                                        </div>
                                    </div>
                                </div>
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td width="15%">
                                <strong>___DISPMODNAMESINGULAR___</strong>
                            </td>
                            <td>
                                {{form.name|as_crispy_field}}
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <strong>Description</strong>
                            </td>
                            <td>
                                {{form.description|as_crispy_field}}
                            </td>
                        </tr>
                       <tr>
                            <td colspan="2" class="text-center"><button type="submit"
                                class="btn btn-sm btn-success">Save</button></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</form>
<script>
    focusField = document.getElementById('id_name');
    focusField.focus();
</script>

<!-- End: Content -->
{% endblock content %}
"""

delete_object_html_single_level = """
{% extends 'app_common/common_files/base_template.html' %}
{% load static %}
{% load crispy_forms_tags %}
{% load custom_tags %}
{% load app_web_my_filters %}
{% load markdown_extras  %}

{% block content %}
{% include 'app_common/common_files/navbar.html' %}

<div class="container-fluid">
    <div class="row">
        <div class="col col-md-12">
            {% include '___APPNAME___/___modulepath___/breadcrumb____pluralmodname___.html' %}
        </div>
    </div>
</div>
<!-- Begin: Content -->
<form method="post">
    {% csrf_token %}
    <div class="container-fluid">
        <div class="row">
            <div class="col col-md-12">
                <div class="container-fluid-width">
                    <div class="row">
                        <div class="col col-md-8">
                            <h2>Delete 
                                ___DISPMODNAMESINGULAR___ :: {{object}}</h2>
                        </div>
                        <div class="col col-md-4 text-end">
                            <a href="{% url 'list____pluralmodname___'  %}"
                             class="btn btn-sm btn-primary"><b>List ___DISPMODNAMESINGULAR___(s)</b></a>
                        </div>
                    </div>
                </div>
                <table class="table table-bordered">
                    <thead>
                        <tr>
                            <div class="container-fluid-width">
                                <div class="row">
                                    <div class="col col-md-5">
                                        {{page_title}}:: {{object}}
                                    </div>
                                    <div class="col col-md-7">
                                        <div class="text-end">
                                            <a href="{% url 'edit____singularmodname___'  object.id %}" class="btn btn-sm btn-primary"><b>Edit</b></a>
                                            &nbsp;&nbsp;&nbsp;
                                            <a href="{% url 'view____singularmodname___'  object.id %}" class="btn btn-sm btn-danger"><b>View</b></a>
                                            
                                        </div>

                                    </div>
                                </div>
                            </div>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                          <td colspan="2" class="text-center">
                            <div class="row">
                                <div class="col col-md-12 text-center">
                                    <p>Are you sure you want to delete "{{ object.name }}"?</p>
                                    <form method="post">
                                        {% csrf_token %}
                                        <button type="submit" class="btn btn-sm btn-danger">Confirm</button> 
                                        &nbsp;&nbsp;&nbsp;
                                        <a href="{% url 'list____pluralmodname___'  %}" class="btn btn-sm btn-warning">Cancel</a>
                                    </form>
                                </div>
                            </div>
                          </td>
                        </tr>
                      
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</form>
<!-- End: Content -->
{% endblock content %}
"""

permanent_deletion_object_html_single_level = """
{% extends 'app_common/common_files/base_template.html' %}
{% load static %}
{% load crispy_forms_tags %}
{% load custom_tags %}
{% load app_web_my_filters %}
{% load markdown_extras  %}

{% block content %}
{% include 'app_common/common_files/navbar.html' %}

<div class="container-fluid">
    <div class="row">
        <div class="col col-md-12">
            {% include '___APPNAME___/___modulepath___/breadcrumb____pluralmodname___.html' %}
        </div>
    </div>
</div>
<!-- Begin: Content -->
<form method="post">
    {% csrf_token %}
    <div class="container-fluid">
        <div class="row">
            <div class="col col-md-12">
                <div class="container-fluid-width">
                    <div class="row">
                        <div class="col col-md-8">
                            <h2>Permanent Deletion
                                ___DISPMODNAMESINGULAR___ :: {{object}}</h2>
                        </div>
                        <div class="col col-md-4 text-end">
                            <a href="{% url 'list____pluralmodname___'  %}"
                             class="btn btn-sm btn-primary"><b>List ___DISPMODNAMESINGULAR___(s)</b></a>
                        </div>
                    </div>
                </div>
                <table class="table table-bordered">
                    <thead>
                        <tr>
                            <div class="container-fluid-width">
                                <div class="row">
                                    <div class="col col-md-5">
                                        Permanently Deleting this record. Only Admins can recover.
                                    </div>
                                    <div class="col col-md-7">
                                        <div class="text-end">
                                            <a href="{% url 'edit____singularmodname___'  object.id %}" class="btn btn-sm btn-primary"><b>Edit</b></a>
                                            &nbsp;&nbsp;&nbsp;
                                            <a href="{% url 'view____singularmodname___'  object.id %}" class="btn btn-sm btn-danger"><b>View</b></a>
                                            
                                        </div>

                                    </div>
                                </div>
                            </div>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                          <td colspan="2" class="text-center">
                            <div class="row">
                                <div class="col col-md-12 text-center">
                                    <p>Are you sure you want to <b>PERMANENTLY</b> delete "{{ object.name }}"?</p>
                                    <form method="post">
                                        {% csrf_token %}
                                        <button type="submit" class="btn btn-sm btn-danger">Confirm</button> 
                                        &nbsp;&nbsp;&nbsp;
                                        <a href="{% url 'list____pluralmodname___'  %}" class="btn btn-sm btn-warning">Cancel</a>
                                    </form>
                                </div>
                            </div>
                          </td>
                        </tr>
                      
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</form>
<!-- End: Content -->
{% endblock content %}
"""

view_object_html_single_level = """
{% extends 'app_common/common_files/base_template.html' %}
{% load static %}
{% load crispy_forms_tags %}
{% load custom_tags %}
{% load app_web_my_filters %}

{% block content %}
{% include 'app_common/common_files/navbar.html' %}

<div class="container-fluid">
    <div class="row">
        <div class="col col-md-12">
            {% include '___APPNAME___/___modulepath___/breadcrumb____pluralmodname___.html' %}
        </div>
    </div>
</div>
<!-- Begin: Content -->
<form method="post">
    {% csrf_token %}
    <div class="container-fluid">
        <div class="row">
            <div class="col col-md-12">
                <div class="container-fluid-width">
                    <div class="row">
                        <div class="col col-md-8">
                            <h2>View 
                                ___DISPMODNAME___ :: {{object}}</h2>
                        </div>
                        <div class="col col-md-4 text-end">
                            <a href="{% url 'list____pluralmodname___'  %}"
                             class="btn btn-sm btn-primary"><b>List ___DISPMODNAME___</b></a>
                        </div>
                    </div>
                </div>
                <table class="table table-bordered">
                    <thead>
                        <tr>
                            <th colspan="2">
                                <div class="container-fluid-width">
                                    <div class="row">
                                        <div class="col col-md-5">
                                            {{page_title}}:: {{object}}
                                        </div>
                                        <div class="col col-md-7">
                                            <div class="text-end">
                                                <a href="{% url 'edit____singularmodname___'  object.id %}" class="btn btn-sm btn-primary"><b>Edit</b></a>
                                                &nbsp;&nbsp;&nbsp;
                                                <a href="{% url 'delete____singularmodname___'  object.id %}" class="btn btn-sm btn-danger"><b>Delete</b></a>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td width="15%">
                                <strong>___DISPMODNAMESINGULAR___</strong>
                            </td>
                            <td>
                                {{object.name}}
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <strong>Description</strong>
                            </td>
                            <td>
                                {{object.description}}
                            </td>
                        </tr>                       
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</form>
<!-- End: Content -->
{% endblock content %}
"""


breadcrumb_html = """
{% load static %}
{% load crispy_forms_tags %}
{% load custom_tags %}
{% load app_web_my_filters %}
{% load markdown_extras  %}
 <!-- Begin: Breadcrumb -->
  <style>
    .breadcrumb {
        font-size: 14px;
    }
 </style>
 <div class="breadcrumb">
    <nav aria-label="breadcrumb"> <!-- Inline style for demonstration -->
        <ol class="breadcrumb">
            <li class="breadcrumb-item">
                <a href="/">
                    <i class="bi bi-house"></i> Home
                </a>
            </li>
          
            <li class="breadcrumb-item active" aria-current="page">
                <a href="{% url 'list____pluralmodname___'  %}">___MODNAME___</a></li>
        
            <!-- decide based on the page -->
                
            {% if page|starts_with_any:"create_,edit_,delete_,view_" %}
                 <li class="breadcrumb-item active" aria-current="page">
                 ___DISPMODNAME___
                </li>
            {% else  %}             
                 <li class="breadcrumb-item active" aria-current="page">
                 ___DISPMODNAME___
                </li>
            {% endif %}
        </ol>
    </nav>
</div>
<!-- End: Breadcrumb -->
"""

urls_py = """
from django.urls import path, include

from ___APPNAME___.mod____singularmodname___ import views____singularmodname___

urlpatterns = [
    # ___APPNAME___/___pluralmodname___: DB/Model: ___MODELNAME___
    path('list____pluralmodname___/', views____singularmodname___.list____pluralmodname___, name='list____pluralmodname___'),
    path('list_deleted____pluralmodname___/', views____singularmodname___.list_deleted____pluralmodname___, name='list_deleted____pluralmodname___'),
    path('create____singularmodname___/', views____singularmodname___.create____singularmodname___, name='create____singularmodname___'),
    path('edit____singularmodname___/<int:___directid___>/', views____singularmodname___.edit____singularmodname___, name='edit____singularmodname___'),
    path('delete____singularmodname___/<int:___directid___>/', views____singularmodname___.delete____singularmodname___, name='delete____singularmodname___'),
    path('permanent_deletion____singularmodname___/<int:___directid___>/', views____singularmodname___.permanent_deletion____singularmodname___, name='permanent_deletion____singularmodname___'),
    path('restore____singularmodname___/<int:___directid___>/', views____singularmodname___.restore____singularmodname___, name='restore____singularmodname___'),
    path('view____singularmodname___/<int:___directid___>/', views____singularmodname___.view____singularmodname___, name='view____singularmodname___'),
]
"""


## models 
models_py = """
from ___APPNAME___.mod_app.all_model_imports import *
from app_common.mod_common.models_common import *

class ___MODELNAME___(BaseModelImpl):
    #org = models.ForeignKey('', on_delete=models.CASCADE, related_name="org_")
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author____MODELNAME___")
   
        
    def __str__(self):
        return self.name
"""

## views

list_objects_view_py = """
from ___APPNAME___.mod_app.all_view_imports import *
from ___APPNAME___.mod____singularmodname___.models____singularmodname___ import *
from ___APPNAME___.mod____singularmodname___.forms____singularmodname___ import *

app_name = '___APPNAME___'
app_version = '___appversion___'

module_name = '___pluralmodname___'
module_path = f'___modulepath___'

# viewable flag
first_viewable_flag = '__ALL__'  # 'all' or '__OWN__'
viewable_flag = '__ALL__'  # 'all' or '__OWN__'
# Setup dictionaries based on flags
viewable_dict = {} if viewable_flag == '__ALL__' else {'author': user}
first_viewable_dict = {} if first_viewable_flag == '__ALL__' else {'author': user}
def get_viewable_dicts(user, viewable_flag, first_viewable_flag):
    viewable_dict = {} if viewable_flag == '__ALL__' else {'author': user}
    first_viewable_dict = {} if first_viewable_flag == '__ALL__' else {'author': user}
    return viewable_dict, first_viewable_dict
# ============================================================= #
@login_required
def list____pluralmodname___(request):
    # take inputs
    # process inputs
    user = request.user       
    objects_count = 0    
    show_all = request.GET.get('all', '25')
    objects_per_page = int(show_all) if show_all != 'all' else 25
    pagination_options = [5, 10, 15, 25, 50, 100, 'all']
    selected_bulk_operations = None
    search_query = request.GET.get('search', '')
    deleted_count = 0
    
    if search_query:
        tobjects = ___MODELNAME___.objects.filter(name__icontains=search_query, 
                                            active=True,deleted=False, **viewable_dict ).order_by('position')
        deleted = ___MODELNAME___.objects.filter(active=False, deleted=False,**viewable_dict).order_by('position')
        deleted_count = deleted.count()
    else:
        tobjects = ___MODELNAME___.objects.filter(active=True).order_by('position')
        deleted = ___MODELNAME___.objects.filter(active=False, deleted=False,**viewable_dict).order_by('position')
        deleted_count = deleted.count()
    
    if show_all == 'all':
        # No pagination, show all records
        page_obj = tobjects
        objects_per_page = tobjects.count()
    else:
        print(f">>> === show_all: {show_all} === <<<")   
        objects_per_page = int(show_all)     
        paginator = Paginator(tobjects, objects_per_page)  # Show 10 tobjects per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    
    objects_count = tobjects.count()
    
    ## processing the POST
    if request.method == 'POST':
        selected_bulk_operations = request.POST.getlist('bulk_operations')
        bulk_operation = str(selected_bulk_operations[0].strip()) if selected_bulk_operations else None
            
        if 'selected_item' in request.POST:  
            selected_items = request.POST.getlist('selected_item')  # Use getlist to ensure all are captured
            for item_id in selected_items:
                item = int(item_id)  
                if bulk_operation == 'bulk_delete':
                    object = get_object_or_404(___MODELNAME___, pk=item, active=True, **viewable_dict)
                    object.active = False
                    object.save()
                    
                elif bulk_operation == 'bulk_done':
                    object = get_object_or_404(___MODELNAME___, pk=item, active=True, **viewable_dict)
                    object.done = True
                    object.save()
                    
                elif bulk_operation == 'bulk_not_done':
                    object = get_object_or_404(___MODELNAME___, pk=item, active=True, **viewable_dict)
                    object.done = False
                    object.save()
                    
                elif bulk_operation == 'bulk_blocked':  # Correct the operation check here
                    object = get_object_or_404(___MODELNAME___, pk=item, active=True, **viewable_dict)
                    object.blocked = True
                    object.save()
                    
                else:
                    return redirect('list____pluralmodname___')
            return redirect('list____pluralmodname___')
    
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list____pluralmodname___',
        
        'module_path': module_path,
        'user': user,
        'tobjects': tobjects,
        'page_obj': page_obj,
        'objects_count': objects_count,
        'objects_per_page': objects_per_page,
        'deleted_count': deleted_count,
        'show_all': show_all,
        'pagination_options': pagination_options,
        'selected_bulk_operations': selected_bulk_operations,

        'page_title': f'___MODNAME___ List',
    }       
    template_file = f"{app_name}/{module_path}/list____pluralmodname___.html"
    return render(request, template_file, context)

"""

list_deleted_objects_view_py = """
# list the deleted objects
# ============================================================= #
@login_required
def list_deleted____pluralmodname___(request):
    # take inputs
    # process inputs
    user = request.user        
    objects_count = 0    
    show_all = request.GET.get('all', '25')
    objects_per_page = int(show_all) if show_all != 'all' else 25
    pagination_options = [5, 10, 15, 25, 50, 100, 'all']
    selected_bulk_operations = None

    show_all = request.GET.get('all', '25')
    objects_per_page = int(show_all) if show_all != 'all' else 25
    
    search_query = request.GET.get('search', '')
    if search_query:
        tobjects = ___MODELNAME___.objects.filter(name__icontains=search_query, 
                                            **viewable_dict, active=False, deleted=False).order_by('position')
    else:
        tobjects = ___MODELNAME___.objects.filter(active=False, deleted=False, **viewable_dict).order_by('position')
    
    if show_all == 'all':
        # No pagination, show all records
        page_obj = tobjects
        objects_per_page = tobjects.count()
    else:
        print(f">>> === show_all: {show_all} === <<<")   
        objects_per_page = int(show_all)     
        paginator = Paginator(tobjects, objects_per_page)  # Show 10 tobjects per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    objects_count = tobjects.count()
    
    ## processing the POST
    if request.method == 'POST':
        selected_bulk_operations = request.POST.getlist('bulk_operations')
        bulk_operation = str(selected_bulk_operations[0].strip()) if selected_bulk_operations else None
            
        if 'selected_item' in request.POST:  
                selected_items = request.POST.getlist('selected_item')  # Use getlist to ensure all are captured
                for item_id in selected_items:
                    item = int(item_id)  
                    if bulk_operation == 'bulk_restore':
                        object = get_object_or_404(___MODELNAME___, pk=item, active=False, **viewable_dict)
                        object.active = True               
                        object.save()
                    elif bulk_operation == 'bulk_erase':
                        object = get_object_or_404(___MODELNAME___, pk=item, active=False, **viewable_dict)
                        object.active = False  
                        object.deleted = True             
                        object.save()
                    else:
                        return redirect('list_deleted____pluralmodname___')
                return redirect('list_deleted____pluralmodname___')
    
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_deleted____pluralmodname___',
        
        'module_path': module_path,
        'user': user,
        'tobjects': tobjects,
        'page_obj': page_obj,
        'objects_count': objects_count,
        'objects_per_page': objects_per_page,
        'show_all': show_all,
        'pagination_options': pagination_options,
        'selected_bulk_operations': selected_bulk_operations,

        'page_title': f'___MODNAME___ List',
    }       
    template_file = f"{app_name}/{module_path}/list_deleted____pluralmodname___.html"
    return render(request, template_file, context)



"""



create_object_view_py = """
# Create View
@login_required
def create____singularmodname___(request):
    user = request.user
    
    if request.method == 'POST':
        form = ___MODELNAME___Form(request.POST)
        if form.is_valid():
            form.instance.author = user
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list____pluralmodname___')
    else:
        form = ___MODELNAME___Form()

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'create____singularmodname___',
        
        'module_path': module_path,
        'form': form,
        'page_title': f'Create ___DISPMODNAMESINGULAR___',
    }
    template_file = f"{app_name}/{module_path}/create____singularmodname___.html"
    return render(request, template_file, context)


"""
view_object_view_py = """
@login_required
def view____singularmodname___(request,  ___directid___):
    user = request.user
    
    object = get_object_or_404(___MODELNAME___, pk=___directid___, active=True, **viewable_dict)    

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'view____singularmodname___',
        
        'module_path': module_path,
        'object': object,
        'page_title': f'View ___DISPMODNAMESINGULAR___',
    }
    template_file = f"{app_name}/{module_path}/view____singularmodname___.html"
    return render(request, template_file, context)

"""
edit_object_view_py = """
# Edit
@login_required
def edit____singularmodname___(request, ___directid___):
    user = request.user
    
    object = get_object_or_404(___MODELNAME___, pk=___directid___, active=True, **viewable_dict)
    if request.method == 'POST':
        form = ___MODELNAME___Form(request.POST, instance=object)
        if form.is_valid():
            form.instance.author = user
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list____pluralmodname___')
    else:
        form = ___MODELNAME___Form(instance=object)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'edit____singularmodname___',
        
        'module_path': module_path,
        'form': form,
        'object': object,
        'page_title': f'Edit ___DISPMODNAMESINGULAR___',
    }
    template_file = f"{app_name}/{module_path}/edit____singularmodname___.html"
    return render(request, template_file, context)

"""
delete_object_view_py = """
@login_required
def delete____singularmodname___(request, ___directid___):
    user = request.user
    
    object = get_object_or_404(___MODELNAME___, pk=___directid___, active=True, **viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.save()
        return redirect('list____pluralmodname___')

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'delete____singularmodname___',
        
        'module_path': module_path,        
        'object': object,
        'page_title': f'Delete ___DISPMODNAMESINGULAR___',
    }
    template_file = f"{app_name}/{module_path}/delete____singularmodname___.html"
    return render(request, template_file, context)
"""

restore_object_view_py = """
@login_required
def restore____singularmodname___(request, ___directid___):
    user = request.user
    object = get_object_or_404(___MODELNAME___, pk=___directid___, active=False, **viewable_dict)
    object.active = True
    object.save()
    return redirect('list____pluralmodname___')
   
"""
permanent_deletion_object_view_py = """
@login_required
def permanent_deletion____singularmodname___(request, ___directid___):
    user = request.user
    
    object = get_object_or_404(___MODELNAME___, pk=___directid___, active=False, deleted=False, **viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.deleted = True
        object.save()
        return redirect('list____pluralmodname___')

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'permanent_deletion____singularmodname___',
        
        'module_path': module_path,        
        'object': object,
        'page_title': f'Permanent Deletion ___DISPMODNAMESINGULAR___',
    }
    template_file = f"{app_name}/{module_path}/permanent_deletion____singularmodname___.html"
    return render(request, template_file, context)
"""
###############################################################################


import inflect
import sys 
import os
from utils.utils import *
p = inflect.engine()

#####################################################################
# configuration
# example2: Model -> model use _views_with_org.py to propogate org
version = "v1"
app_name = "app_automate"
module_name = "content"

if len(sys.argv) < 2:
    print("Usage: python TOP_LEVEL_CRUD.py  <projectname>.<app_name> <module_name:Organization>")
    sys.exit(1)  # Exit the program indicating that there was an issue
# Extract the script name without the '.py' extension
script_name = os.path.splitext(os.path.basename(__file__))[0]
# Read arguments
project_app_input = sys.argv[1]
project_name = project_app_input.split(".")[0]
app_name = project_app_input.split(".")[1]
app_name = app_name.lower()
app_name = f"app_{app_name}"
ref_module_name = sys.argv[2]

module_name = format_title_re(ref_module_name)
model_name = module_name.title() # Title Content / ContentType for ORM Model
model_name = model_name.replace("_", "")
db_app_name = module_name.lower()

direct_id = module_name.lower() + "_id"
#module_path_prefix = app_name.split("_")[1]
#module_path = f"{module_path_prefix}/{module_name}"
module_path = f"mod_{module_name}"



#######################################################################

display_module_name = module_name.replace('_', ' ').title()
#display_module_name_singular = p.singular_noun(display_module_name)
display_module_name_singular = display_module_name if p.singular_noun(display_module_name) is False else p.singular_noun(display_module_name)
#singular_module_name = p.singular_noun(module_name)
singular_module_name = module_name if p.singular_noun(module_name) is False else p.singular_noun(module_name)
plural_module_name = module_name if p.singular_noun(module_name) else p.plural(module_name)

lc_singular_module_name = singular_module_name.lower()
lc_plural_module_name = module_name.lower() if p.singular_noun(module_name) else p.plural(module_name)

print(f">>> === singular_module_name: {lc_singular_module_name} === <<<")
print(f">>> === plural_module_name: {lc_plural_module_name} === <<<")


############################################# END OF CODE #############################################
var_value_dict = {
    "___APPNAME___": app_name,
    "___MODNAME___": module_name.capitalize(),
    "___DISPMODNAME___": display_module_name,
    "___DISPMODNAMESINGULAR___": display_module_name_singular,
    "___singularmodname___": singular_module_name.lower(),
    "___pluralmodname___": lc_plural_module_name,
    "___UCsingularmodname___": singular_module_name.capitalize(),
    "___MODELNAME___": model_name,
    "___dbappname___": db_app_name,
   
    "___directid___": direct_id,
    "___appversion___": version,
    "___modulepath___": module_path,
    
}


html_var_list = [
    list_objects_html_single_level,
    list_deleted_objects_html_single_level,
    create_object_html_single_level,
    edit_object_html_single_level,
    delete_object_html_single_level,
    permanent_deletion_object_html_single_level,
    view_object_html_single_level,
    breadcrumb_html,
    connected_to_organization_links_html,
]

views_var_list = [
    list_objects_view_py,
    list_deleted_objects_view_py,
    create_object_view_py,
    edit_object_view_py,
    delete_object_view_py,
    permanent_deletion_object_view_py,
    restore_object_view_py,
    view_object_view_py
]

urls_var_list = [
    urls_py,
]

forms_var_list = [
    forms_py
]

models_var_list = [
    models_py
]

html_files_list = [
    f"list_{lc_plural_module_name}.html",
    f"list_deleted_{lc_plural_module_name}.html",
    f"create_{lc_singular_module_name}.html",
    f"edit_{lc_singular_module_name}.html",
    f"delete_{lc_singular_module_name}.html",
    f"permanent_deletion_{lc_singular_module_name}.html",
    f"view_{lc_singular_module_name}.html",
    f"breadcrumb_{lc_plural_module_name}.html",
    f"connected_{lc_plural_module_name}.html",
]
views_files_list = [f"views_{lc_singular_module_name}.py"]
urls_files_list = [f"urls_{lc_singular_module_name}.py"]
forms_files_list = [f"forms_{lc_singular_module_name}.py"]
models_files_list = [f"models_{lc_singular_module_name}.py"]
# File processing functions

def replace_all_vars_with_values(var_value_dict, file_data):
    for var, value in var_value_dict.items():
        file_data = file_data.replace(var, value)
    return file_data

def write_file(file_name, file_data):
    open(file_name, "w").write(file_data)
def process_file_str(file_str, var_value_dict):
    file_str = replace_all_vars_with_values(var_value_dict, file_str)
    return file_str

# Define dictionaries to hold file lists and variable lists for each module
file_lists = {
    "html": html_files_list,
    "views": views_files_list,
    "urls": urls_files_list,
    "forms": forms_files_list,
    "models": models_files_list,
}

var_lists = {
    "html": html_var_list,
    "views": views_var_list,
    "urls": urls_var_list,
    "forms": forms_var_list,
    "models": models_var_list,
}
## outcome folder
outcome = f"../outcome/{script_name}"
process_modules = ["html", "views", "urls", "forms", "models"]

if not os.path.exists(outcome):
    os.makedirs(outcome)
    os.makedirs(f"{outcome}/python")
    os.makedirs(f"{outcome}/html")
else:
    shutil.rmtree(outcome)
    os.makedirs(outcome)
    os.makedirs(f"{outcome}/python")
    os.makedirs(f"{outcome}/html")
    print(f">>> === {outcome} cleaned, dir ready === <<<")

for module in process_modules:
    # Access the appropriate lists from the dictionaries
    current_files_list = file_lists[module]
    current_var_list = var_lists[module]

    # Special handling for views module
    if module == "views":
        # Assume lc_plural_module_name is defined somewhere globally or passed into this context
        view_file_name = f"{outcome}/python/views_{lc_singular_module_name}.py"
        with open(view_file_name, "w") as file:
            file.write("")
        with open(view_file_name, "a+") as file:
            # Process each view content part with variable replacements before writing
            views_content = [
                list_objects_view_py,
                list_deleted_objects_view_py,
                create_object_view_py,
                edit_object_view_py,
                delete_object_view_py,
                permanent_deletion_object_view_py,
                restore_object_view_py,
                view_object_view_py
            ]
            for content in views_content:
                processed_content = process_file_str(content, var_value_dict)
                file.write(processed_content)
                file.write("\n")  # Optionally add a newline for better readability
    else:
        # Iterate over each html_var and corresponding html_file
        for dest_file, html_var in zip(current_files_list, current_var_list):
            print(f">>> === Processing File: {dest_file} === <<<")

            # Process the html_var with multiple replacements
            processed_html = process_file_str(html_var, var_value_dict)
            
            # Print the processed HTML for debugging
            html_dir = f"{outcome}/html/{module_name}"
            os.makedirs(html_dir) if not os.path.exists(html_dir) else None
            print(f">>> === created html_dir: {html_dir} === <<<\n{processed_html}")
            # Print the processed HTML for debugging
            print(f">>> === Processed Content for {dest_file}: === <<<\n{processed_html}")
            dest_file = f"{html_dir}/{dest_file}" if dest_file.endswith(".html") else f"{outcome}/python/{dest_file}"
            # Write the processed content to the corresponding HTML file
            with open(dest_file, "w") as file:
                file.write(processed_html)

# Special handling for urls module
project_dir = f"../../dev_env/project_area/env_{project_name}/{project_name}"
app_dirname = f"{app_name}"
dest_dir = f"{project_dir}/{app_dirname}/templates/{app_dirname}/mod_{module_name}"
copy_files(html_dir, dest_dir, html_files_list)

# copy the python files
src_python_files = f"{outcome}/python"
des_python_dir = f"{project_dir}/{app_dirname}/mod_{module_name}"
copy_directory_contents(src_python_files, des_python_dir)