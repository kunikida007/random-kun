from email.policy import default
import uuid as uuid_lib

from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.db import models

from common.models import TimeStampedModel


User = get_user_model()


class Match(TimeStampedModel):
    id = models.UUIDField(
        verbose_name="試合ID",
        default=uuid_lib.uuid4,
        primary_key=True,
        editable=False,
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    match_name = models.CharField(max_length=10)
    number_of_court = models.IntegerField()
    match_list = ArrayField(
        ArrayField(ArrayField(models.CharField(max_length=10, null=True), null=True), default=list),
        default=list,
    )

    def __str__(self):
        return self.match_name


# class MemberQueryManager(models.Manager):
#     def members_in_match(self, *args, **kwargs):
#         return (
#             self.get_queryset()
#             .filter(id, *args, **kwargs)
#             .values_list("member_name", flat=True)
#         )


class Member(TimeStampedModel):
    member_name = models.CharField(max_length=10)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    court_number = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.member_name}-{self.match.match_name}"
