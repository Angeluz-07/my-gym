from django.contrib import admin
from .models import Member
from .models import Gym
from .models import Membership

# Register your models here.
admin.site.register(Member)
admin.site.register(Gym)

admin.site.register(Membership)