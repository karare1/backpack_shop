from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib import messages

from products.models import Product

# Create your views here.


def shop_cart(request):
    """ A view that renders the cart contents page """

    return render(request, 'cart/cart.html')


def add_items(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    product = Product.objects.get(pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})

    if item_id in list(cart.keys()):
        cart[item_id] += quantity
    else:
        cart[item_id] = quantity
        messages.success(request, f'Added {product.name} to your bag')

    request.session['cart'] = cart
    # print(request.session['cart'])
    return redirect(redirect_url)


def amend_item(request, item_id):
    """Adjust the quantity of the specified product to the specified amount"""

    quantity = int(request.POST.get('quantity'))
    # size = None
    # if 'product_size' in request.POST:
    #     size = request.POST['product_size']
    cart = request.session.get('cart', {})

    # if size:
    #     if quantity > 0:
    #         bag[item_id]['items_by_size'][size] = quantity
    #     else:
    #         del bag[item_id]['items_by_size'][size]
    #         if not bag[item_id]['items_by_size']:
    #             bag.pop(item_id)
    # else:

    if quantity > 0:
        cart[item_id] = quantity
    else:
        cart.pop(item_id)

    request.session['cart'] = cart
    return redirect(reverse('shop_cart'))


def remove_item(request, item_id):
    """Remove the item from the shopping bag"""

    try:
        # size = None
        # if 'product_size' in request.POST:
        #     size = request.POST['product_size']
        cart = request.session.get('cart', {})

        # if size:
        #     del bag[item_id]['items_by_size'][size]
        #     if not bag[item_id]['items_by_size']:
        #         bag.pop(item_id)
        # else:
        cart.pop(item_id)

        request.session['cart'] = cart
        return HttpResponse(status=200)

    except Exception as e:
        return HttpResponse(status=500)
