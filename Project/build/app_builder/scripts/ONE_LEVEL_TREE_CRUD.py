import inflect
import sys 
import os

from utils.utils import *
p = inflect.engine()

version = "v1"
app_name = "app_automate"
module_name = "content"

if len(sys.argv) < 2:
    print("Usage: python ONE_LEVEL_TREE_CRUD.py  <projectname>.<app_name> <connectappname>.<connect_model:Organization> <module_name:BacklogSuperType/BacklogType/Backlog>")
    sys.exit(1)  
#
# Usage:
#  python script_name.py project1.app_backlog app_organization.Organization backlog
#
#

# Remove the .py / script extension
script_name = os.path.splitext(os.path.basename(__file__))[0]
# Read arguments
# first argument
project_app_name = sys.argv[1].lower()
project_name = project_app_name.split(".")[0]
app_name = project_app_name.split(".")[1]
app_name = f"app_{app_name}"
# second argument
connect_full_details = sys.argv[2]
connect_app_name = connect_full_details.split(".")[0]
connect_module_ip = connect_full_details.split(".")[1]
connect_app_name = f"app_{connect_app_name}"
# third argument
ref_module_name = sys.argv[3]
ip_module_title = ref_module_name.title()

##################################################################################
## connected module definitions
connect_module_title = connect_module_ip.title()
lc_connect_module_ip = connect_module_ip.lower()
connectstr = process_word(connect_module_ip).lower()  # Organization => org
connectid = process_word(connect_module_ip).lower() + "_id" # org_id
## all the connect related work
db_connect_name = connect_module_ip.capitalize() # like Organization, Enterprise etc.,
query_connect_name = connect_module_ip.lower() # like organization, enterprise etc.,

# root module name is the first module name
connect_convert = connect_module_ip.lower()
lc_singular_connect_name = connect_convert.lower()
lc_plural_connect_name = connect_convert.lower() if p.singular_noun(connect_convert) else p.plural(connect_convert)
    


##################################################################################

def create_variables(app_name, current_module_name):
    # convert the input ContentType into content_type add underscore
    module_name = format_title_re(current_module_name)
    # Convert words into Title contenttype into ContentType
    model_name = module_name.title() 
    # Remove underscore if any
    model_name = model_name.replace("_", "")
    db_app_name = module_name.lower()

    direct_id = module_name.lower() + "_id"
    # take the app_<name> name part 
    module_path_prefix = app_name.split("_")[1] 
    # app_name/module_name is the convention => 
    # templates/app_name/module_path_prefix/module_name
    module_path = f"mod_{module_name}"

    first_model = "EMPTY" # this is used when top level one is connected like Org / Level etc.,

    first_id_fk_ref = process_word(first_model).lower() 
    first_model_name_import = first_model if p.singular_noun(first_model) else p.plural(first_model)
    first_model_name_import = first_model_name_import.lower()

    first_id = process_word(first_model).lower() + "_id"
    first_name = first_model.lower()
    first_model_name = first_model.title()

    #######################################################################

    display_module_name = module_name.replace('_', ' ').title()
    display_module_name_singular = display_module_name if p.singular_noun(display_module_name) is False else p.singular_noun(display_module_name)
    display_module_name_plural = display_module_name if p.singular_noun(display_module_name) else p.plural(display_module_name)
    
    singular_module_name = module_name if p.singular_noun(module_name) is False else p.singular_noun(module_name)
    plural_module_name = module_name if p.singular_noun(module_name) else p.plural(module_name)

    lc_singular_module_name = singular_module_name.lower()
    lc_plural_module_name = module_name.lower() if p.singular_noun(module_name) else p.plural(module_name)
    
    
    # root module name is the first module name
    lc_singular_root_module_name = ref_module_name.lower()
    lc_plural_root_module_name = ref_module_name.lower() if p.singular_noun(ref_module_name) else p.plural(ref_module_name)
    
    
    variables = {
        "app_name": app_name,
        "connect_module_title": connect_module_title, 
        "lc_connect_module_ip": lc_connect_module_ip,
        "db_connect_name": db_connect_name, 
        "connectstr": connectstr, # org
        "connectid": connectid, # org_id
        "connect_app_name": connect_app_name,
        "lc_singular_connect_name": lc_singular_connect_name,
        "lc_plural_connect_name": lc_plural_connect_name,
        
        "module_name": current_module_name.lower(),
        "version": version,
        "dbmodelnameprimary": ip_module_title, 
        "model_name": model_name,
        "db_app_name": db_app_name,
        "direct_id": direct_id,
        "module_path": module_path,
        "first_model": first_model,
        "first_id_fk_ref": first_id_fk_ref,
        "first_model_name_import": first_model_name_import,
        "first_id": first_id,
        "first_name": first_name,
        "first_model_name": first_model_name,
        "display_module_name": display_module_name,
        "display_module_name_singular": display_module_name_singular,
        "display_module_name_plural": display_module_name_plural,
        "singular_module_name": singular_module_name,
        "plural_module_name": plural_module_name,
        "lc_singular_module_name": lc_singular_module_name,
        "lc_plural_module_name": lc_plural_module_name,  
        "lc_singular_root_module_name": lc_singular_root_module_name,
        "lc_plural_root_module_name": lc_plural_root_module_name
    }
    
    return variables

