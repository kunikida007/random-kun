from django.contrib.auth import get_user_model
from django.db import models

from common.models import TimeStampedModel

User = get_user_model()


class Profile(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    introduction = models.TextField(max_length=200, null=True, blank=True)
    career = models.IntegerField()


class Good(TimeStampedModel):
    doing = models.ForeignKey(Profile, related_name="doing", on_delete=models.CASCADE)
    done = models.ForeignKey(Profile, related_name="done", on_delete=models.CASCADE)
