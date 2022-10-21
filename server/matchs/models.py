from email.policy import default
import uuid as uuid_lib

from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.db import models

from common.models import TimeStampedModel


User = get_user_model()


class Match(TimeStampedModel):
    class MatchType(models.TextChoices):
        SAME = "1", "同時進行"
        FIRST = "2", "先取"

    id = models.UUIDField(
        verbose_name="試合ID",
        default=uuid_lib.uuid4,
        primary_key=True,
        editable=False,
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    match_name = models.CharField(max_length=10)
    number_of_court = models.IntegerField()
    match_list = ArrayField(
        ArrayField(
            ArrayField(models.CharField(max_length=10, null=True), null=True),
            default=list,
        ),
        default=list,
    )
    type = models.CharField(
        verbose_name="試合の種類",
        max_length=15,
        choices=MatchType.choices,
        default=MatchType.SAME,
    )
    # is_active = models.BooleanField(default)

    def __str__(self):
        return self.match_name


class Member(TimeStampedModel):
    member_name = models.CharField(max_length=10)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    court_number = models.IntegerField(default=0)
    goals_score = models.IntegerField(blank=True, null=True)
    match_count = models.IntegerField(default=0)
    goals_score_rate = models.IntegerField(default=0)
    win = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.member_name}-{self.match.match_name}"