############################################# END OF CODE #############################################

def process_module_files(app_name, input_module, local_files_dir):
    #print(f">>> === Processing files in{app_name}{input_module} {local_files_dir} === <<<")
    variables = create_variables(app_name, input_module)
    # prepare the dictionary of variables for replacement
    var_value_dict = {
    "__appname__": variables["app_name"],
    "__version__": variables["version"],
    "__connectmoduletitle__": variables["connect_module_title"],
    "__connectappname__": variables["connect_app_name"],
    "__lcconnectmoduleip__": variables["lc_connect_module_ip"],
    "__dbconnectname__": variables["db_connect_name"],
    "__connectstr__": variables["connectstr"],
    "__connectid__": variables["connectid"],
    "__lcsingularconnectname__": variables["lc_singular_connect_name"],
    "__lcpluralconnectname__": variables["lc_plural_connect_name"],
    
    "__rootmodulename__": ref_module_name.lower(),
    "__modulename__": variables["module_name"],  
    "__dbmodelnameprimary__": variables["dbmodelnameprimary"],
    "__modelname__": variables["model_name"],
    "__dbappname__": variables["db_app_name"],
    "__directid__": variables["direct_id"],
    "__modulepath__": variables["module_path"],
    "__firstmodel__": variables["first_model"],
    "__firstidfkref__": variables["first_id_fk_ref"],
    "__firstmodelnameimport__": variables["first_model_name_import"],
    "__firstid__": variables["first_id"],
    "__firstname__": variables["first_name"],
    "__firstmodelname__": variables["first_model_name"],
    "__displaymodulename__": variables["display_module_name"],
    "__displaysingularmodname__": variables["display_module_name_singular"],
    "__displaypluralmodname__": variables["display_module_name_plural"],
    "__singularmodname__": variables["singular_module_name"],
    "__pluralmodname__": variables["plural_module_name"],
    "__lcsingularmodname__": variables["lc_singular_module_name"],
    "__lcpluralmodname__": variables["lc_plural_module_name"],
    "__lcsingularrootmodulename__": variables["lc_singular_root_module_name"],
    "__lcpluralrootmodulename__": variables["lc_plural_root_module_name"]
    }
    
    
    # important read the files from given dir and replace
    replace_placeholders_in_files(local_files_dir, var_value_dict)

#########################################################################################################
print(f">>> === START OF {script_name} === <<<")
ref_module_name = ref_module_name.lower()
# step1: using the script name go to the placeholder files
base_templates_dirnames = ["content", "content_type", "content_super_type"]
created_linked_modules = [f"{ref_module_name}", f"{ref_module_name}_type", f"{ref_module_name}_super_type"]
# Zip the lists together
zipped_lists = list(zip(base_templates_dirnames, created_linked_modules))
root_content_dirname = "content"
module_path_prefix = app_name.split("_")[1] 
connect_module_path_prefix = connect_app_name.split("_")[1]
placeholder_files_dir = "../../library/django_files"
project_dir = f"../../dev_env/project_area/env_{project_name}/{project_name}"
dest_app_dir = f"../../dev_env/project_area/env_{project_name}/{project_name}/{app_name}"

