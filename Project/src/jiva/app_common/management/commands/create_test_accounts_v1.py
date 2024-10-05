from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app_organization.mod_organization.models_organization import *
from app_memberprofilerole.mod_profile.models_profile import *
from app_memberprofilerole.mod_member.models_member import *

import random
test_user_accounts_count = 150
class Command(BaseCommand):
    help = 'Generate test user accounts with roles and organization membership'

    def handle(self, *args, **kwargs):
        first_names = ["John", "Jane", "Michael", "Michelle", "Chris", "Christina", "David", "Danielle", "James", "Jennifer"]
        last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor"]
        roles = ["Admin", "Editor", "Viewer", "Manager", "Contributor",  "Scrum Master", "Product Owner", "Developer", "Designer", "UI/UX", "System Architect", 
                 "Enterprise Architect", "Business Owner", "Program Manager", "Project Manager", "Program Manager", "Portfolio Manager",
                 "BlogAdmin", "BlogWriter", "BlogEditor", "BlogViewer",
                 
                 ]

        # Create the organization
        organization = Organization.objects.create(name="ABC Organization")

        # Create the "Team Member" role
        team_member_role = Role.objects.create(name="Team Member", org=organization)

        # Create other roles for the organization
        role_objects = [team_member_role]
        for role in roles:
            role_obj = Role.objects.create(name=role, org=organization)
            role_objects.append(role_obj)

        user_count = 0
        total_users = test_user_accounts_count
        team_member_count = int(total_users * 0.9)  # 90% should be "Team Member"

        for first_name in first_names:
            for last_name in last_names:
                for i in range(1, 11):
                    if user_count >= total_users:
                        break
                    username = f"{first_name.lower()}.{last_name.lower()}{i}"
                    email = f"{first_name.lower()}.{last_name.lower()}{i}@example.com"
                    password = 'password123'  # Default password for all fake users
                    user = User.objects.create_user(username=username, email=email, password=password)
                    
                    if user_count < team_member_count:
                        role = team_member_role
                    else:
                        role = random.choice(role_objects)
                    member = Member.objects.create(user=user, org=organization)
                    MemberOrganizationRole.objects.create(member = member, org=organization, role=role)
                    user_count += 1

        self.stdout.write(self.style.SUCCESS('Successfully created test users with roles and organization membership'))
