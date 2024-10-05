import sys
import os
import subprocess
from utils import *

DJANGO_PROJECTS_DIRNAME = "dev_env"
PROJECTAREA_DIRNAME = "project_area"


def get_base_projects_directory():
    # Get the absolute path of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Move up two levels from 'build/bin'
    base_dir = os.path.join(script_dir, '..', '..')
    return os.path.abspath(base_dir)

def verbose_print(verbose, *args):
    if verbose:
        print(*args)
        
        
def get_project_details(project_name, verbose):
    base_dir = get_base_projects_directory()
    projects_area = os.path.join(base_dir, DJANGO_PROJECTS_DIRNAME, 
                                                PROJECTAREA_DIRNAME)
    
    # Create the project area if required
    if not os.path.exists(projects_area):
        os.makedirs(projects_area)   
    # This will be created under env_projectname/projectname/std_project_dirname
    env_project_dirname = f"env_{project_name}"
    project_dirname = f"{project_name}"
    std_project_name = f"project_{project_name}"
    project_parent_dir = os.path.join(projects_area, env_project_dirname, project_dirname)
    return env_project_dirname, project_dirname, std_project_name, project_parent_dir

def get_app_details(project_name, app_name, verbose):
    base_dir = get_base_projects_directory()
    projects_area = os.path.join(base_dir, DJANGO_PROJECTS_DIRNAME, 
                                                PROJECTAREA_DIRNAME)
    env_project_dirname = f"env_{project_name}"
    project_dirname = f"{project_name}"
    std_project_name = f"project_{project_name}"
    project_parent_dir = os.path.join(projects_area, env_project_dirname, project_dirname)
    project_dir = project_parent_dir + f"/{std_project_name}"
    std_app_name = f"app_{app_name}"
    app_dir = os.path.join(projects_area, env_project_dirname, project_dirname, std_app_name)
    
    return env_project_dirname, project_dirname, std_project_name, project_parent_dir, project_dir, std_app_name, app_dir

def generate_urls(app_directory, urls_app_filename):
    # Ensure the app directory path is absolute
    app_directory = os.path.abspath(app_directory)
    # Extract the app name from the absolute path
    app_name = os.path.basename(app_directory)
    # Path to the file that will include all module URLs
    urls_file_path = os.path.join(app_directory, f"mod_app/{urls_app_filename}.py")
    
    with open(urls_file_path, 'w') as urls_file:
        urls_file.write("from django.urls import include, path\n\n")
        urls_file.write("urlpatterns = [\n")
        
        for entry in os.listdir(app_directory):
            entry_path = os.path.join(app_directory, entry)
            #print(f"Processing entry: {entry_path}")
            # Check if the entry is a directory and starts with 'mod_' but is not 'mod_app'
            if os.path.isdir(entry_path) and entry.startswith('mod_') and entry != 'mod_app':
                urls_module = f'urls_{entry[4:]}'
                urls_module_path = os.path.join(entry_path, f'{urls_module}.py')
                print(f">>> === Found module: {urls_module_path} ===")
                if os.path.exists(urls_module_path):
                    urls_file.write(f"    path('{entry[4:]}/', include('{app_name}.{entry}.{urls_module}')),\n")
                else:
                    print(f"urls_module_path does not exist: {urls_module_path}")
        
        urls_file.write("]\n")

    print(f"{urls_file_path} generated successfully.")