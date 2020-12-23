from django.shortcuts import reverse
from django.contrib import messages
from django.views.generic import View, ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponseForbidden

from .models import Product, OrderItem
from .forms import ProductQuantityForm, BillingAddressForm


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
    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        context = {
            'cart': cart,
            'shipping_form': CheckoutForm()
        }
        if request.user.is_authenticated:
            print('CURRENT USER: ', request.user.email, request.user.first_name)
            shipping_address_qs = Address.objects.filter(
                user=request.user, address_type='S', default=True)
            if shipping_address_qs.exists():
                context.update(
                    {'default_shipping_address': shipping_address_qs[0]})
        return render(request, 'checkout.html', context)

    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        shipping_form = CheckoutForm(request.POST)
        if shipping_form.is_valid():
            cd = shipping_form.cleaned_data
            shipping_address = shipping_form.save(commit=False)
            shipping_address.user = request.user
            if (cd.get('set_default_shipping')):
                shipping_address.default = True
            shipping_address.save()

            # Create order
            order = Order.objects.create(
                email=request.user.email, shipping_address=shipping_address)
            for item in cart:
                OrderItem.objects.create(
                    order=order, item=item['product'], quantity=item['quantity'])
            cart.clear()

        # Redirect to payment
        return redirect('core:payment')


def store(request):
    context = {}
    return render(request, 'store.html', context)


class PaymentView(View):
    def get(self, request, *args, **kwargs):
        order_id = request.session.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        context = {'billing_form': BillingAddressForm()}
        if order.shipping_address:
            context['shipping_address'] = order.shipping_address
        return render(request, 'payment.html', context)
