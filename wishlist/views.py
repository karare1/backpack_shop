from django.shortcuts import render, get_object_or_404, redirect, reverse, HttpResponseRedirect
from django.conf import settings
from django.contrib import messages
from profiles.models import UserProfile
from products.models import Product
from wishlist.models import Wishlist


def wishlist_view(request):
    if not request.user.is_authenticated:
        messages.error(request,
                       'Please log in to add this product into your Wishlist.')
        return redirect(reverse('account_login'))

    user = get_object_or_404(UserProfile, user=request.user)
    wishlist = Wishlist.objects.filter(profile=user)

    template = 'wishlist/my_wishlist.html'

    context = {
        'wishlist': wishlist,
    }

    return render(request, template, context)


def wishlist_on(request, product_id):
    if not request.user.is_authenticated:
        messages.error(request,
                       'Please log in to add this product into your Wishlist.')
        return redirect(reverse('account_login'))

    user = get_object_or_404(UserProfile, user=request.user)
    product = get_object_or_404(Product, pk=product_id)

    existing = Wishlist.objects.filter(product=product,
                                       profile=user).exists()
    if existing:
        messages.info(request, f'{product.name} is already in your Wishlist!')
        return redirect(reverse('individual_product', args=[product.id]))
    else:
        wishlist_item = Wishlist.objects.create(profile=user,
                                                product=product)
    messages.info(request,
                     f'{product.name} has been added to your Wishlist!')

    return redirect(reverse('individual_product', args=[product.id]))


def wishlist_off(request, product_id):
    if not request.user.is_authenticated:
        messages.error(request,
                       'Please log in to add an item to your Wishlist.')
        return redirect(reverse('account_login'))

    user = get_object_or_404(UserProfile, user=request.user)
    product = get_object_or_404(Product, pk=product_id)
    Wishlist.objects.filter(product=product,
                            profile=user).delete()
    messages.info(request,
                  f'{product.name} has been removed from your Wishlist!')

    return HttpResponseRedirect(reverse('wishlist_view'))
