from django.db import models
import uuid
from datetime import datetime, timezone


class Gym(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField()


class Member(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField()
    created_at = models.DateTimeField()


class Membership(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)

    start_date = models.DateField()
    due_date = models.DateField()
    expires_at = models.DateTimeField()
    cost = models.FloatField(default=60)

    created_at = models.DateTimeField()
