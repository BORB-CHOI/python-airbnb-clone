from django.core.management.base import BaseCommand
from users.models import User

NAME = "superuser"


class Command(BaseCommand):

    help = f"This command create superuser"

    def handle(self, *args, **options):
        admin = User.objects.get_or_none(username="ebadmin")

        if not admin:
            User.objects.create_superuser("ebadmin", "ebadmin@admin.com", "ebadmin")
            self.stdout.write(self.style.SUCCESS(f"Superuser Created"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Superuser Exists"))
