from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader

from .models import Member, Membership
from typing import List

from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from .models import Member, Membership
from .forms import MemberForm


class MembershipListView(ListView):
    model = Membership
    template_name = "members/membership_list.html"


from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Member, Membership, MembershipType


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


def get_wa_link(phone, client_name, cost, date):
    import urllib.parse

    # 1. Limpiar el teléfono (dejar solo dígitos, asegurando que tenga código de país, ej: 593...)
    telefono_limpio = "593" + "".join(filter(str.isdigit, str(phone)))

    # 2. Redactar el mensaje del recordatorio
    mensaje = (
        f"Hola *{client_name}*, te recordamos que tienes un pago pendiente "
        f"por *$ {cost}* con vencimiento el *{date}*.\n\nSi ya realizaste el "
        "pago, por favor ignora este mensaje. ¡Gracias!"
    )

    # 3. Codificar el texto para la URL (maneja espacios, tildes y saltos de línea)
    mensaje_encoded = urllib.parse.quote(mensaje)

    return f"https://wa.me/{telefono_limpio}?text={mensaje_encoded}"


def index(request):
    memberships = Membership.objects.select_related("member", "membership_type").all()
    memberships: List[Membership] = list(memberships)
    for m in memberships:
        m.wa_link = get_wa_link(
            m.member.phone, m.member.name, m.membership_type.price, m.expires_at
        )

    template = loader.get_template("members/index.html")
    context = {"memberships": memberships}
    return HttpResponse(template.render(context, request))


# def detail(request, member_id):
#     return HttpResponse("You're looking at member %s." % member_id)
