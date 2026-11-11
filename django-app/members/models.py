from django.db import models
import uuid
from datetime import datetime, timezone


class Gym(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField()

    def __str__(self):
        return f"{self.name}"


class Member(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField()
    created_at = models.DateTimeField()

    def __str__(self):
        return f"{self.name}"


class Membership(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    member = models.OneToOneField(
        Member, on_delete=models.CASCADE, related_name="membership"
    )
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)

    start_date = models.DateField()
    due_date = models.DateField()
    expires_at = models.DateField()
    cost = models.FloatField(default=60)

    created_at = models.DateTimeField()

    @property
    def is_up_to_date(self) -> dict:
        from datetime import date
        today = date.today()
        return today <= self.expires_at