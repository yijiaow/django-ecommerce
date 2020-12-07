from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView
from django.http import HttpResponse, JsonResponse

from .models import Product, OrderItem, Order


class StoreView(ListView):
    model = Product
    template_name = 'store.html'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product.html'

    def post(self, *args, **kwargs):
        form = ProductQuantityForm(self.request.POST)


class CartView(DetailView):
    model = OrderItem
    template_name = 'cart.html'


class CheckoutView(View):
    pass


def store(request):
    context = {}
    return render(request, 'store.html', context)
