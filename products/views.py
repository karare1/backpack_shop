from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category
from django.db.models.functions import Lower

# Create your views here.


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
            # if sortkey == 'category':
            #     sortkey = 'category__name'
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
            queries1 = Q(name__icontains=query1) | Q(description__icontains=query1)
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

    context = {
        'product': product,
    }

    return render(request, 'products/individual_product.html', context)
