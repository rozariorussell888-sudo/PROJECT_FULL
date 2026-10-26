import re
from django import template

register = template.Library()


@register.filter
def whatsapp_phone(value):
    if not value:
        return ""

    phone = re.sub(r"\D", "", str(value))

    if phone.startswith("00"):
        phone = phone[2:]

    if phone.startswith("880"):
        return phone

    if phone.startswith("0") and len(phone) == 11:
        return "88" + phone

    if phone.startswith("1") and len(phone) == 10:
        return "880" + phone

    return phone