connected_apps_dirname = "connected_apps"
template_files_dir = f"{placeholder_files_dir}/{connected_apps_dirname}/{script_name}"
print(f">>> === TEMPLATE FILES Directory\n {template_files_dir} === <<<")
local_work_area = f"./work_area"
if os.path.exists(local_work_area):
    shutil.rmtree(local_work_area)

# step2: prepare the variables
ref_variables = create_variables(app_name, ref_module_name)
# step3: prepare the local work area where we will copy files

    #print(f">>> === STEP3:Creating local work area {local_work_area} === <<<")
   
# step4: copy the files to the local work area
for dirname, linked_module in zipped_lists:
    src_dir = f"{template_files_dir}/{dirname}"
    dst_dir = f"{local_work_area}/{linked_module}"
    #print(f">>> === STEP4:Copying files {src_dir} => {dst_dir} === <<<")
    copy_directory_contents(src_dir, dst_dir)

# step5: process module files 
for base_template, linked_module in zipped_lists:
    process_module_files(app_name, linked_module, f"{local_work_area}/{linked_module}")

# rename the work area files
def copy_and_rename_files(src_dir, dst_dir, linked_module):
    if not os.path.exists(src_dir):
        print(f"Source directory {src_dir} does not exist.")
        return
    
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    zipped_lists = list(zip(base_templates_dirnames, created_linked_modules))
    for dirname, linked_module in zipped_lists:
        lc_singular_module_name = linked_module.lower()
        lc_plural_module_name = linked_module.lower() if p.singular_noun(linked_module) else p.plural(linked_module)
        
        src_lc_singular_module_name = dirname.lower()
        src_lc_plural_module_name = dirname.lower() if p.singular_noun(dirname) else p.plural(dirname)
        
        #src_dir = f"{local_work_area}/{linked_module}/html/"
        dst_file = None
        for filename in os.listdir(src_dir):
            if filename.endswith(".html"):
                ops_name = filename.split('__')[0]
                module_suffix = filename.split('__')[1]
                file1 = f"{src_lc_singular_module_name}.html"
                file2 = f"{src_lc_plural_module_name}.html"
                
                if module_suffix == file1:
                    dst_file = f"{ops_name}__{lc_singular_module_name}.html"
                    #print(f">>> === SINGULAR MATCH FOUND {dst_file} === <<<")
                elif module_suffix == file2:
                    dst_file = f"{ops_name}__{lc_plural_module_name}.html"
                    #print(f">>> === PLURAL MATCH FOUND {dst_file} === <<<")
                else:
                    dst_file = filename
                    continue
                
                print(f">>> === SOURCE: suffix: {filename} => {dst_file}  === <<<")
                #print(f">>> === STEP5: Renaming files {src_dir}{filename} => {src_dir}{dst_file} === <<<")
                 
                src_file = os.path.join(src_dir, filename)
                dst_file = os.path.join(dst_dir, dst_file)
                print(f"Copying and renaming:\n Source: {src_file}\n Dest: {dst_file}\n")
                shutil.copy2(src_file, dst_file)
zipped_lists = list(zip(base_templates_dirnames, created_linked_modules))  # Recreate the zipped list if necessary
dst_html_files_dir = f"{dest_app_dir}/templates/{app_name}"
for dirname, linked_module in zipped_lists:
    src_dir = f"{local_work_area}/{linked_module}/html"
    dst_dir = f"{dst_html_files_dir}/mod_{linked_module}"
    print(f">>> === STEP6: Copying files {src_dir} => {dst_dir} === <<<")
    copy_and_rename_files(src_dir, dst_dir, linked_module)

