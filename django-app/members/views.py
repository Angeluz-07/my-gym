from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader

from .models import Member

def index(request):
    members = Member.objects.all()
    template = loader.get_template("members/index.html")
    context = {"members": members}
    return HttpResponse(template.render(context, request))

def detail(request, member_id):
    return HttpResponse("You're looking at member %s." % member_id)