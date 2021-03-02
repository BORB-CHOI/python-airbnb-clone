import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from django.contrib.admin.utils import flatten
from lists import models as list_models
from users import models as user_models
from rooms import models as room_models

NAME = "lists"


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
        # rooms = room_models.Room.objects.all()[4:10]
        # 4에서 10 사이의 list 값만

        seeder.add_entity(
            list_models.List,
            number,
            {
                "user": lambda x: random.choice(users),
            },
        )
        created = seeder.execute()
        created_clean = flatten(list(created.values()))

        for pk in created_clean:
            a_list = list_models.List.objects.get(pk=pk)
            to_add = rooms[random.randint(0, 5) : random.randint(6, 30)]
            a_list.rooms.add(*to_add)

        self.stdout.write(self.style.SUCCESS(f"{number} {NAME} created"))
