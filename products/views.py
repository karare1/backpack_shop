from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from .forms import ReviewForm
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Product, Category, Review
from django.db.models.functions import Lower
from profiles.models import UserProfile
from django.core.exceptions import PermissionDenied

from .forms import ProductForm


def all_products(request):
    """ A view to show all products, including sorting and search queries """
    products = Product.objects.all()
    query1 = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

    if request.GET:
        if 'query' in request.GET:
            query1 = request.GET['query']
            if not query1:
                messages.error(request, "Please enter search criteria!")
                return redirect(reverse('products'))
            queries1 = Q(name__icontains=query1) | Q(
                description__icontains=query1)
            products = products.filter(queries1)

    sorting_by = f'{sort}_{direction}'

    context = {
        'products': products,
        'query_expression': query1,
        'actual_categories': categories,
        'sorting_by': sorting_by,
    }

    return render(request, 'products/products.html', context)


def individual_product(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)
    reviews = Review.objects.filter(product_id=product.id, status=True)
    context = {
        'product': product,
        'reviews': reviews,
    }

    return render(request, 'products/individual_product.html', context)


@login_required
def add_product(request):
    """ Add a product to the store """

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.info(request, 'Successfully added product!')
            return redirect(reverse('individual_product', args=[product.id]))
        else:
            messages.error(
                request, 'Failed to add product. \
                    Please ensure the form is valid.')
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.info(request, 'Successfully updated product!')
            return redirect(reverse('individual_product', args=[product.id]))
        else:
            messages.error(
                request, 'Failed to update product.\
                    Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.info(request, 'Product deleted!')
    return redirect(reverse('products'))


def reviews_views(request, product_id):
    """ A view to show all available reviews for current product """
    product = get_object_or_404(Product, pk=product_id)
    review = Review.objects.create(
        product=product, user=request.user, rating=rating, review=review)
    template = 'products/individual_product.html'

    context = {
        'reviews': reviews,
        'product': product,
    }

    return render(request, template, context)


def submit_review(request, product_id):
    """
    Renders a form to allow users to add a review and provide feedback
    to user actions via toasts
    """
    if not request.user.is_authenticated:
        messages.error(request,
                       'Sorry, you need to be logged in to add a review.')
        return redirect(reverse('account_login'))

    user = UserProfile.objects.get(user=request.user)
    product = Product.objects.get(id=product_id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        print('Form Errors:', form.errors)

        if 'rating' in request.POST and form.is_valid():
            user = request.user
            product = get_object_or_404(Product, pk=product_id)
            existing = Review.objects.filter(
                product=product, user=user).exists()
            if existing:
                messages.error(
                    request, f'You have already reviewed {product.name}!')
                return redirect(
                    reverse('individual_product', args=[product.id]))

            rating = form.save()
            review = form.save()
            review.product = product
            review.user = request.user
            review.save()
            messages.info(request, "New product review added.")
            return redirect(reverse('individual_product', args=[product.id]))
        else:
            messages.error(request, "Please rate the product.")
            return redirect(reverse('individual_product', args=[product.id]))

    else:
        form = ReviewForm()

    template = 'products/individual_product.html'

    context = {
        'form': form,
        'product': product,
        'review': review,
        'rating': rating,
    }

    return render(request, template, context)
