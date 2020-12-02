from django.views.generic import View, ListView, DetailView

from .models import Product, OrderItem, Order


class StoreView(ListView):
    model = Product
    template_name = 'store.html'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product.html'


class CartView(DetailView):
    model = OrderItem
    template_name = 'cart.html'


class CheckoutView(View):
    pass
