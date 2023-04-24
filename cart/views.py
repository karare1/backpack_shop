from django.shortcuts import render, redirect

# Create your views here.


def shop_cart(request):
    """ A view that renders the cart contents page """

    return render(request, 'cart/cart.html')


def add_items(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})

    if item_id in list(cart.keys()):
        cart[item_id] += quantity
    else:
        cart[item_id] = quantity

    request.session['cart'] = cart
    # print(request.session['cart'])
    return redirect(redirect_url)