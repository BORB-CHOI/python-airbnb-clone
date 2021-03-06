from django.core.management.base import BaseCommand
from django_seed import Seed
from users.models import User

NAME = "users"


class Command(BaseCommand):

    help = f"This command creates many {NAME}"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=1,  # 비어있을 시에 1
            type=int,  # 입력값을 int로 변환
            help=(f"How many {NAME} do you want to create?"),
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()

        seeder.add_entity(User, number, {"is_staff": False, "is_superuser": False})
        seeder.execute()

        self.stdout.write(self.style.SUCCESS(f"{number} {NAME} created"))
