from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from core import models as core_models


class Review(core_models.TimeStampedModel):

    """Review Model Definition"""

    review = models.TextField()
    accuracy = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    communication = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    cleanliness = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    location = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    check_in = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    value = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    user = models.ForeignKey(
        "users.User", related_name="reviews", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        "rooms.Room", related_name="reviews", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.review} - {self.room}"
        #                        self.room.name

    # model에 함수를 쓰기위한 기준은
    # 1. 그게 계산이 필요한 뭔가라면 2. 그게 여기저기 반복되어질 경우(어드민 패널에서만 쓰이지 않고 프론트에서도 사용되는 경우)
    def rating_average(self):
        avg = (
            self.accuracy
            + self.communication
            + self.cleanliness
            + self.location
            + self.check_in
            + self.value
        ) / 6
        return round(avg, 2)

    rating_average.short_description = "AVG."

    class Meta:
        ordering = ("-created",)
