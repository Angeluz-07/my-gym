from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from members.models import Member, Membership, MembershipType
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader

from members.models import Member, Membership
from typing import List

from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from members.models import Member, Membership
from members.forms import MemberForm
from django.views.generic.edit import UpdateView


class MemberUpdateView(UpdateView):
    model = Member
    form_class = MemberForm
    template_name = "members/member_form_upd.html"  # ¡Reutilizamos el mismo formulario!
    success_url = reverse_lazy("member_list")


class MemberListView(ListView):
    model = Member
    template_name = "members/member_list.html"
    context_object_name = "members"


class MemberCreateView(CreateView):
    model = Member
    # Campos básicos que llenará el admin en el formulario de la persona
    fields = ["name", "phone", "email"]
    template_name = "members/member_form.html"
    success_url = reverse_lazy("index")  # O la URL de tu lista de miembros

    def get_context_data(self, **kwargs):
        """Inyecta los tipos de membresía disponibles para mostrarlos en el HTML"""
        context = super().get_context_data(**kwargs)
        context["membership_types"] = MembershipType.objects.all()
        return context

    def form_valid(self, form):
        # transaction.atomic asegura que si algo falla, no se guarde a medias
        with transaction.atomic():
            # 1. Guardamos primero al miembro
            self.object = form.save()

            # 2. Capturamos el tipo de membresía que el admin seleccionó en el HTML
            membership_type_id = self.request.POST.get("membership_type_id")

            if membership_type_id:
                membership_type = MembershipType.objects.get(id=membership_type_id)

                # 3. Creamos la membresía asociada automáticamente
                # (Las fechas y costos usarán los valores por defecto que definiste en el modelo)
                Membership.objects.create(
                    member=self.object,
                    membership_type=membership_type,
                )

        return super().form_valid(form)
