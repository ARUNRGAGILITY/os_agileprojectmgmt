from django.core.management.base import BaseCommand
from app_organization.mod_organization.models_organization import Organization
from app_system.mod_system_super_type.models_system_super_type import SystemSuperType
from app_system.mod_system_type.models_system_type import SystemType
from app_system.mod_system.models_system import System

class Command(BaseCommand):
    help = 'Generate the Organizations system backlog items'

    def create_organization(self, name):
        org, created = Organization.objects.get_or_create(name=name, active=True)
        if created:
            self.stdout.write(self.style.SUCCESS(f'Organization {name} created'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Organization {name} already exists'))
        return org

    def create_system(self, name, system_type, org, parent=None):
        system, created = System.objects.get_or_create(name=name, type=system_type, org=org, parent=parent, active=True)
        if created:
            self.stdout.write(self.style.SUCCESS(f'System {name} created'))
        return system

    def handle(self, *args, **kwargs):
        org = self.create_organization("ABC Organization")

        # Retrieve the system types with active=True
        delivery_system_type = SystemType.objects.get(name="Delivery System", org=org, active=True)
        portfolio_safe_type = SystemType.objects.get(name="Portfolio-SAFe", org=org, active=True)
        wbs_type = SystemType.objects.get(name="WBS", org=org, active=True)
        initiative_type = SystemType.objects.get(name="Initiative", org=org, active=True)
        strategic_theme_type = SystemType.objects.get(name="Strategic Theme", org=org, active=True)
        epic_type = SystemType.objects.get(name="Epic", org=org, active=True)
        enabler_epic_type = SystemType.objects.get(name="Enabler Epic", org=org, active=True)
        
        feature_type = SystemType.objects.get(name="Feature", org=org, active=True)
        component_type = SystemType.objects.get(name="Component", org=org, active=True)
        capability_type = SystemType.objects.get(name="Capability", org=org, active=True)        

        feature_us_type = SystemType.objects.get(name="User Story", parent=feature_type, org=org, active=True)
        feature_spike_type = SystemType.objects.get(name="Spike", parent=feature_type, org=org, active=True)
        
        component_us_type = SystemType.objects.get(name="User Story", parent=component_type, org=org, active=True)
        component_spike_type = SystemType.objects.get(name="Spike", parent=component_type, org=org, active=True)
        
        capability_us_type = SystemType.objects.get(name="User Story", parent=capability_type, org=org, active=True)
        capability_spike_type = SystemType.objects.get(name="Spike", parent=capability_type, org=org, active=True)
        
        us_feature_task_type = SystemType.objects.get(name="Task", parent=feature_us_type, org=org, active=True)
        spike_feature_task_type = SystemType.objects.get(name="Task", parent=feature_spike_type, org=org, active=True)
        
        us_component_task_type = SystemType.objects.get(name="Task", parent=component_us_type, org=org, active=True)
        spike_component_task_type = SystemType.objects.get(name="Task", parent=component_spike_type, org=org, active=True)
        
        us_capability_task_type = SystemType.objects.get(name="Task", parent=capability_us_type, org=org, active=True)
        spike_capability_task_type = SystemType.objects.get(name="Task", parent=capability_spike_type, org=org, active=True)
        
        
        # enablers
        enabler_feature_type = SystemType.objects.get(name="Enabler Feature", org=org, active=True)
        enabler_component_type = SystemType.objects.get(name="Enabler Component", org=org, active=True)
        enabler_capability_type = SystemType.objects.get(name="Enabler Capability", org=org, active=True)

        
        efeature_us_type = SystemType.objects.get(name="User Story", parent=enabler_feature_type, org=org, active=True)
        efeature_spike_type = SystemType.objects.get(name="Spike", parent=enabler_feature_type, org=org, active=True)
        
        ecomponent_us_type = SystemType.objects.get(name="User Story", parent=enabler_component_type, org=org, active=True)
        ecomponent_spike_type = SystemType.objects.get(name="Spike", parent=enabler_component_type, org=org, active=True)
        
        ecapability_us_type = SystemType.objects.get(name="User Story", parent=enabler_capability_type, org=org, active=True)
        ecapability_spike_type = SystemType.objects.get(name="Spike", parent=enabler_capability_type, org=org, active=True)
        
        us_efeature_task_type = SystemType.objects.get(name="Task", parent=efeature_us_type, org=org, active=True)
        spike_efeature_task_type = SystemType.objects.get(name="Task", parent=efeature_spike_type, org=org, active=True)
        
        us_ecomponent_task_type = SystemType.objects.get(name="Task", parent=ecomponent_us_type, org=org, active=True)
        spike_ecomponent_task_type = SystemType.objects.get(name="Task", parent=ecomponent_spike_type, org=org, active=True)
        
        us_ecapability_task_type = SystemType.objects.get(name="Task", parent=ecapability_us_type, org=org, active=True)
        spike_ecapability_task_type = SystemType.objects.get(name="Task", parent=ecapability_spike_type, org=org, active=True)
        
        
        # setup 
        # Create the root system
        self.stdout.write(self.style.SUCCESS('Creating the root system'))
        root_system = self.create_system("Delivery System", delivery_system_type, org)

        # Create the Portfolio-SAFe system
        portfolio_safe_system = self.create_system("Portfolio-SAFe", portfolio_safe_type, org, parent=root_system)

        # Create WBS system under Portfolio-SAFe
        wbs_system = self.create_system("WBS", wbs_type, org, parent=portfolio_safe_system)

        
        # creation of the backlog
        initiative_system = self.create_system("Basic Initiative 1", initiative_type, org, parent=wbs_system)
        initiative_system_2 = self.create_system("Strategic Initiative 2", initiative_type, org, parent=wbs_system)
        
        # Create Strategic Themes under Initiatives
        strategic_theme1_system = self.create_system("Improve Customer Experience", strategic_theme_type, org, parent=initiative_system)
        strategic_theme2_system = self.create_system("Increase Operational Efficiency", strategic_theme_type, org, parent=initiative_system_2)

        # Create Epics under Strategic Theme 1
        epic1_system = self.create_system("Develop New Mobile App", epic_type, org, parent=strategic_theme1_system)
        epic2_system = self.create_system("Enhance Website UX", epic_type, org, parent=strategic_theme1_system)

        # Create Epics under Strategic Theme 1
        epic1_system = self.create_system("Develop New Mobile App", epic_type, org, parent=strategic_theme1_system)
        epic2_system = self.create_system("Enhance Website UX", epic_type, org, parent=strategic_theme1_system)

        # Create Features, Components, and Capabilities under Epic 1 (Develop New Mobile App)
        feature1_epic1 = self.create_system("User Authentication", feature_type, org, parent=epic1_system)
        feature2_epic1 = self.create_system("Push Notifications", feature_type, org, parent=epic1_system)

        component1_epic1 = self.create_system("Login Page", component_type, org, parent=epic1_system)
        component2_epic1 = self.create_system("Notification Service", component_type, org, parent=epic1_system)

        capability1_epic1 = self.create_system("OAuth2 Integration", capability_type, org, parent=epic1_system)
        capability2_epic1 = self.create_system("Firebase Cloud Messaging", capability_type, org, parent=epic1_system)

        # Create Features, Components, and Capabilities under Epic 2 (Enhance Website UX)
        feature1_epic2 = self.create_system("Revamp Home Page", feature_type, org, parent=epic2_system)
        feature2_epic2 = self.create_system("Improve Search Functionality", feature_type, org, parent=epic2_system)

        component1_epic2 = self.create_system("Home Page Design", component_type, org, parent=epic2_system)
        component2_epic2 = self.create_system("Search Bar", component_type, org, parent=epic2_system)

        capability1_epic2 = self.create_system("Responsive Design", capability_type, org, parent=epic2_system)
        capability2_epic2 = self.create_system("ElasticSearch Integration", capability_type, org, parent=epic2_system)
        
        # creating for epic1/feature1 & feature2
        # Create Epics under Strategic Theme 1
      

        # Create Epics under Strategic Theme 1
        ############################################################################################################################
        # Add User Stories under Feature 1 of Epic 1 (User Authentication)
        us1_feature1_epic1 = self.create_system("As a user, I want to register using my email address, so that I can create an account quickly and easily", feature_us_type, org, parent=feature1_epic1)
        us2_feature1_epic1 = self.create_system("As a user, I want to log in using my email and password, so that I can securely access my account", feature_us_type, org, parent=feature1_epic1)
        us3_feature1_epic1 = self.create_system("As a user, I want to reset my password if I forget it, so that I can regain access to my account", feature_us_type, org, parent=feature1_epic1)
        us4_feature1_epic1 = self.create_system("As a user, I want to receive a verification email after registration, so that I can confirm my account and ensure security", feature_us_type, org, parent=feature1_epic1)
        us5_feature1_epic1 = self.create_system("As a user, I want to enable two-factor authentication for added security, so that I can protect my account from unauthorized access", feature_us_type, org, parent=feature1_epic1)

        # Add Spikes under Feature 1 of Epic 1 (User Authentication)
        spike1_feature1_epic1 = self.create_system("Spike: Research OAuth2 Providers", feature_spike_type, org, parent=feature1_epic1)
        spike2_feature1_epic1 = self.create_system("Spike: Evaluate Security Measures for Password Reset", feature_spike_type, org, parent=feature1_epic1)
        
        # Add Tasks under User Stories for Feature 1 of Epic 1 (User Authentication)
        #################################### TASKS ####################################
        # Tasks for "As a user, I want to register using my email address, so that I can create an account quickly and easily"
        self.create_system("Design registration form", us_feature_task_type, org, parent=us1_feature1_epic1)
        self.create_system("Implement registration backend logic", us_feature_task_type, org, parent=us1_feature1_epic1)
        self.create_system("Add email validation", us_feature_task_type, org, parent=us1_feature1_epic1)
        self.create_system("Create database schema for user accounts", us_feature_task_type, org, parent=us1_feature1_epic1)
        self.create_system("Write unit tests for registration", us_feature_task_type, org, parent=us1_feature1_epic1)
        self.create_system("Deploy registration feature", us_feature_task_type, org, parent=us1_feature1_epic1)

        # Tasks for "As a user, I want to log in using my email and password, so that I can securely access my account"
        self.create_system("Design login form", us_feature_task_type, org, parent=us2_feature1_epic1)
        self.create_system("Implement login backend logic", us_feature_task_type, org, parent=us2_feature1_epic1)
        self.create_system("Add password hashing", us_feature_task_type, org, parent=us2_feature1_epic1)
        self.create_system("Create session management system", us_feature_task_type, org, parent=us2_feature1_epic1)
        self.create_system("Write unit tests for login", us_feature_task_type, org, parent=us2_feature1_epic1)
        self.create_system("Deploy login feature", us_feature_task_type, org, parent=us2_feature1_epic1)

        # Tasks for "As a user, I want to reset my password if I forget it, so that I can regain access to my account"
        self.create_system("Design password reset form", us_feature_task_type, org, parent=us3_feature1_epic1)
        self.create_system("Implement password reset backend logic", us_feature_task_type, org, parent=us3_feature1_epic1)
        self.create_system("Add email notification for password reset", us_feature_task_type, org, parent=us3_feature1_epic1)
        self.create_system("Write unit tests for password reset", us_feature_task_type, org, parent=us3_feature1_epic1)
        self.create_system("Deploy password reset feature", us_feature_task_type, org, parent=us3_feature1_epic1)
        self.create_system("Monitor password reset feature", us_feature_task_type, org, parent=us3_feature1_epic1)

        # Tasks for "As a user, I want to receive a verification email after registration, so that I can confirm my account and ensure security"
        self.create_system("Design verification email template", us_feature_task_type, org, parent=us4_feature1_epic1)
        self.create_system("Implement verification email sending logic", us_feature_task_type, org, parent=us4_feature1_epic1)
        self.create_system("Add verification token generation", us_feature_task_type, org, parent=us4_feature1_epic1)
        self.create_system("Write unit tests for email verification", us_feature_task_type, org, parent=us4_feature1_epic1)
        self.create_system("Deploy email verification feature", us_feature_task_type, org, parent=us4_feature1_epic1)
        self.create_system("Monitor email verification feature", us_feature_task_type, org, parent=us4_feature1_epic1)

        # Tasks for "As a user, I want to enable two-factor authentication for added security, so that I can protect my account from unauthorized access"
        self.create_system("Design two-factor authentication UI", us_feature_task_type, org, parent=us5_feature1_epic1)
        self.create_system("Implement two-factor authentication logic", us_feature_task_type, org, parent=us5_feature1_epic1)
        self.create_system("Add two-factor authentication configuration options", us_feature_task_type, org, parent=us5_feature1_epic1)
        self.create_system("Write unit tests for two-factor authentication", us_feature_task_type, org, parent=us5_feature1_epic1)
        self.create_system("Deploy two-factor authentication feature", us_feature_task_type, org, parent=us5_feature1_epic1)
        self.create_system("Monitor two-factor authentication feature", us_feature_task_type, org, parent=us5_feature1_epic1)

        # Add Tasks under Spikes for Feature 1 of Epic 1 (User Authentication)

        # Tasks for "Spike: Research OAuth2 Providers"
        self.create_system("Research OAuth2 providers' documentation", spike_feature_task_type, org, parent=spike1_feature1_epic1)
        self.create_system("Create proof of concept for OAuth2 integration", spike_feature_task_type, org, parent=spike1_feature1_epic1)
        self.create_system("Evaluate security implications of OAuth2", spike_feature_task_type, org, parent=spike1_feature1_epic1)
        self.create_system("Document OAuth2 integration process", spike_feature_task_type, org, parent=spike1_feature1_epic1)
        self.create_system("Present findings on OAuth2 providers", spike_feature_task_type, org, parent=spike1_feature1_epic1)
        self.create_system("Make recommendations for OAuth2 provider selection", spike_feature_task_type, org, parent=spike1_feature1_epic1)

        # Tasks for "Spike: Evaluate Security Measures for Password Reset"
        self.create_system("Evaluate current password reset security measures", spike_feature_task_type, org, parent=spike2_feature1_epic1)
        self.create_system("Research best practices for password reset security", spike_feature_task_type, org, parent=spike2_feature1_epic1)
        self.create_system("Create proof of concept for improved password reset security", spike_feature_task_type, org, parent=spike2_feature1_epic1)
        self.create_system("Document password reset security findings", spike_feature_task_type, org, parent=spike2_feature1_epic1)
        self.create_system("Present findings on password reset security", spike_feature_task_type, org, parent=spike2_feature1_epic1)
        self.create_system("Make recommendations for password reset security improvements", spike_feature_task_type, org, parent=spike2_feature1_epic1)


        # Add Tasks under Spikes for Feature 1 of Epic 1 (User Authentication)
      
        # Add User Stories under Feature 2 of Epic 1 (Push Notifications)
        self.create_system("As a user, I want to receive notifications for new messages, so that I am promptly informed about any new communication", feature_us_type, org, parent=feature2_epic1)
        self.create_system("As a user, I want to receive notifications for friend requests, so that I can quickly accept or decline connection requests", feature_us_type, org, parent=feature2_epic1)
        self.create_system("As a user, I want to receive notifications for app updates, so that I am aware of new features and improvements", feature_us_type, org, parent=feature2_epic1)
        self.create_system("As a user, I want to customize which notifications I receive, so that I can control the information I am alerted to", feature_us_type, org, parent=feature2_epic1)
        self.create_system("As a user, I want to receive notifications for upcoming events, so that I can stay informed about important dates and activities", feature_us_type, org, parent=feature2_epic1)

        # Add Spikes under Feature 2 of Epic 1 (Push Notifications)
        self.create_system("Spike: Explore Firebase Cloud Messaging Integration", feature_spike_type, org, parent=feature2_epic1)
        self.create_system("Spike: Investigate Notification Preferences Management", feature_spike_type, org, parent=feature2_epic1)

        ## tasks
        # Add User Stories under Feature 2 of Epic 1 (Push Notifications)
        us1_feature2_epic1 = self.create_system("As a user, I want to receive notifications for new messages, so that I am promptly informed about any new communication", feature_us_type, org, parent=feature2_epic1)
        us2_feature2_epic1 = self.create_system("As a user, I want to receive notifications for friend requests, so that I can quickly accept or decline connection requests", feature_us_type, org, parent=feature2_epic1)
        us3_feature2_epic1 = self.create_system("As a user, I want to receive notifications for app updates, so that I am aware of new features and improvements", feature_us_type, org, parent=feature2_epic1)
        us4_feature2_epic1 = self.create_system("As a user, I want to customize which notifications I receive, so that I can control the information I am alerted to", feature_us_type, org, parent=feature2_epic1)
        us5_feature2_epic1 = self.create_system("As a user, I want to receive notifications for upcoming events, so that I can stay informed about important dates and activities", feature_us_type, org, parent=feature2_epic1)

        # Add Spikes under Feature 2 of Epic 1 (Push Notifications)
        spike1_feature2_epic1 = self.create_system("Spike: Explore Firebase Cloud Messaging Integration", feature_spike_type, org, parent=feature2_epic1)
        spike2_feature2_epic1 = self.create_system("Spike: Investigate Notification Preferences Management", feature_spike_type, org, parent=feature2_epic1)

        # Add Tasks under User Stories for Feature 2 of Epic 1 (Push Notifications)

        # Tasks for "As a user, I want to receive notifications for new messages, so that I am promptly informed about any new communication"
        self.create_system("Design notification UI for new messages", us_feature_task_type, org, parent=us1_feature2_epic1)
        self.create_system("Implement backend logic for new message notifications", us_feature_task_type, org, parent=us1_feature2_epic1)
        self.create_system("Integrate notification service with messaging system", us_feature_task_type, org, parent=us1_feature2_epic1)
        self.create_system("Write unit tests for new message notifications", us_feature_task_type, org, parent=us1_feature2_epic1)
        self.create_system("Deploy new message notification feature", us_feature_task_type, org, parent=us1_feature2_epic1)
        self.create_system("Monitor new message notification feature", us_feature_task_type, org, parent=us1_feature2_epic1)

        # Tasks for "As a user, I want to receive notifications for friend requests, so that I can quickly accept or decline connection requests"
        self.create_system("Design friend request notification UI", us_feature_task_type, org, parent=us2_feature2_epic1)
        self.create_system("Implement backend logic for friend request notifications", us_feature_task_type, org, parent=us2_feature2_epic1)
        self.create_system("Integrate notification service with friend request system", us_feature_task_type, org, parent=us2_feature2_epic1)
        self.create_system("Write unit tests for friend request notifications", us_feature_task_type, org, parent=us2_feature2_epic1)
        self.create_system("Deploy friend request notification feature", us_feature_task_type, org, parent=us2_feature2_epic1)
        self.create_system("Monitor friend request notification feature", us_feature_task_type, org, parent=us2_feature2_epic1)

        # Tasks for "As a user, I want to receive notifications for app updates, so that I am aware of new features and improvements"
        self.create_system("Design app update notification UI", us_feature_task_type, org, parent=us3_feature2_epic1)
        self.create_system("Implement backend logic for app update notifications", us_feature_task_type, org, parent=us3_feature2_epic1)
        self.create_system("Integrate notification service with app update system", us_feature_task_type, org, parent=us3_feature2_epic1)
        self.create_system("Write unit tests for app update notifications", us_feature_task_type, org, parent=us3_feature2_epic1)
        self.create_system("Deploy app update notification feature", us_feature_task_type, org, parent=us3_feature2_epic1)
        self.create_system("Monitor app update notification feature", us_feature_task_type, org, parent=us3_feature2_epic1)

        # Tasks for "As a user, I want to customize which notifications I receive, so that I can control the information I am alerted to"
        self.create_system("Design notification preferences UI", us_feature_task_type, org, parent=us4_feature2_epic1)
        self.create_system("Implement backend logic for notification preferences", us_feature_task_type, org, parent=us4_feature2_epic1)
        self.create_system("Add options for customizing notifications", us_feature_task_type, org, parent=us4_feature2_epic1)
        self.create_system("Write unit tests for notification preferences", us_feature_task_type, org, parent=us4_feature2_epic1)
        self.create_system("Deploy notification preferences feature", us_feature_task_type, org, parent=us4_feature2_epic1)
        self.create_system("Monitor notification preferences feature", us_feature_task_type, org, parent=us4_feature2_epic1)

        # Tasks for "As a user, I want to receive notifications for upcoming events, so that I can stay informed about important dates and activities"
        self.create_system("Design event notification UI", us_feature_task_type, org, parent=us5_feature2_epic1)
        self.create_system("Implement backend logic for event notifications", us_feature_task_type, org, parent=us5_feature2_epic1)
        self.create_system("Integrate notification service with event system", us_feature_task_type, org, parent=us5_feature2_epic1)
        self.create_system("Write unit tests for event notifications", us_feature_task_type, org, parent=us5_feature2_epic1)
        self.create_system("Deploy event notification feature", us_feature_task_type, org, parent=us5_feature2_epic1)
        self.create_system("Monitor event notification feature", us_feature_task_type, org, parent=us5_feature2_epic1)

        # Add Tasks under Spikes for Feature 2 of Epic 1 (Push Notifications)

        # Tasks for "Spike: Explore Firebase Cloud Messaging Integration"
        self.create_system("Explore Firebase Cloud Messaging documentation", spike_feature_task_type, org, parent=spike1_feature2_epic1)
        self.create_system("Create proof of concept for Firebase integration", spike_feature_task_type, org, parent=spike1_feature2_epic1)
        self.create_system("Evaluate compatibility of Firebase with existing systems", spike_feature_task_type, org, parent=spike1_feature2_epic1)
        self.create_system("Document Firebase integration process", spike_feature_task_type, org, parent=spike1_feature2_epic1)
        self.create_system("Present findings on Firebase integration", spike_feature_task_type, org, parent=spike1_feature2_epic1)
        self.create_system("Make recommendations for Firebase usage", spike_feature_task_type, org, parent=spike1_feature2_epic1)

        # Tasks for "Spike: Investigate Notification Preferences Management"
        self.create_system("Investigate current notification preferences management", spike_feature_task_type, org, parent=spike2_feature2_epic1)
        self.create_system("Research best practices for notification preferences management", spike_feature_task_type, org, parent=spike2_feature2_epic1)
        self.create_system("Create proof of concept for improved notification preferences", spike_feature_task_type, org, parent=spike2_feature2_epic1)
        self.create_system("Document notification preferences management findings", spike_feature_task_type, org, parent=spike2_feature2_epic1)
        self.create_system("Present findings on notification preferences management", spike_feature_task_type, org, parent=spike2_feature2_epic1)
        self.create_system("Make recommendations for notification preferences improvements", spike_feature_task_type, org, parent=spike2_feature2_epic1)

        
        
        
        ## tasks
        # Add User Stories under Feature 1 of Epic 2 (Revamp Home Page)
        # Add User Stories under Feature 1 of Epic 2 (Revamp Home Page)
        us1_feature1_epic2 = self.create_system("As a user, I want the home page to load quickly, so that I can start using the app without delay", feature_us_type, org, parent=feature1_epic2)
        us2_feature1_epic2 = self.create_system("As a user, I want the home page to be visually appealing, so that I have a pleasant experience using the app", feature_us_type, org, parent=feature1_epic2)
        us3_feature1_epic2 = self.create_system("As a user, I want the home page to highlight key features of the app, so that I can easily find and use them", feature_us_type, org, parent=feature1_epic2)
        us4_feature1_epic2 = self.create_system("As a user, I want the home page to be easy to navigate, so that I can find what I need quickly", feature_us_type, org, parent=feature1_epic2)

        # Add Tasks under User Stories for Feature 1 of Epic 2 (Revamp Home Page)

        # Tasks for "As a user, I want the home page to load quickly, so that I can start using the app without delay"
        task1_us1_feature1_epic2 = self.create_system("Optimize image loading", us_feature_task_type, org, parent=us1_feature1_epic2)
        task2_us1_feature1_epic2 = self.create_system("Minimize CSS and JS", us_feature_task_type, org, parent=us1_feature1_epic2)
        task3_us1_feature1_epic2 = self.create_system("Implement lazy loading", us_feature_task_type, org, parent=us1_feature1_epic2)
        task4_us1_feature1_epic2 = self.create_system("Reduce server response time", us_feature_task_type, org, parent=us1_feature1_epic2)
        task5_us1_feature1_epic2 = self.create_system("Conduct performance testing", us_feature_task_type, org, parent=us1_feature1_epic2)
        task6_us1_feature1_epic2 = self.create_system("Monitor home page load speed", us_feature_task_type, org, parent=us1_feature1_epic2)

        # Tasks for "As a user, I want the home page to be visually appealing, so that I have a pleasant experience using the app"
        task1_us2_feature1_epic2 = self.create_system("Redesign home page layout", us_feature_task_type, org, parent=us2_feature1_epic2)
        task2_us2_feature1_epic2 = self.create_system("Choose color scheme", us_feature_task_type, org, parent=us2_feature1_epic2)
        task3_us2_feature1_epic2 = self.create_system("Update fonts and typography", us_feature_task_type, org, parent=us2_feature1_epic2)
        task4_us2_feature1_epic2 = self.create_system("Add engaging visuals", us_feature_task_type, org, parent=us2_feature1_epic2)
        task5_us2_feature1_epic2 = self.create_system("Implement animations", us_feature_task_type, org, parent=us2_feature1_epic2)
        task6_us2_feature1_epic2 = self.create_system("Gather user feedback on design", us_feature_task_type, org, parent=us2_feature1_epic2)

        # Tasks for "As a user, I want the home page to highlight key features of the app, so that I can easily find and use them"
        task1_us3_feature1_epic2 = self.create_system("Identify key features to highlight", us_feature_task_type, org, parent=us3_feature1_epic2)
        task2_us3_feature1_epic2 = self.create_system("Design feature highlight sections", us_feature_task_type, org, parent=us3_feature1_epic2)
        task3_us3_feature1_epic2 = self.create_system("Implement feature highlights", us_feature_task_type, org, parent=us3_feature1_epic2)
        task4_us3_feature1_epic2 = self.create_system("Write content for feature highlights", us_feature_task_type, org, parent=us3_feature1_epic2)
        task5_us3_feature1_epic2 = self.create_system("Test feature highlight functionality", us_feature_task_type, org, parent=us3_feature1_epic2)
        task6_us3_feature1_epic2 = self.create_system("Monitor user interaction with feature highlights", us_feature_task_type, org, parent=us3_feature1_epic2)

        # Tasks for "As a user, I want the home page to be easy to navigate, so that I can find what I need quickly"
        task1_us4_feature1_epic2 = self.create_system("Design intuitive navigation menu", us_feature_task_type, org, parent=us4_feature1_epic2)
        task2_us4_feature1_epic2 = self.create_system("Implement navigation menu", us_feature_task_type, org, parent=us4_feature1_epic2)
        task3_us4_feature1_epic2 = self.create_system("Add search functionality", us_feature_task_type, org, parent=us4_feature1_epic2)
        task4_us4_feature1_epic2 = self.create_system("Write user guides for navigation", us_feature_task_type, org, parent=us4_feature1_epic2)
        task5_us4_feature1_epic2 = self.create_system("Test navigation flow", us_feature_task_type, org, parent=us4_feature1_epic2)
        task6_us4_feature1_epic2 = self.create_system("Monitor user navigation patterns", us_feature_task_type, org, parent=us4_feature1_epic2)

        # Add Spikes under Feature 1 of Epic 2 (Revamp Home Page)
        spike1_feature1_epic2 = self.create_system("Spike: Research Latest UI/UX Trends for Home Page Design", feature_spike_type, org, parent=feature1_epic2)
        spike2_feature1_epic2 = self.create_system("Spike: Evaluate Performance Optimization Techniques for Home Page Loading Speed", feature_spike_type, org, parent=feature1_epic2)
        spike3_feature1_epic2 = self.create_system("Spike: Investigate Tools for Personalized Content Display on Home Page", feature_spike_type, org, parent=feature1_epic2)

        # Add Tasks under Spikes for Feature 1 of Epic 2 (Revamp Home Page)

        # Tasks for "Spike: Research Latest UI/UX Trends for Home Page Design"
        task1_spike1_feature1_epic2 = self.create_system("Review recent UI/UX design publications", spike_feature_task_type, org, parent=spike1_feature1_epic2)
        task2_spike1_feature1_epic2 = self.create_system("Analyze competitor home page designs", spike_feature_task_type, org, parent=spike1_feature1_epic2)
        task3_spike1_feature1_epic2 = self.create_system("Identify common design patterns", spike_feature_task_type, org, parent=spike1_feature1_epic2)
        task4_spike1_feature1_epic2 = self.create_system("Create design mockups", spike_feature_task_type, org, parent=spike1_feature1_epic2)
        task5_spike1_feature1_epic2 = self.create_system("Conduct user surveys on design preferences", spike_feature_task_type, org, parent=spike1_feature1_epic2)
        task6_spike1_feature1_epic2 = self.create_system("Present findings on UI/UX trends", spike_feature_task_type, org, parent=spike1_feature1_epic2)

        # Tasks for "Spike: Evaluate Performance Optimization Techniques for Home Page Loading Speed"
        task1_spike2_feature1_epic2 = self.create_system("Research performance optimization techniques", spike_feature_task_type, org, parent=spike2_feature1_epic2)
        task2_spike2_feature1_epic2 = self.create_system("Identify key performance bottlenecks", spike_feature_task_type, org, parent=spike2_feature1_epic2)
        task3_spike2_feature1_epic2 = self.create_system("Implement sample optimizations", spike_feature_task_type, org, parent=spike2_feature1_epic2)
        task4_spike2_feature1_epic2 = self.create_system("Test performance improvements", spike_feature_task_type, org, parent=spike2_feature1_epic2)
        task5_spike2_feature1_epic2 = self.create_system("Document performance optimization process", spike_feature_task_type, org, parent=spike2_feature1_epic2)
        task6_spike2_feature1_epic2 = self.create_system("Present findings on performance optimization", spike_feature_task_type, org, parent=spike2_feature1_epic2)

        # Tasks for "Spike: Investigate Tools for Personalized Content Display on Home Page"
        task1_spike3_feature1_epic2 = self.create_system("Research tools for personalized content display", spike_feature_task_type, org, parent=spike3_feature1_epic2)
        task2_spike3_feature1_epic2 = self.create_system("Evaluate pros and cons of different tools", spike_feature_task_type, org, parent=spike3_feature1_epic2)
        task3_spike3_feature1_epic2 = self.create_system("Create proof of concept for content personalization", spike_feature_task_type, org, parent=spike3_feature1_epic2)
        task4_spike3_feature1_epic2 = self.create_system("Test personalized content display", spike_feature_task_type, org, parent=spike3_feature1_epic2)
        task5_spike3_feature1_epic2 = self.create_system("Document content personalization findings", spike_feature_task_type, org, parent=spike3_feature1_epic2)
        task6_spike3_feature1_epic2 = self.create_system("Present findings on personalized content tools", spike_feature_task_type, org, parent=spike3_feature1_epic2)

        # Add User Stories under Feature 2 of Epic 2 (Improve Search Functionality)
        # Add User Stories under Feature 2 of Epic 2 (Improve Search Functionality)
        us1_feature2_epic2 = self.create_system("As a user, I want to find relevant results quickly, so that I can access the information I need", feature_us_type, org, parent=feature2_epic2)
        us2_feature2_epic2 = self.create_system("As a user, I want to filter search results by categories, so that I can narrow down my search and find specific items", feature_us_type, org, parent=feature2_epic2)
        us3_feature2_epic2 = self.create_system("As a user, I want to see search suggestions as I type, so that I can find what I'm looking for more efficiently", feature_us_type, org, parent=feature2_epic2)
        us4_feature2_epic2 = self.create_system("As a user, I want to view my search history, so that I can easily revisit previous searches", feature_us_type, org, parent=feature2_epic2)

        # Add Tasks under User Stories for Feature 2 of Epic 2 (Improve Search Functionality)

        # Tasks for "As a user, I want to find relevant results quickly, so that I can access the information I need"
        task1_us1_feature2_epic2 = self.create_system("Optimize search algorithm for speed", us_feature_task_type, org, parent=us1_feature2_epic2)
        task2_us1_feature2_epic2 = self.create_system("Implement caching for search results", us_feature_task_type, org, parent=us1_feature2_epic2)
        task3_us1_feature2_epic2 = self.create_system("Index frequently searched terms", us_feature_task_type, org, parent=us1_feature2_epic2)
        task4_us1_feature2_epic2 = self.create_system("Write unit tests for search functionality", us_feature_task_type, org, parent=us1_feature2_epic2)
        task5_us1_feature2_epic2 = self.create_system("Deploy optimized search feature", us_feature_task_type, org, parent=us1_feature2_epic2)
        task6_us1_feature2_epic2 = self.create_system("Monitor search performance", us_feature_task_type, org, parent=us1_feature2_epic2)

        # Tasks for "As a user, I want to filter search results by categories, so that I can narrow down my search and find specific items"
        task1_us2_feature2_epic2 = self.create_system("Design UI for category filters", us_feature_task_type, org, parent=us2_feature2_epic2)
        task2_us2_feature2_epic2 = self.create_system("Implement backend logic for category filters", us_feature_task_type, org, parent=us2_feature2_epic2)
        task3_us2_feature2_epic2 = self.create_system("Integrate category filters with search functionality", us_feature_task_type, org, parent=us2_feature2_epic2)
        task4_us2_feature2_epic2 = self.create_system("Write unit tests for category filters", us_feature_task_type, org, parent=us2_feature2_epic2)
        task5_us2_feature2_epic2 = self.create_system("Deploy category filters feature", us_feature_task_type, org, parent=us2_feature2_epic2)
        task6_us2_feature2_epic2 = self.create_system("Monitor usage of category filters", us_feature_task_type, org, parent=us2_feature2_epic2)

        # Tasks for "As a user, I want to see search suggestions as I type, so that I can find what I'm looking for more efficiently"
        task1_us3_feature2_epic2 = self.create_system("Design UI for search suggestions", us_feature_task_type, org, parent=us3_feature2_epic2)
        task2_us3_feature2_epic2 = self.create_system("Implement search suggestions algorithm", us_feature_task_type, org, parent=us3_feature2_epic2)
        task3_us3_feature2_epic2 = self.create_system("Integrate search suggestions with search bar", us_feature_task_type, org, parent=us3_feature2_epic2)
        task4_us3_feature2_epic2 = self.create_system("Write unit tests for search suggestions", us_feature_task_type, org, parent=us3_feature2_epic2)
        task5_us3_feature2_epic2 = self.create_system("Deploy search suggestions feature", us_feature_task_type, org, parent=us3_feature2_epic2)
        task6_us3_feature2_epic2 = self.create_system("Monitor accuracy of search suggestions", us_feature_task_type, org, parent=us3_feature2_epic2)

        # Tasks for "As a user, I want to view my search history, so that I can easily revisit previous searches"
        task1_us4_feature2_epic2 = self.create_system("Design UI for search history", us_feature_task_type, org, parent=us4_feature2_epic2)
        task2_us4_feature2_epic2 = self.create_system("Implement backend logic for search history", us_feature_task_type, org, parent=us4_feature2_epic2)
        task3_us4_feature2_epic2 = self.create_system("Integrate search history with user accounts", us_feature_task_type, org, parent=us4_feature2_epic2)
        task4_us4_feature2_epic2 = self.create_system("Write unit tests for search history", us_feature_task_type, org, parent=us4_feature2_epic2)
        task5_us4_feature2_epic2 = self.create_system("Deploy search history feature", us_feature_task_type, org, parent=us4_feature2_epic2)
        task6_us4_feature2_epic2 = self.create_system("Monitor usage of search history", us_feature_task_type, org, parent=us4_feature2_epic2)

        # Add Spikes under Feature 2 of Epic 2 (Improve Search Functionality)
        spike1_feature2_epic2 = self.create_system("Spike: Explore ElasticSearch Integration for Advanced Search Features", feature_spike_type, org, parent=feature2_epic2)
        spike2_feature2_epic2 = self.create_system("Spike: Investigate User Interface Design for Search Bar and Filters", feature_spike_type, org, parent=feature2_epic2)
        spike3_feature2_epic2 = self.create_system("Spike: Research Search Algorithm Optimization Techniques for Faster and More Relevant Results", feature_spike_type, org, parent=feature2_epic2)

        # Add Tasks under Spikes for Feature 2 of Epic 2 (Improve Search Functionality)

        # Tasks for "Spike: Explore ElasticSearch Integration for Advanced Search Features"
        task1_spike1_feature2_epic2 = self.create_system("Review ElasticSearch documentation", spike_feature_task_type, org, parent=spike1_feature2_epic2)
        task2_spike1_feature2_epic2 = self.create_system("Set up ElasticSearch instance", spike_feature_task_type, org, parent=spike1_feature2_epic2)
        task3_spike1_feature2_epic2 = self.create_system("Create proof of concept for ElasticSearch integration", spike_feature_task_type, org, parent=spike1_feature2_epic2)
        task4_spike1_feature2_epic2 = self.create_system("Test search functionality with ElasticSearch", spike_feature_task_type, org, parent=spike1_feature2_epic2)
        task5_spike1_feature2_epic2 = self.create_system("Evaluate performance of ElasticSearch integration", spike_feature_task_type, org, parent=spike1_feature2_epic2)
        task6_spike1_feature2_epic2 = self.create_system("Document findings and recommendations for ElasticSearch integration", spike_feature_task_type, org, parent=spike1_feature2_epic2)

        # Tasks for "Spike: Investigate User Interface Design for Search Bar and Filters"
        task1_spike2_feature2_epic2 = self.create_system("Research best practices for search bar UI design", spike_feature_task_type, org, parent=spike2_feature2_epic2)
        task2_spike2_feature2_epic2 = self.create_system("Analyze competitor search bar designs", spike_feature_task_type, org, parent=spike2_feature2_epic2)
        task3_spike2_feature2_epic2 = self.create_system("Create design mockups for search bar and filters", spike_feature_task_type, org, parent=spike2_feature2_epic2)
        task4_spike2_feature2_epic2 = self.create_system("Conduct user testing for search bar design", spike_feature_task_type, org, parent=spike2_feature2_epic2)
        task5_spike2_feature2_epic2 = self.create_system("Iterate on design based on user feedback", spike_feature_task_type, org, parent=spike2_feature2_epic2)
        task6_spike2_feature2_epic2 = self.create_system("Document findings and recommendations for search bar UI", spike_feature_task_type, org, parent=spike2_feature2_epic2)

        # Tasks for "Spike: Research Search Algorithm Optimization Techniques for Faster and More Relevant Results"
        task1_spike3_feature2_epic2 = self.create_system("Review existing search algorithms", spike_feature_task_type, org, parent=spike3_feature2_epic2)
        task2_spike3_feature2_epic2 = self.create_system("Identify key factors affecting search relevance", spike_feature_task_type, org, parent=spike3_feature2_epic2)
        task3_spike3_feature2_epic2 = self.create_system("Implement sample optimizations for search algorithms", spike_feature_task_type, org, parent=spike3_feature2_epic2)
        task4_spike3_feature2_epic2 = self.create_system("Test optimized search algorithms", spike_feature_task_type, org, parent=spike3_feature2_epic2)
        task5_spike3_feature2_epic2 = self.create_system("Evaluate performance of optimized search algorithms", spike_feature_task_type, org, parent=spike3_feature2_epic2)
        task6_spike3_feature2_epic2 = self.create_system("Document findings and recommendations for search algorithm optimization", spike_feature_task_type, org, parent=spike3_feature2_epic2)

        ############################################################################################################################
        # Add for components 1 and 2 of Epic 1 and 2
        # Add User Stories under Component 1 of Epic 1 (Login Page)
        us1_component1_epic1 = self.create_system("As a user, I want to see a clear error message if I enter incorrect login details, so that I know what to correct", component_us_type, org, parent=component1_epic1)
        us2_component1_epic1 = self.create_system("As a user, I want the login page to remember my email address for future logins, so that I can log in faster", component_us_type, org, parent=component1_epic1)
        us3_component1_epic1 = self.create_system("As a user, I want to be able to see my password as I type it, so that I can avoid mistakes", component_us_type, org, parent=component1_epic1)
        us4_component1_epic1 = self.create_system("As a user, I want to log in using my social media accounts (e.g., Google, Facebook), so that I can log in quickly and easily", component_us_type, org, parent=component1_epic1)
        us5_component1_epic1 = self.create_system("As a user, I want to be redirected to the homepage after a successful login, so that I can start using the app immediately", component_us_type, org, parent=component1_epic1)

        # Add Tasks under User Stories for Component 1 of Epic 1 (Login Page)

        # Tasks for "As a user, I want to see a clear error message if I enter incorrect login details, so that I know what to correct"
        task1_us1_component1_epic1 = self.create_system("Design error message UI", us_component_task_type, org, parent=us1_component1_epic1)
        task2_us1_component1_epic1 = self.create_system("Implement error message logic", us_component_task_type, org, parent=us1_component1_epic1)
        task3_us1_component1_epic1 = self.create_system("Integrate error message with login form", us_component_task_type, org, parent=us1_component1_epic1)
        task4_us1_component1_epic1 = self.create_system("Write unit tests for error messages", us_component_task_type, org, parent=us1_component1_epic1)
        task5_us1_component1_epic1 = self.create_system("Deploy error message feature", us_component_task_type, org, parent=us1_component1_epic1)
        task6_us1_component1_epic1 = self.create_system("Monitor error message feature", us_component_task_type, org, parent=us1_component1_epic1)

        # Tasks for "As a user, I want the login page to remember my email address for future logins, so that I can log in faster"
        task1_us2_component1_epic1 = self.create_system("Design email remember UI", us_component_task_type, org, parent=us2_component1_epic1)
        task2_us2_component1_epic1 = self.create_system("Implement email remember logic", us_component_task_type, org, parent=us2_component1_epic1)
        task3_us2_component1_epic1 = self.create_system("Integrate email remember feature with login form", us_component_task_type, org, parent=us2_component1_epic1)
        task4_us2_component1_epic1 = self.create_system("Write unit tests for email remember feature", us_component_task_type, org, parent=us2_component1_epic1)
        task5_us2_component1_epic1 = self.create_system("Deploy email remember feature", us_component_task_type, org, parent=us2_component1_epic1)
        task6_us2_component1_epic1 = self.create_system("Monitor email remember feature", us_component_task_type, org, parent=us2_component1_epic1)

        # Tasks for "As a user, I want to be able to see my password as I type it, so that I can avoid mistakes"
        task1_us3_component1_epic1 = self.create_system("Design show password UI", us_component_task_type, org, parent=us3_component1_epic1)
        task2_us3_component1_epic1 = self.create_system("Implement show password logic", us_component_task_type, org, parent=us3_component1_epic1)
        task3_us3_component1_epic1 = self.create_system("Integrate show password feature with login form", us_component_task_type, org, parent=us3_component1_epic1)
        task4_us3_component1_epic1 = self.create_system("Write unit tests for show password feature", us_component_task_type, org, parent=us3_component1_epic1)
        task5_us3_component1_epic1 = self.create_system("Deploy show password feature", us_component_task_type, org, parent=us3_component1_epic1)
        task6_us3_component1_epic1 = self.create_system("Monitor show password feature", us_component_task_type, org, parent=us3_component1_epic1)

        # Tasks for "As a user, I want to log in using my social media accounts (e.g., Google, Facebook), so that I can log in quickly and easily"
        task1_us4_component1_epic1 = self.create_system("Design social media login UI", us_component_task_type, org, parent=us4_component1_epic1)
        task2_us4_component1_epic1 = self.create_system("Implement social media login logic", us_component_task_type, org, parent=us4_component1_epic1)
        task3_us4_component1_epic1 = self.create_system("Integrate social media login with login form", us_component_task_type, org, parent=us4_component1_epic1)
        task4_us4_component1_epic1 = self.create_system("Write unit tests for social media login", us_component_task_type, org, parent=us4_component1_epic1)
        task5_us4_component1_epic1 = self.create_system("Deploy social media login feature", us_component_task_type, org, parent=us4_component1_epic1)
        task6_us4_component1_epic1 = self.create_system("Monitor social media login feature", us_component_task_type, org, parent=us4_component1_epic1)

        # Tasks for "As a user, I want to be redirected to the homepage after a successful login, so that I can start using the app immediately"
        task1_us5_component1_epic1 = self.create_system("Design redirection logic", us_component_task_type, org, parent=us5_component1_epic1)
        task2_us5_component1_epic1 = self.create_system("Implement redirection logic", us_component_task_type, org, parent=us5_component1_epic1)
        task3_us5_component1_epic1 = self.create_system("Integrate redirection with login feature", us_component_task_type, org, parent=us5_component1_epic1)
        task4_us5_component1_epic1 = self.create_system("Write unit tests for redirection feature", us_component_task_type, org, parent=us5_component1_epic1)
        task5_us5_component1_epic1 = self.create_system("Deploy redirection feature", us_component_task_type, org, parent=us5_component1_epic1)
        task6_us5_component1_epic1 = self.create_system("Monitor redirection feature", us_component_task_type, org, parent=us5_component1_epic1)

        # Add User Stories under Component 2 of Epic 1 (Notification Service)
        us1_component2_epic1 = self.create_system("As a user, I want to manage my notification preferences from the settings page, so that I can control which notifications I receive", component_us_type, org, parent=component2_epic1)
        us2_component2_epic1 = self.create_system("As a user, I want to receive a daily summary of my notifications, so that I can stay informed without being overwhelmed", component_us_type, org, parent=component2_epic1)
        us3_component2_epic1 = self.create_system("As a user, I want to be able to mute notifications during specific hours, so that I am not disturbed at inconvenient times", component_us_type, org, parent=component2_epic1)
        us4_component2_epic1 = self.create_system("As a user, I want to receive push notifications even when the app is closed, so that I stay informed about important updates", component_us_type, org, parent=component2_epic1)
        us5_component2_epic1 = self.create_system("As a user, I want to be able to clear all notifications with a single tap, so that I can manage my notifications efficiently", component_us_type, org, parent=component2_epic1)

        # Add Tasks under User Stories for Component 2 of Epic 1 (Notification Service)

        # Tasks for "As a user, I want to manage my notification preferences from the settings page, so that I can control which notifications I receive"
        task1_us1_component2_epic1 = self.create_system("Design notification preferences UI", us_component_task_type, org, parent=us1_component2_epic1)
        task2_us1_component2_epic1 = self.create_system("Implement notification preferences backend logic", us_component_task_type, org, parent=us1_component2_epic1)
        task3_us1_component2_epic1 = self.create_system("Integrate notification preferences with settings page", us_component_task_type, org, parent=us1_component2_epic1)
        task4_us1_component2_epic1 = self.create_system("Write unit tests for notification preferences", us_component_task_type, org, parent=us1_component2_epic1)
        task5_us1_component2_epic1 = self.create_system("Deploy notification preferences feature", us_component_task_type, org, parent=us1_component2_epic1)
        task6_us1_component2_epic1 = self.create_system("Monitor notification preferences usage", us_component_task_type, org, parent=us1_component2_epic1)

        # Tasks for "As a user, I want to receive a daily summary of my notifications, so that I can stay informed without being overwhelmed"
        task1_us2_component2_epic1 = self.create_system("Design daily summary notification UI", us_component_task_type, org, parent=us2_component2_epic1)
        task2_us2_component2_epic1 = self.create_system("Implement daily summary backend logic", us_component_task_type, org, parent=us2_component2_epic1)
        task3_us2_component2_epic1 = self.create_system("Integrate daily summary with notification service", us_component_task_type, org, parent=us2_component2_epic1)
        task4_us2_component2_epic1 = self.create_system("Write unit tests for daily summary notifications", us_component_task_type, org, parent=us2_component2_epic1)
        task5_us2_component2_epic1 = self.create_system("Deploy daily summary notification feature", us_component_task_type, org, parent=us2_component2_epic1)
        task6_us2_component2_epic1 = self.create_system("Monitor daily summary notifications", us_component_task_type, org, parent=us2_component2_epic1)

        # Tasks for "As a user, I want to be able to mute notifications during specific hours, so that I am not disturbed at inconvenient times"
        task1_us3_component2_epic1 = self.create_system("Design mute notifications UI", us_component_task_type, org, parent=us3_component2_epic1)
        task2_us3_component2_epic1 = self.create_system("Implement mute notifications backend logic", us_component_task_type, org, parent=us3_component2_epic1)
        task3_us3_component2_epic1 = self.create_system("Integrate mute notifications with settings page", us_component_task_type, org, parent=us3_component2_epic1)
        task4_us3_component2_epic1 = self.create_system("Write unit tests for mute notifications", us_component_task_type, org, parent=us3_component2_epic1)
        task5_us3_component2_epic1 = self.create_system("Deploy mute notifications feature", us_component_task_type, org, parent=us3_component2_epic1)
        task6_us3_component2_epic1 = self.create_system("Monitor mute notifications usage", us_component_task_type, org, parent=us3_component2_epic1)

        # Tasks for "As a user, I want to receive push notifications even when the app is closed, so that I stay informed about important updates"
        task1_us4_component2_epic1 = self.create_system("Design push notification UI", us_component_task_type, org, parent=us4_component2_epic1)
        task2_us4_component2_epic1 = self.create_system("Implement push notification backend logic", us_component_task_type, org, parent=us4_component2_epic1)
        task3_us4_component2_epic1 = self.create_system("Integrate push notifications with notification service", us_component_task_type, org, parent=us4_component2_epic1)
        task4_us4_component2_epic1 = self.create_system("Write unit tests for push notifications", us_component_task_type, org, parent=us4_component2_epic1)
        task5_us4_component2_epic1 = self.create_system("Deploy push notification feature", us_component_task_type, org, parent=us4_component2_epic1)
        task6_us4_component2_epic1 = self.create_system("Monitor push notification usage", us_component_task_type, org, parent=us4_component2_epic1)

        # Tasks for "As a user, I want to be able to clear all notifications with a single tap, so that I can manage my notifications efficiently"
        task1_us5_component2_epic1 = self.create_system("Design clear all notifications UI", us_component_task_type, org, parent=us5_component2_epic1)
        task2_us5_component2_epic1 = self.create_system("Implement clear all notifications backend logic", us_component_task_type, org, parent=us5_component2_epic1)
        task3_us5_component2_epic1 = self.create_system("Integrate clear all notifications with notification service", us_component_task_type, org, parent=us5_component2_epic1)
        task4_us5_component2_epic1 = self.create_system("Write unit tests for clear all notifications", us_component_task_type, org, parent=us5_component2_epic1)
        task5_us5_component2_epic1 = self.create_system("Deploy clear all notifications feature", us_component_task_type, org, parent=us5_component2_epic1)
        task6_us5_component2_epic1 = self.create_system("Monitor clear all notifications usage", us_component_task_type, org, parent=us5_component2_epic1)

        # Add User Stories under Component 1 of Epic 2 (Home Page Design)
        us1_component1_epic2 = self.create_system("As a user, I want the home page to load quickly, so that I can start using the app without delay", component_us_type, org, parent=component1_epic2)
        us2_component1_epic2 = self.create_system("As a user, I want the home page to be visually appealing, so that I have a pleasant experience using the app", component_us_type, org, parent=component1_epic2)
        us3_component1_epic2 = self.create_system("As a user, I want the home page to highlight key features of the app, so that I can easily find and use them", component_us_type, org, parent=component1_epic2)
        us4_component1_epic2 = self.create_system("As a user, I want the home page to be easy to navigate, so that I can find what I need quickly", component_us_type, org, parent=component1_epic2)
        us5_component1_epic2 = self.create_system("As a user, I want to see personalized content on the home page, so that the app is more relevant to my interests", component_us_type, org, parent=component1_epic2)

        # Add Tasks under User Stories for Component 1 of Epic 2 (Home Page Design)

        # Tasks for "As a user, I want the home page to load quickly, so that I can start using the app without delay"
        task1_us1_component1_epic2 = self.create_system("Optimize image loading", us_component_task_type, org, parent=us1_component1_epic2)
        task2_us1_component1_epic2 = self.create_system("Minimize CSS and JS", us_component_task_type, org, parent=us1_component1_epic2)
        task3_us1_component1_epic2 = self.create_system("Implement lazy loading", us_component_task_type, org, parent=us1_component1_epic2)
        task4_us1_component1_epic2 = self.create_system("Reduce server response time", us_component_task_type, org, parent=us1_component1_epic2)
        task5_us1_component1_epic2 = self.create_system("Conduct performance testing", us_component_task_type, org, parent=us1_component1_epic2)
        task6_us1_component1_epic2 = self.create_system("Monitor home page load speed", us_component_task_type, org, parent=us1_component1_epic2)

        # Tasks for "As a user, I want the home page to be visually appealing, so that I have a pleasant experience using the app"
        task1_us2_component1_epic2 = self.create_system("Redesign home page layout", us_component_task_type, org, parent=us2_component1_epic2)
        task2_us2_component1_epic2 = self.create_system("Choose color scheme", us_component_task_type, org, parent=us2_component1_epic2)
        task3_us2_component1_epic2 = self.create_system("Update fonts and typography", us_component_task_type, org, parent=us2_component1_epic2)
        task4_us2_component1_epic2 = self.create_system("Add engaging visuals", us_component_task_type, org, parent=us2_component1_epic2)
        task5_us2_component1_epic2 = self.create_system("Implement animations", us_component_task_type, org, parent=us2_component1_epic2)
        task6_us2_component1_epic2 = self.create_system("Gather user feedback on design", us_component_task_type, org, parent=us2_component1_epic2)

        # Tasks for "As a user, I want the home page to highlight key features of the app, so that I can easily find and use them"
        task1_us3_component1_epic2 = self.create_system("Identify key features to highlight", us_component_task_type, org, parent=us3_component1_epic2)
        task2_us3_component1_epic2 = self.create_system("Design feature highlight sections", us_component_task_type, org, parent=us3_component1_epic2)
        task3_us3_component1_epic2 = self.create_system("Implement feature highlights", us_component_task_type, org, parent=us3_component1_epic2)
        task4_us3_component1_epic2 = self.create_system("Write content for feature highlights", us_component_task_type, org, parent=us3_component1_epic2)
        task5_us3_component1_epic2 = self.create_system("Test feature highlight functionality", us_component_task_type, org, parent=us3_component1_epic2)
        task6_us3_component1_epic2 = self.create_system("Monitor user interaction with feature highlights", us_component_task_type, org, parent=us3_component1_epic2)

        # Tasks for "As a user, I want the home page to be easy to navigate, so that I can find what I need quickly"
        task1_us4_component1_epic2 = self.create_system("Design intuitive navigation menu", us_component_task_type, org, parent=us4_component1_epic2)
        task2_us4_component1_epic2 = self.create_system("Implement navigation menu", us_component_task_type, org, parent=us4_component1_epic2)
        task3_us4_component1_epic2 = self.create_system("Add search functionality", us_component_task_type, org, parent=us4_component1_epic2)
        task4_us4_component1_epic2 = self.create_system("Write user guides for navigation", us_component_task_type, org, parent=us4_component1_epic2)
        task5_us4_component1_epic2 = self.create_system("Test navigation flow", us_component_task_type, org, parent=us4_component1_epic2)
        task6_us4_component1_epic2 = self.create_system("Monitor user navigation patterns", us_component_task_type, org, parent=us4_component1_epic2)

        # Tasks for "As a user, I want to see personalized content on the home page, so that the app is more relevant to my interests"
        task1_us5_component1_epic2 = self.create_system("Design personalized content UI", us_component_task_type, org, parent=us5_component1_epic2)
        task2_us5_component1_epic2 = self.create_system("Implement backend logic for personalized content", us_component_task_type, org, parent=us5_component1_epic2)
        task3_us5_component1_epic2 = self.create_system("Integrate personalized content with home page", us_component_task_type, org, parent=us5_component1_epic2)
        task4_us5_component1_epic2 = self.create_system("Write unit tests for personalized content", us_component_task_type, org, parent=us5_component1_epic2)
        task5_us5_component1_epic2 = self.create_system("Deploy personalized content feature", us_component_task_type, org, parent=us5_component1_epic2)
        task6_us5_component1_epic2 = self.create_system("Monitor personalized content usage", us_component_task_type, org, parent=us5_component1_epic2)

        # Add User Stories under Component 2 of Epic 2 (Search Bar)
        us1_component2_epic2 = self.create_system("As a user, I want to find relevant results quickly using the search bar, so that I can access the information I need", component_us_type, org, parent=component2_epic2)
        us2_component2_epic2 = self.create_system("As a user, I want to filter search results by categories, so that I can narrow down my search and find specific items", component_us_type, org, parent=component2_epic2)
        us3_component2_epic2 = self.create_system("As a user, I want to see search suggestions as I type, so that I can find what I'm looking for more efficiently", component_us_type, org, parent=component2_epic2)
        us4_component2_epic2 = self.create_system("As a user, I want to view my search history, so that I can easily revisit previous searches", component_us_type, org, parent=component2_epic2)
        us5_component2_epic2 = self.create_system("As a user, I want to search using voice commands, so that I can perform searches hands-free", component_us_type, org, parent=component2_epic2)

        # Add Tasks under User Stories for Component 2 of Epic 2 (Search Bar)

        # Tasks for "As a user, I want to find relevant results quickly using the search bar, so that I can access the information I need"
        task1_us1_component2_epic2 = self.create_system("Optimize search algorithm for speed", us_component_task_type, org, parent=us1_component2_epic2)
        task2_us1_component2_epic2 = self.create_system("Implement caching for search results", us_component_task_type, org, parent=us1_component2_epic2)
        task3_us1_component2_epic2 = self.create_system("Index frequently searched terms", us_component_task_type, org, parent=us1_component2_epic2)
        task4_us1_component2_epic2 = self.create_system("Write unit tests for search functionality", us_component_task_type, org, parent=us1_component2_epic2)
        task5_us1_component2_epic2 = self.create_system("Deploy optimized search feature", us_component_task_type, org, parent=us1_component2_epic2)
        task6_us1_component2_epic2 = self.create_system("Monitor search performance", us_component_task_type, org, parent=us1_component2_epic2)

        # Tasks for "As a user, I want to filter search results by categories, so that I can narrow down my search and find specific items"
        task1_us2_component2_epic2 = self.create_system("Design UI for category filters", us_component_task_type, org, parent=us2_component2_epic2)
        task2_us2_component2_epic2 = self.create_system("Implement backend logic for category filters", us_component_task_type, org, parent=us2_component2_epic2)
        task3_us2_component2_epic2 = self.create_system("Integrate category filters with search functionality", us_component_task_type, org, parent=us2_component2_epic2)
        task4_us2_component2_epic2 = self.create_system("Write unit tests for category filters", us_component_task_type, org, parent=us2_component2_epic2)
        task5_us2_component2_epic2 = self.create_system("Deploy category filters feature", us_component_task_type, org, parent=us2_component2_epic2)
        task6_us2_component2_epic2 = self.create_system("Monitor usage of category filters", us_component_task_type, org, parent=us2_component2_epic2)

        # Tasks for "As a user, I want to see search suggestions as I type, so that I can find what I'm looking for more efficiently"
        task1_us3_component2_epic2 = self.create_system("Design UI for search suggestions", us_component_task_type, org, parent=us3_component2_epic2)
        task2_us3_component2_epic2 = self.create_system("Implement search suggestions algorithm", us_component_task_type, org, parent=us3_component2_epic2)
        task3_us3_component2_epic2 = self.create_system("Integrate search suggestions with search bar", us_component_task_type, org, parent=us3_component2_epic2)
        task4_us3_component2_epic2 = self.create_system("Write unit tests for search suggestions", us_component_task_type, org, parent=us3_component2_epic2)
        task5_us3_component2_epic2 = self.create_system("Deploy search suggestions feature", us_component_task_type, org, parent=us3_component2_epic2)
        task6_us3_component2_epic2 = self.create_system("Monitor accuracy of search suggestions", us_component_task_type, org, parent=us3_component2_epic2)

        # Tasks for "As a user, I want to view my search history, so that I can easily revisit previous searches"
        task1_us4_component2_epic2 = self.create_system("Design UI for search history", us_component_task_type, org, parent=us4_component2_epic2)
        task2_us4_component2_epic2 = self.create_system("Implement backend logic for search history", us_component_task_type, org, parent=us4_component2_epic2)
        task3_us4_component2_epic2 = self.create_system("Integrate search history with user accounts", us_component_task_type, org, parent=us4_component2_epic2)
        task4_us4_component2_epic2 = self.create_system("Write unit tests for search history", us_component_task_type, org, parent=us4_component2_epic2)
        task5_us4_component2_epic2 = self.create_system("Deploy search history feature", us_component_task_type, org, parent=us4_component2_epic2)
        task6_us4_component2_epic2 = self.create_system("Monitor usage of search history", us_component_task_type, org, parent=us4_component2_epic2)

        # Tasks for "As a user, I want to search using voice commands, so that I can perform searches hands-free"
        task1_us5_component2_epic2 = self.create_system("Design UI for voice search", us_component_task_type, org, parent=us5_component2_epic2)
        task2_us5_component2_epic2 = self.create_system("Implement voice recognition algorithm", us_component_task_type, org, parent=us5_component2_epic2)
        task3_us5_component2_epic2 = self.create_system("Integrate voice search with search functionality", us_component_task_type, org, parent=us5_component2_epic2)
        task4_us5_component2_epic2 = self.create_system("Write unit tests for voice search", us_component_task_type, org, parent=us5_component2_epic2)
        task5_us5_component2_epic2 = self.create_system("Deploy voice search feature", us_component_task_type, org, parent=us5_component2_epic2)
        task6_us5_component2_epic2 = self.create_system("Monitor voice search usage", us_component_task_type, org, parent=us5_component2_epic2)


        ############################################################################################################################
        # Add for capabilities 1 and 2 of Epic 1 and 2
        # Add User Stories under Capability 1 of Epic 1 (OAuth2 Integration)
        us1_capability1_epic1 = self.create_system("As a user, I want to log in using my Google account, so that I can access the app without creating a new account", capability_us_type, org, parent=capability1_epic1)
        us2_capability1_epic1 = self.create_system("As a user, I want to log in using my Facebook account, so that I can quickly access the app with my social media credentials", capability_us_type, org, parent=capability1_epic1)
        us3_capability1_epic1 = self.create_system("As a user, I want to see a list of available OAuth2 providers, so that I can choose my preferred login method", capability_us_type, org, parent=capability1_epic1)
        us4_capability1_epic1 = self.create_system("As a user, I want to link my existing app account with my social media accounts, so that I can log in using multiple methods", capability_us_type, org, parent=capability1_epic1)
        us5_capability1_epic1 = self.create_system("As a user, I want to revoke OAuth2 access from my account settings, so that I can secure my account if needed", capability_us_type, org, parent=capability1_epic1)

        # Add Tasks under User Stories for Capability 1 of Epic 1 (OAuth2 Integration)

        # Tasks for "As a user, I want to log in using my Google account, so that I can access the app without creating a new account"
        task1_us1_capability1_epic1 = self.create_system("Integrate Google OAuth2 API", us_capability_task_type, org, parent=us1_capability1_epic1)
        task2_us1_capability1_epic1 = self.create_system("Design Google login button", us_capability_task_type, org, parent=us1_capability1_epic1)
        task3_us1_capability1_epic1 = self.create_system("Implement Google login functionality", us_capability_task_type, org, parent=us1_capability1_epic1)
        task4_us1_capability1_epic1 = self.create_system("Test Google login integration", us_capability_task_type, org, parent=us1_capability1_epic1)
        task5_us1_capability1_epic1 = self.create_system("Write documentation for Google login", us_capability_task_type, org, parent=us1_capability1_epic1)
        task6_us1_capability1_epic1 = self.create_system("Deploy Google login feature", us_capability_task_type, org, parent=us1_capability1_epic1)

        # Tasks for "As a user, I want to log in using my Facebook account, so that I can quickly access the app with my social media credentials"
        task1_us2_capability1_epic1 = self.create_system("Integrate Facebook OAuth2 API", us_capability_task_type, org, parent=us2_capability1_epic1)
        task2_us2_capability1_epic1 = self.create_system("Design Facebook login button", us_capability_task_type, org, parent=us2_capability1_epic1)
        task3_us2_capability1_epic1 = self.create_system("Implement Facebook login functionality", us_capability_task_type, org, parent=us2_capability1_epic1)
        task4_us2_capability1_epic1 = self.create_system("Test Facebook login integration", us_capability_task_type, org, parent=us2_capability1_epic1)
        task5_us2_capability1_epic1 = self.create_system("Write documentation for Facebook login", us_capability_task_type, org, parent=us2_capability1_epic1)
        task6_us2_capability1_epic1 = self.create_system("Deploy Facebook login feature", us_capability_task_type, org, parent=us2_capability1_epic1)

        # Tasks for "As a user, I want to see a list of available OAuth2 providers, so that I can choose my preferred login method"
        task1_us3_capability1_epic1 = self.create_system("Compile list of available OAuth2 providers", us_capability_task_type, org, parent=us3_capability1_epic1)
        task2_us3_capability1_epic1 = self.create_system("Design UI for OAuth2 provider list", us_capability_task_type, org, parent=us3_capability1_epic1)
        task3_us3_capability1_epic1 = self.create_system("Implement OAuth2 provider selection functionality", us_capability_task_type, org, parent=us3_capability1_epic1)
        task4_us3_capability1_epic1 = self.create_system("Test OAuth2 provider selection", us_capability_task_type, org, parent=us3_capability1_epic1)
        task5_us3_capability1_epic1 = self.create_system("Write documentation for OAuth2 provider selection", us_capability_task_type, org, parent=us3_capability1_epic1)
        task6_us3_capability1_epic1 = self.create_system("Deploy OAuth2 provider selection feature", us_capability_task_type, org, parent=us3_capability1_epic1)

        # Tasks for "As a user, I want to link my existing app account with my social media accounts, so that I can log in using multiple methods"
        task1_us4_capability1_epic1 = self.create_system("Implement account linking functionality", us_capability_task_type, org, parent=us4_capability1_epic1)
        task2_us4_capability1_epic1 = self.create_system("Design UI for account linking", us_capability_task_type, org, parent=us4_capability1_epic1)
        task3_us4_capability1_epic1 = self.create_system("Test account linking feature", us_capability_task_type, org, parent=us4_capability1_epic1)
        task4_us4_capability1_epic1 = self.create_system("Write documentation for account linking", us_capability_task_type, org, parent=us4_capability1_epic1)
        task5_us4_capability1_epic1 = self.create_system("Deploy account linking feature", us_capability_task_type, org, parent=us4_capability1_epic1)
        task6_us4_capability1_epic1 = self.create_system("Monitor account linking usage", us_capability_task_type, org, parent=us4_capability1_epic1)

        # Tasks for "As a user, I want to revoke OAuth2 access from my account settings, so that I can secure my account if needed"
        task1_us5_capability1_epic1 = self.create_system("Implement OAuth2 revocation functionality", us_capability_task_type, org, parent=us5_capability1_epic1)
        task2_us5_capability1_epic1 = self.create_system("Design UI for OAuth2 revocation", us_capability_task_type, org, parent=us5_capability1_epic1)
        task3_us5_capability1_epic1 = self.create_system("Test OAuth2 revocation feature", us_capability_task_type, org, parent=us5_capability1_epic1)
        task4_us5_capability1_epic1 = self.create_system("Write documentation for OAuth2 revocation", us_capability_task_type, org, parent=us5_capability1_epic1)
        task5_us5_capability1_epic1 = self.create_system("Deploy OAuth2 revocation feature", us_capability_task_type, org, parent=us5_capability1_epic1)
        task6_us5_capability1_epic1 = self.create_system("Monitor OAuth2 revocation usage", us_capability_task_type, org, parent=us5_capability1_epic1)


        # Add User Stories under Capability 2 of Epic 1 (Firebase Cloud Messaging)
        us1_capability2_epic1 = self.create_system("As a user, I want to receive real-time push notifications, so that I am immediately informed about important updates", capability_us_type, org, parent=capability2_epic1)
        us2_capability2_epic1 = self.create_system("As a user, I want to receive notifications even when the app is closed, so that I don’t miss any important messages", capability_us_type, org, parent=capability2_epic1)
        us3_capability2_epic1 = self.create_system("As a user, I want to customize notification sounds, so that I can differentiate app notifications from others", capability_us_type, org, parent=capability2_epic1)
        us4_capability2_epic1 = self.create_system("As a user, I want to receive notifications based on my preferences, so that I only get relevant updates", capability_us_type, org, parent=capability2_epic1)
        us5_capability2_epic1 = self.create_system("As a user, I want to see a history of received notifications, so that I can review past messages", capability_us_type, org, parent=capability2_epic1)

        # Add Tasks under User Stories for Capability 2 of Epic 1 (Firebase Cloud Messaging)

        # Tasks for "As a user, I want to receive real-time push notifications, so that I am immediately informed about important updates"
        task1_us1_capability2_epic1 = self.create_system("Integrate Firebase Cloud Messaging API", us_capability_task_type, org, parent=us1_capability2_epic1)
        task2_us1_capability2_epic1 = self.create_system("Design push notification UI", us_capability_task_type, org, parent=us1_capability2_epic1)
        task3_us1_capability2_epic1 = self.create_system("Implement push notification functionality", us_capability_task_type, org, parent=us1_capability2_epic1)
        task4_us1_capability2_epic1 = self.create_system("Test real-time push notifications", us_capability_task_type, org, parent=us1_capability2_epic1)
        task5_us1_capability2_epic1 = self.create_system("Write documentation for push notifications", us_capability_task_type, org, parent=us1_capability2_epic1)
        task6_us1_capability2_epic1 = self.create_system("Deploy real-time push notification feature", us_capability_task_type, org, parent=us1_capability2_epic1)

        # Tasks for "As a user, I want to receive notifications even when the app is closed, so that I don’t miss any important messages"
        task1_us2_capability2_epic1 = self.create_system("Ensure background notification support", us_capability_task_type, org, parent=us2_capability2_epic1)
        task2_us2_capability2_epic1 = self.create_system("Test notifications with app closed", us_capability_task_type, org, parent=us2_capability2_epic1)
        task3_us2_capability2_epic1 = self.create_system("Implement persistent notification service", us_capability_task_type, org, parent=us2_capability2_epic1)
        task4_us2_capability2_epic1 = self.create_system("Write unit tests for background notifications", us_capability_task_type, org, parent=us2_capability2_epic1)
        task5_us2_capability2_epic1 = self.create_system("Deploy background notification feature", us_capability_task_type, org, parent=us2_capability2_epic1)
        task6_us2_capability2_epic1 = self.create_system("Monitor background notification performance", us_capability_task_type, org, parent=us2_capability2_epic1)

        # Tasks for "As a user, I want to customize notification sounds, so that I can differentiate app notifications from others"
        task1_us3_capability2_epic1 = self.create_system("Design UI for notification sound settings", us_capability_task_type, org, parent=us3_capability2_epic1)
        task2_us3_capability2_epic1 = self.create_system("Implement custom notification sound functionality", us_capability_task_type, org, parent=us3_capability2_epic1)
        task3_us3_capability2_epic1 = self.create_system("Test custom notification sounds", us_capability_task_type, org, parent=us3_capability2_epic1)
        task4_us3_capability2_epic1 = self.create_system("Write documentation for custom notification sounds", us_capability_task_type, org, parent=us3_capability2_epic1)
        task5_us3_capability2_epic1 = self.create_system("Deploy custom notification sound feature", us_capability_task_type, org, parent=us3_capability2_epic1)
        task6_us3_capability2_epic1 = self.create_system("Monitor custom notification sound usage", us_capability_task_type, org, parent=us3_capability2_epic1)

        # Tasks for "As a user, I want to receive notifications based on my preferences, so that I only get relevant updates"
        task1_us4_capability2_epic1 = self.create_system("Design UI for notification preferences", us_capability_task_type, org, parent=us4_capability2_epic1)
        task2_us4_capability2_epic1 = self.create_system("Implement backend logic for notification preferences", us_capability_task_type, org, parent=us4_capability2_epic1)
        task3_us4_capability2_epic1 = self.create_system("Integrate notification preferences with notification service", us_capability_task_type, org, parent=us4_capability2_epic1)
        task4_us4_capability2_epic1 = self.create_system("Write unit tests for notification preferences", us_capability_task_type, org, parent=us4_capability2_epic1)
        task5_us4_capability2_epic1 = self.create_system("Deploy notification preferences feature", us_capability_task_type, org, parent=us4_capability2_epic1)
        task6_us4_capability2_epic1 = self.create_system("Monitor usage of notification preferences", us_capability_task_type, org, parent=us4_capability2_epic1)

        # Tasks for "As a user, I want to see a history of received notifications, so that I can review past messages"
        task1_us5_capability2_epic1 = self.create_system("Design UI for notification history", us_capability_task_type, org, parent=us5_capability2_epic1)
        task2_us5_capability2_epic1 = self.create_system("Implement backend logic for notification history", us_capability_task_type, org, parent=us5_capability2_epic1)
        task3_us5_capability2_epic1 = self.create_system("Integrate notification history with user accounts", us_capability_task_type, org, parent=us5_capability2_epic1)
        task4_us5_capability2_epic1 = self.create_system("Write unit tests for notification history", us_capability_task_type, org, parent=us5_capability2_epic1)
        task5_us5_capability2_epic1 = self.create_system("Deploy notification history feature", us_capability_task_type, org, parent=us5_capability2_epic1)
        task6_us5_capability2_epic1 = self.create_system("Monitor usage of notification history", us_capability_task_type, org, parent=us5_capability2_epic1)

        # Add User Stories under Capability 1 of Epic 2 (Responsive Design)
        us1_capability1_epic2 = self.create_system("As a user, I want the website to adapt to my device's screen size, so that I have a consistent experience on any device", capability_us_type, org, parent=capability1_epic2)
        us2_capability1_epic2 = self.create_system("As a user, I want images and text to resize automatically, so that I can read and view content comfortably", capability_us_type, org, parent=capability1_epic2)
        us3_capability1_epic2 = self.create_system("As a user, I want the navigation menu to be easy to use on both mobile and desktop, so that I can find what I need quickly", capability_us_type, org, parent=capability1_epic2)
        us4_capability1_epic2 = self.create_system("As a user, I want touch-friendly controls on mobile devices, so that I can interact with the website easily", capability_us_type, org, parent=capability1_epic2)
        us5_capability1_epic2 = self.create_system("As a user, I want the website to load quickly on all devices, so that I can start using it without delay", capability_us_type, org, parent=capability1_epic2)

        # Add Tasks under User Stories for Capability 1 of Epic 2 (Responsive Design)

        # Tasks for "As a user, I want the website to adapt to my device's screen size, so that I have a consistent experience on any device"
        task1_us1_capability1_epic2 = self.create_system("Implement responsive design using CSS media queries", us_capability_task_type, org, parent=us1_capability1_epic2)
        task2_us1_capability1_epic2 = self.create_system("Test responsiveness on various screen sizes", us_capability_task_type, org, parent=us1_capability1_epic2)
        task3_us1_capability1_epic2 = self.create_system("Ensure consistent layout across devices", us_capability_task_type, org, parent=us1_capability1_epic2)
        task4_us1_capability1_epic2 = self.create_system("Write documentation for responsive design implementation", us_capability_task_type, org, parent=us1_capability1_epic2)
        task5_us1_capability1_epic2 = self.create_system("Deploy responsive design updates", us_capability_task_type, org, parent=us1_capability1_epic2)
        task6_us1_capability1_epic2 = self.create_system("Monitor user feedback on responsiveness", us_capability_task_type, org, parent=us1_capability1_epic2)

        # Tasks for "As a user, I want images and text to resize automatically, so that I can read and view content comfortably"
        task1_us2_capability1_epic2 = self.create_system("Implement fluid grid layout", us_capability_task_type, org, parent=us2_capability1_epic2)
        task2_us2_capability1_epic2 = self.create_system("Use scalable vector graphics (SVG) for images", us_capability_task_type, org, parent=us2_capability1_epic2)
        task3_us2_capability1_epic2 = self.create_system("Apply responsive typography techniques", us_capability_task_type, org, parent=us2_capability1_epic2)
        task4_us2_capability1_epic2 = self.create_system("Test resizing of images and text on various devices", us_capability_task_type, org, parent=us2_capability1_epic2)
        task5_us2_capability1_epic2 = self.create_system("Write documentation for responsive images and text", us_capability_task_type, org, parent=us2_capability1_epic2)
        task6_us2_capability1_epic2 = self.create_system("Deploy updates for responsive images and text", us_capability_task_type, org, parent=us2_capability1_epic2)

        # Tasks for "As a user, I want the navigation menu to be easy to use on both mobile and desktop, so that I can find what I need quickly"
        task1_us3_capability1_epic2 = self.create_system("Design mobile-friendly navigation menu", us_capability_task_type, org, parent=us3_capability1_epic2)
        task2_us3_capability1_epic2 = self.create_system("Implement responsive navigation menu", us_capability_task_type, org, parent=us3_capability1_epic2)
        task3_us3_capability1_epic2 = self.create_system("Test navigation menu on various devices", us_capability_task_type, org, parent=us3_capability1_epic2)
        task4_us3_capability1_epic2 = self.create_system("Write documentation for responsive navigation menu", us_capability_task_type, org, parent=us3_capability1_epic2)
        task5_us3_capability1_epic2 = self.create_system("Deploy responsive navigation menu", us_capability_task_type, org, parent=us3_capability1_epic2)
        task6_us3_capability1_epic2 = self.create_system("Monitor user feedback on navigation menu", us_capability_task_type, org, parent=us3_capability1_epic2)

        # Tasks for "As a user, I want touch-friendly controls on mobile devices, so that I can interact with the website easily"
        task1_us4_capability1_epic2 = self.create_system("Design touch-friendly UI elements", us_capability_task_type, org, parent=us4_capability1_epic2)
        task2_us4_capability1_epic2 = self.create_system("Implement touch-friendly controls", us_capability_task_type, org, parent=us4_capability1_epic2)
        task3_us4_capability1_epic2 = self.create_system("Test touch controls on mobile devices", us_capability_task_type, org, parent=us4_capability1_epic2)
        task4_us4_capability1_epic2 = self.create_system("Write documentation for touch-friendly controls", us_capability_task_type, org, parent=us4_capability1_epic2)
        task5_us4_capability1_epic2 = self.create_system("Deploy touch-friendly control updates", us_capability_task_type, org, parent=us4_capability1_epic2)
        task6_us4_capability1_epic2 = self.create_system("Monitor user feedback on touch controls", us_capability_task_type, org, parent=us4_capability1_epic2)

        # Tasks for "As a user, I want the website to load quickly on all devices, so that I can start using it without delay"
        task1_us5_capability1_epic2 = self.create_system("Optimize images for faster loading", us_capability_task_type, org, parent=us5_capability1_epic2)
        task2_us5_capability1_epic2 = self.create_system("Minify CSS and JavaScript files", us_capability_task_type, org, parent=us5_capability1_epic2)
        task3_us5_capability1_epic2 = self.create_system("Implement lazy loading for images", us_capability_task_type, org, parent=us5_capability1_epic2)
        task4_us5_capability1_epic2 = self.create_system("Use a content delivery network (CDN)", us_capability_task_type, org, parent=us5_capability1_epic2)
        task5_us5_capability1_epic2 = self.create_system("Test website loading speed on various devices", us_capability_task_type, org, parent=us5_capability1_epic2)
        task6_us5_capability1_epic2 = self.create_system("Monitor website performance and loading times", us_capability_task_type, org, parent=us5_capability1_epic2)


        # Add User Stories under Capability 2 of Epic 2 (ElasticSearch Integration)
        us1_capability2_epic2 = self.create_system("As a user, I want to find relevant results quickly, so that I can access the information I need efficiently", capability_us_type, org, parent=capability2_epic2)
        us2_capability2_epic2 = self.create_system("As a user, I want to see search suggestions as I type, so that I can find what I'm looking for more easily", capability_us_type, org, parent=capability2_epic2)
        us3_capability2_epic2 = self.create_system("As a user, I want to filter search results by categories, so that I can narrow down my search to specific types of content", capability_us_type, org, parent=capability2_epic2)
        us4_capability2_epic2 = self.create_system("As a user, I want to view my search history, so that I can easily revisit previous searches", capability_us_type, org, parent=capability2_epic2)
        us5_capability2_epic2 = self.create_system("As a user, I want to search using advanced query options, so that I can find exactly what I’m looking for", capability_us_type, org, parent=capability2_epic2)

        # Add Tasks under User Stories for Capability 2 of Epic 2 (ElasticSearch Integration)

        # Tasks for "As a user, I want to find relevant results quickly, so that I can access the information I need efficiently"
        task1_us1_capability2_epic2 = self.create_system("Integrate ElasticSearch API", us_capability_task_type, org, parent=us1_capability2_epic2)
        task2_us1_capability2_epic2 = self.create_system("Optimize search queries for performance", us_capability_task_type, org, parent=us1_capability2_epic2)
        task3_us1_capability2_epic2 = self.create_system("Index frequently searched terms", us_capability_task_type, org, parent=us1_capability2_epic2)
        task4_us1_capability2_epic2 = self.create_system("Test search performance", us_capability_task_type, org, parent=us1_capability2_epic2)
        task5_us1_capability2_epic2 = self.create_system("Write documentation for ElasticSearch integration", us_capability_task_type, org, parent=us1_capability2_epic2)
        task6_us1_capability2_epic2 = self.create_system("Deploy ElasticSearch integration", us_capability_task_type, org, parent=us1_capability2_epic2)

        # Tasks for "As a user, I want to see search suggestions as I type, so that I can find what I'm looking for more easily"
        task1_us2_capability2_epic2 = self.create_system("Implement search suggestions feature", us_capability_task_type, org, parent=us2_capability2_epic2)
        task2_us2_capability2_epic2 = self.create_system("Design UI for search suggestions", us_capability_task_type, org, parent=us2_capability2_epic2)
        task3_us2_capability2_epic2 = self.create_system("Optimize search suggestion queries", us_capability_task_type, org, parent=us2_capability2_epic2)
        task4_us2_capability2_epic2 = self.create_system("Test search suggestions functionality", us_capability_task_type, org, parent=us2_capability2_epic2)
        task5_us2_capability2_epic2 = self.create_system("Write documentation for search suggestions", us_capability_task_type, org, parent=us2_capability2_epic2)
        task6_us2_capability2_epic2 = self.create_system("Deploy search suggestions feature", us_capability_task_type, org, parent=us2_capability2_epic2)

        # Tasks for "As a user, I want to filter search results by categories, so that I can narrow down my search to specific types of content"
        task1_us3_capability2_epic2 = self.create_system("Implement category filters for search results", us_capability_task_type, org, parent=us3_capability2_epic2)
        task2_us3_capability2_epic2 = self.create_system("Design UI for category filters", us_capability_task_type, org, parent=us3_capability2_epic2)
        task3_us3_capability2_epic2 = self.create_system("Optimize filter queries", us_capability_task_type, org, parent=us3_capability2_epic2)
        task4_us3_capability2_epic2 = self.create_system("Test category filter functionality", us_capability_task_type, org, parent=us3_capability2_epic2)
        task5_us3_capability2_epic2 = self.create_system("Write documentation for category filters", us_capability_task_type, org, parent=us3_capability2_epic2)
        task6_us3_capability2_epic2 = self.create_system("Deploy category filter feature", us_capability_task_type, org, parent=us3_capability2_epic2)

        # Tasks for "As a user, I want to view my search history, so that I can easily revisit previous searches"
        task1_us4_capability2_epic2 = self.create_system("Implement search history feature", us_capability_task_type, org, parent=us4_capability2_epic2)
        task2_us4_capability2_epic2 = self.create_system("Design UI for search history", us_capability_task_type, org, parent=us4_capability2_epic2)
        task3_us4_capability2_epic2 = self.create_system("Optimize search history queries", us_capability_task_type, org, parent=us4_capability2_epic2)
        task4_us4_capability2_epic2 = self.create_system("Test search history functionality", us_capability_task_type, org, parent=us4_capability2_epic2)
        task5_us4_capability2_epic2 = self.create_system("Write documentation for search history", us_capability_task_type, org, parent=us4_capability2_epic2)
        task6_us4_capability2_epic2 = self.create_system("Deploy search history feature", us_capability_task_type, org, parent=us4_capability2_epic2)

        # Tasks for "As a user, I want to search using advanced query options, so that I can find exactly what I’m looking for"
        task1_us5_capability2_epic2 = self.create_system("Implement advanced query options for search", us_capability_task_type, org, parent=us5_capability2_epic2)
        task2_us5_capability2_epic2 = self.create_system("Design UI for advanced query options", us_capability_task_type, org, parent=us5_capability2_epic2)
        task3_us5_capability2_epic2 = self.create_system("Optimize advanced query performance", us_capability_task_type, org, parent=us5_capability2_epic2)
        task4_us5_capability2_epic2 = self.create_system("Test advanced query functionality", us_capability_task_type, org, parent=us5_capability2_epic2)
        task5_us5_capability2_epic2 = self.create_system("Write documentation for advanced queries", us_capability_task_type, org, parent=us5_capability2_epic2)
        task6_us5_capability2_epic2 = self.create_system("Deploy advanced query feature", us_capability_task_type, org, parent=us5_capability2_epic2)
