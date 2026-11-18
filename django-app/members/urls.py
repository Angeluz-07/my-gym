from django.urls import path

from members.views.index import index

from members.views.members import MemberCreateView, MemberListView

urlpatterns = [
    path("", index, name="index"),
    path("list/", MemberListView.as_view(), name="member_list"),
    path("add/", MemberCreateView.as_view(), name="member_add"),
    # path("<str:member_id>/", views.detail, name="detail"),
]