# the python file does not need module_path_prefix only html does
if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
zipped_lists = list(zip(base_templates_dirnames, created_linked_modules))
dst_python_files_dir = f"{dest_app_dir}"
define_python_ops_dir = ["views_app", "urls_app", "forms_app", "models_app"]
for dirname, linked_module in zipped_lists:
    
    for ops_dir in define_python_ops_dir:
        print(f">>> === ******* CHECKED : dirname{dirname}=={linked_module} === <<<")
        src_dir = f"{local_work_area}/{linked_module}/python"
        
        dst_ops_name = ops_dir.split('_')[0]
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        
        lc_singular_module_name = linked_module.lower()
        lc_plural_module_name = linked_module.lower() if p.singular_noun(linked_module) else p.plural(linked_module)
        
        src_lc_singular_module_name = dirname.lower()
        src_lc_plural_module_name = dirname.lower() if p.singular_noun(dirname) else p.plural(dirname)
        
        for filename in os.listdir(src_dir):
            if filename.endswith(".py"):
                print(f">>> === ***** CHECKED IF CONDITION .PY === <<<")
                ops_name = filename.split('__')[0]
                module_suffix = filename.split('__')[1]
                file1 = f"{src_lc_singular_module_name}.py"
                file2 = f"{src_lc_plural_module_name}.py"
                print(f">>> === ***** IMPORTANT: module_suffix {module_suffix} == {file1} / {file2} === <<<")
                if module_suffix == file1:
                    dst_file = f"{ops_name}_{lc_singular_module_name}.py"
                    #print(f">>> === SINGULAR MATCH FOUND {dst_file} === <<<")
                elif module_suffix == file2:
                    dst_file = f"{ops_name}_{lc_plural_module_name}.py"
                    #print(f">>> === PLURAL MATCH FOUND {dst_file} === <<<")
                else:
                    dst_file = filename
                    continue
                
                print(f">>> === ***** CHECKED IF CONDITION {dst_ops_name} == {ops_name} === <<<")
                #print(f">>> === STEP5: Renaming files {src_dir}{filename} => {src_dir}{dst_file} === <<<")
                if dst_ops_name == ops_name:
                    print(f">>> === ***** CHECKED IF CONDITION {dst_ops_name} == {ops_name} === <<<")
                    print(f">>> === {dirname} => PYTHON COPY {filename} => {dst_file}  === <<<")
                    dst_dir = f"{dest_app_dir}/{ops_dir}"
                    dst_dir = f"{dest_app_dir}/mod_{lc_singular_module_name}"
                    src_file = os.path.join(src_dir, filename)
                    dst_file = os.path.join(dst_dir, dst_file)
                    print(f"Copying and renaming:\n Source: {src_file}\n Dest: {dst_file}\n")
                    shutil.copy2(src_file, dst_file)
        
print(f"\n\n>>> === END OF {script_name} === <<<")       



# final step
# add the connection between the connect module and this
connect_module_dirname = lc_connect_module_ip
connect_module_app_dir = f"{project_dir}/{connect_app_name}"
templates_dir = f"{connect_module_app_dir}/templates/{connect_app_name}/mod_{connect_module_dirname}"
connected_module_filename = f"connected_{lc_plural_connect_name}.html"
add_link = """
<a id="WHATMODULE_super_type" href="{% url 'list_REPLACE_super_types' tobject.id %}"
   class="btn btn-sm btn-primary">
    <i class="bi bi-diagram-3"></i> 
    WHATMODULE Super Type
</a>
&nbsp;&nbsp;

<a id="WHATMODULE" href="{% url 'list_SECOND' tobject.id 0 %}"
   class="btn btn-sm btn-primary">
    <i class="bi bi-diagram-3"></i> 
    WHATMODULE
</a>

"""

new_one = add_link.replace("REPLACE", ref_module_name.lower())
lc_plural_root_module_name = ref_module_name.lower() if p.singular_noun(ref_module_name) else p.plural(ref_module_name)
new_one = new_one.replace("SECOND", lc_plural_root_module_name)
new_one = new_one.replace("WHATMODULE", ref_module_name.title())    
print(f">>> === ADDING LINK TO CONNECTED MODULE {new_one} === <<<")
with(open(f"{templates_dir}/{connected_module_filename}", "a")) as f:
    f.write(new_one)
