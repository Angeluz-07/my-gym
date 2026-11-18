from django.db import models
import uuid
from datetime import datetime, timezone

from django.utils import timezone


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
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"


class MembershipType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    price = models.FloatField(default=60)


from datetime import date
from dateutil.relativedelta import relativedelta


def get_default_start_date():
    """Retorna la fecha actual del registro"""
    return date.today()


class Membership(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    membership_type = models.ForeignKey(
        MembershipType, on_delete=models.CASCADE, related_name="memberships"
    )
    member = models.OneToOneField(
        Member, on_delete=models.CASCADE, related_name="membership"
    )
    start_date = models.DateField(default=get_default_start_date)
    created_at = models.DateTimeField(default=timezone.now)

    @property
    def last_month(self) -> str:
        MESES = {
            1: "enero",
            2: "febrero",
            3: "marzo",
            4: "abril",
            5: "mayo",
            6: "junio",
            7: "julio",
            8: "agosto",
            9: "septiembre",
            10: "octubre",
            11: "noviembre",
            12: "diciembre",
        }

        from datetime import datetime

        return MESES[self.start_date.month].capitalize() + " / " + str(self.start_date.year)[-2:]

    @property
    def due_date(self) -> date:
        next_month = self.start_date + relativedelta(months=1)
        return date(next_month.year, next_month.month, 1)

    @property
    def expires_at(self) -> date:
        grace_period = relativedelta(days=3)
        return self.due_date + grace_period

    @property
    def is_up_to_date(self) -> dict:
        from datetime import date

        today = date.today()
        return today <= self.expires_at
