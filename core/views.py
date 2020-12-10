from django.shortcuts import reverse
from django.contrib import messages
from django.views.generic import View, ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponseForbidden

from .models import Product, OrderItem
from .forms import ProductQuantityForm


class StoreView(ListView):
    model = Product
    template_name = 'store.html'


class ProductDisplay(DetailView):
    model = Product
    template_name = 'product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProductQuantityForm()
        return context


class ProductQuantity(SingleObjectMixin, FormView):
    model = Product
    template_name = 'product.html'
    form_class = ProductQuantityForm

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        quantity = form.cleaned_data.get('quantity')
        cart = self.request.session.get('shopping_cart')
        order_item, created = OrderItem.objects.get_or_create(item=self.object)
        if not cart:
            cart = self.request.session['shopping_cart'] = {}

        if str(order_item.item.id) in cart.keys():
            cart[str(order_item.item.id)] = cart[str(
                order_item.item.id)] + quantity
            order_item.quantity += quantity
            order_item.save()
            messages.info(self.request, 'Item quantity updated')
        else:
            cart[str(order_item.item.id)] = quantity
            order_item.quantity = quantity
            order_item.save()
            cart[order_item.item.id] = quantity
            messages.info(self.request, 'Item added to cart')

        self.request.session['shopping_cart'] = cart
        # Gotcha: Session is NOT modified, because this alters
        # request.session['shopping_cart'] instead of request.session.
        # self.request.session['shopping_cart'][str(order_item.item.id)]
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('core:product', kwargs={'slug': self.object.slug})


class ProductDetailView(View):
    def get(self, request, *args, **kwargs):
        view = ProductDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ProductQuantity.as_view()
        return view(request, *args, **kwargs)

class CartView(DetailView):
    model = OrderItem
    template_name = 'cart.html'


class CheckoutView(View):
    pass


def store(request):
    context = {}
    return render(request, 'store.html', context)
