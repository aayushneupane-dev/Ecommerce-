from django.shortcuts import render
from .models import Order, Product


def _get_order_items(order):
    for relation in Order._meta.get_fields():
        if (
            relation.one_to_many
            and relation.auto_created
            and relation.field.remote_field.model is Order
        ):
            return getattr(order, relation.get_accessor_name()).all()

    raise AttributeError('No order-item relation is defined for Order.')


def store(request):
    products = Product.objects.all()

    context = {
        'products': products
    }

    return render(request, 'store/store.html', context)


def products(request):
    context = {}
    return render(request, 'store/products.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer

        order, created = Order.objects.get_or_create(
            customer=customer,
            complete=False
        )

        items = _get_order_items(order)

    else:
        items = []
        order = {
            'get_cart_total': 0,
            'get_cart_items': 0
        }

    context = {
        'items': items,
        'order': order
    }

    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer

        order, created = Order.objects.get_or_create(
            customer=customer,
            complete=False
        )

        items = _get_order_items(order)

    else:
        order = {
            'get_cart_total': 0,
            'get_cart_items': 0
        }
        items = []

    context = {
        'items': items,
        'order': order
    }

    return render(request, 'store/checkout.html', context)


