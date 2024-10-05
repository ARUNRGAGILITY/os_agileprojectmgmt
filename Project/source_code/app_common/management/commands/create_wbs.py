from django.core.management.base import BaseCommand
from app_organization.mod_organization.models_organization import Organization
from app_system.mod_system_super_type.models_system_super_type import SystemSuperType
from app_system.mod_system_type.models_system_type import SystemType
from app_system.mod_system.models_system import System

class Command(BaseCommand):
    help = 'Generate the Organizations system'

    def create_organization(self, name):
        org, created = Organization.objects.get_or_create(name=name, active=True)
        if created:
            self.stdout.write(self.style.SUCCESS(f'Organization {name} created'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Organization {name} already exists'))
        return org

    def create_system_super_type(self, name, org):
        super_type, created = SystemSuperType.objects.get_or_create(name=name, org=org, active=True)
        if created:
            self.stdout.write(self.style.SUCCESS(f'SystemSuperType {name} created'))
        return super_type

    def create_system_type(self, name, super_type, org, parent=None):
        system_type, created = SystemType.objects.get_or_create(name=name, super_type=super_type, org=org, parent=parent, active=True)
        if created:
            self.stdout.write(self.style.SUCCESS(f'SystemType {name} created'))
        return system_type

    def create_system(self, name, type, org):
        system, created = System.objects.get_or_create(name=name, type=type, org=org, active=True)
        if created:
            self.stdout.write(self.style.SUCCESS(f'System {name} created'))
        return system

    def handle(self, *args, **kwargs):
        org = self.create_organization("ABC Organization")
        
        system_name = "Delivery System"
        
        super_type = self.create_system_super_type(system_name, org)
        stype = self.create_system_type(system_name, super_type, org)
        system = self.create_system(system_name, stype, org)
        
        # Create the different Agile and Agile at Scale Configurations, Backlog System
        portfolio_safe = self.create_system_type("Portfolio-SAFe", super_type, org, parent=stype)
        wbs = self.create_system_type("WBS", super_type, org, parent=portfolio_safe)
        initiative = self.create_system_type("Initiative", super_type, org, parent=wbs)
        strategic_theme = self.create_system_type("Strategic Theme", super_type, org, parent=initiative)
        epic = self.create_system_type("Epic", super_type, org, parent=strategic_theme)
        enabler_epic = self.create_system_type("Enabler Epic", super_type, org, parent=strategic_theme)
        feature = self.create_system_type("Feature", super_type, org, parent=epic)
        component = self.create_system_type("Component", super_type, org, parent=epic)
        capability = self.create_system_type("Capability", super_type, org, parent=epic)
        
        # Create User Stories, Spikes, and Tasks for Features
        user_story_feature = self.create_system_type("User Story", super_type, org, parent=feature)
        spike_feature = self.create_system_type("Spike", super_type, org, parent=feature)
        task_user_story_feature = self.create_system_type("Task", super_type, org, parent=user_story_feature)
        task_spike_feature = self.create_system_type("Task", super_type, org, parent=spike_feature)
        
        # Create User Stories, Spikes, and Tasks for Components
        user_story_component = self.create_system_type("User Story", super_type, org, parent=component)
        spike_component = self.create_system_type("Spike", super_type, org, parent=component)
        task_user_story_component = self.create_system_type("Task", super_type, org, parent=user_story_component)
        task_spike_component = self.create_system_type("Task", super_type, org, parent=spike_component)
        
        # Create User Stories, Spikes, and Tasks for Capabilities
        user_story_capability = self.create_system_type("User Story", super_type, org, parent=capability)
        spike_capability = self.create_system_type("Spike", super_type, org, parent=capability)
        task_user_story_capability = self.create_system_type("Task", super_type, org, parent=user_story_capability)
        task_spike_capability = self.create_system_type("Task", super_type, org, parent=spike_capability)
        
        # Enabler Features
        enabler_feature = self.create_system_type("Enabler Feature", super_type, org, parent=enabler_epic)
        enabler_component = self.create_system_type("Enabler Component", super_type, org, parent=enabler_epic)
        enabler_capability = self.create_system_type("Enabler Capability", super_type, org, parent=enabler_epic)
        
        # Create User Stories, Spikes, and Tasks for Enabler Features
        user_story_enabler_feature = self.create_system_type("User Story", super_type, org, parent=enabler_feature)
        spike_enabler_feature = self.create_system_type("Spike", super_type, org, parent=enabler_feature)
        task_user_story_enabler_feature = self.create_system_type("Task", super_type, org, parent=user_story_enabler_feature)
        task_spike_enabler_feature = self.create_system_type("Task", super_type, org, parent=spike_enabler_feature)
        
        # Create User Stories, Spikes, and Tasks for Enabler Components
        user_story_enabler_component = self.create_system_type("User Story", super_type, org, parent=enabler_component)
        spike_enabler_component = self.create_system_type("Spike", super_type, org, parent=enabler_component)
        task_user_story_enabler_component = self.create_system_type("Task", super_type, org, parent=user_story_enabler_component)
        task_spike_enabler_component = self.create_system_type("Task", super_type, org, parent=spike_enabler_component)
        
        # Create User Stories, Spikes, and Tasks for Enabler Capabilities
        user_story_enabler_capability = self.create_system_type("User Story", super_type, org, parent=enabler_capability)
        spike_enabler_capability = self.create_system_type("Spike", super_type, org, parent=enabler_capability)
        task_user_story_enabler_capability = self.create_system_type("Task", super_type, org, parent=user_story_enabler_capability)
        task_spike_enabler_capability = self.create_system_type("Task", super_type, org, parent=spike_enabler_capability)
