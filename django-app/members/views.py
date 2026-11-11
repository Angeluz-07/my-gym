from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader

from .models import Member
from typing import List


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
    members = Member.objects.select_related("membership").all()
    members: List[Member] = list(members)
    for m in members:
        m.wa_link = get_wa_link(
            m.phone, m.name, m.membership.cost, m.membership.expires_at
        )
    template = loader.get_template("members/index.html")
    context = {"members": members}
    return HttpResponse(template.render(context, request))


def detail(request, member_id):
    return HttpResponse("You're looking at member %s." % member_id)
