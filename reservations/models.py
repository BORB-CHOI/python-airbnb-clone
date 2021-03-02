from django.db import models
from django.utils import timezone

# python utils과 다른 점 : 어플리케이션 서버의 시간대를 알 수가 있음 그리고 그걸 사용자의 시간대로 변환해줌
from core import models as core_models


class Reservation(core_models.TimeStampedModel):

    """ Rsservation Model Definition """

    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELED = "canceled"

    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_CANCELED, "Canceled"),
    )

    status = models.CharField(
        max_length=12, choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    check_in = models.DateField()
    check_out = models.DateField()
    guest = models.ForeignKey(
        "users.User", related_name="reservations", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        "rooms.Room", related_name="reservations", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.room} = {self.check_in}"

    def in_progress(self):
        now = timezone.now().date()
        return now >= self.check_in and now <= self.check_out

    in_progress.boolean = True

    def in_finished(self):
        now = timezone.now().date()
        return now > self.check_out

    in_finished.boolean = True