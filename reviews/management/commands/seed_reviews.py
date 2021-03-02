import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from reviews import models as review_models
from users import models as user_models
from rooms import models as room_models

NAME = "reviews"


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
        users = user_models.User.objects.all()
        rooms = room_models.Room.objects.all()

        seeder.add_entity(
            review_models.Review,
            number,
            {
                "accuracy": lambda x: random.randint(0, 5),
                "communitication": lambda x: random.randint(0, 5),
                "cleanliness": lambda x: random.randint(0, 5),
                "location": lambda x: random.randint(0, 5),
                "check_in": lambda x: random.randint(0, 5),
                "value": lambda x: random.randint(0, 5),
                "user": lambda x: random.choice(users),
                "room": lambda x: random.choice(rooms),
            },
        )
        seeder.execute()

        self.stdout.write(self.style.SUCCESS(f"{number} {NAME} created"))
