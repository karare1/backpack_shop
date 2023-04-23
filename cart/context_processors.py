from decimal import Decimal
from django.conf import settings


def cart_contents(request):

    cart_items = []
    subtotal = 0
    count_items = 0

    if subtotal < settings.FREE_DELIVERY_THRESHOLD:
        delivery = subtotal * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_confirmed = settings.FREE_DELIVERY_THRESHOLD - subtotal
    else:
        delivery = 0
        free_delivery_confirmed = 0

    final_total = delivery + subtotal

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'count_items': count_items,
        'delivery': delivery,
        'free_delivery_confirmed': free_delivery_confirmed,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'final_total': final_total,
    }

    return context
