import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from rooms import models as room_models
from users import models as user_models

NAME = "rooms"


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
        room_types = room_models.RoomType.objects.all()

        seeder.add_entity(
            room_models.Room,
            number,
            {
                "name": lambda x: seeder.faker.address(),
                "host": lambda x: random.choice(users),
                "room_type": lambda x: random.choice(room_types),
                "price": lambda x: random.randint(1, 300),
                "guests": lambda x: random.randint(1, 20),
                "beds": lambda x: random.randint(1, 5),
                "bedrooms": lambda x: random.randint(1, 5),
                "baths": lambda x: random.randint(1, 5),
            },
        )
        created = seeder.execute()
        created_clean = flatten(list(created.values()))

        amenities = room_models.Amenity.objects.all()
        facilities = room_models.Facility.objects.all()
        rules = room_models.HouseRule.objects.all()

        for pk in created_clean:
            a_room = room_models.Room.objects.get(pk=pk)

            # Seed Photo
            for i in range(3, random.randint(10, 30)):
                room_models.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    room=a_room,
                    file=f"room_photos/{random.randint(1, 31)}.webp",
                )

            # Seed Amenities
            for a in amenities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    a_room.amenities.add(a)

            # Seed Facilities
            for f in facilities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    a_room.facilities.add(f)

            # Seed House Rules
            for r in rules:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    a_room.house_rules.add(r)

        self.stdout.write(self.style.SUCCESS(f"{number} {NAME} created"))
