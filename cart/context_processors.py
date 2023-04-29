from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product


def cart_contents(request):

    cart_items = []
    subtotal = 0
    count_items = 0
    cart = request.session.get('cart', {})

    for item_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=item_id)
        subtotal += quantity * product.price
        count_items += quantity
        cart_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'product': product,
        })

    if subtotal < settings.FREE_DELIVERY_THRESHOLD:
        delivery = Decimal(3.99)
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
