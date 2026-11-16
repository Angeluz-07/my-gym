from django.urls import path

from . import views

from .views import MemberCreateView

urlpatterns = [
    path("", views.index, name="index"),
    path('add/', MemberCreateView.as_view(), name='member_add'),
    #path("<str:member_id>/", views.detail, name="detail"),
]