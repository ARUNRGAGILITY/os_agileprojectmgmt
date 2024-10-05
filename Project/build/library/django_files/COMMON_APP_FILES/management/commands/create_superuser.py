# your_app/management/commands/create_superuser.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = 'Creates a superuser non-interactively using environment variables'

    def handle(self, *args, **options):
        User = get_user_model()
        username = 'admin'
        email = 'admin@example.com'
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        if password is None:
            self.stdout.write(self.style.ERROR('Please set the DJANGO_SUPERUSER_PASSWORD environment variable.'))
            return

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            self.stdout.write(self.style.SUCCESS('Successfully created a new superuser'))
        else:
            self.stdout.write(self.style.WARNING('Superuser already exists'))
