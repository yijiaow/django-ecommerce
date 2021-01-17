from django.db import models
from django.urls import reverse
import uuid


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('core:store_by_category', kwargs={'category_slug': self.slug})


class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    category = models.ForeignKey(
        Category, related_name='products', on_delete=models.SET_NULL, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Order(models.Model):
    transaction_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return f'Order #{self.transaction_id}'

    def get_total(self):
        return sum(item.get_item_cost() for item in self.order_items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name='order_items', on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} of {self.item.name}'

    def get_item_cost(self):
        return self.item.price * self.quantity

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_KEY)
        if not cart:
            cart = self.session[settings.CART_SESSION_KEY] = {}
        self.cart = cart

    def __iter__(self):
        ids = self.cart.keys()
        products = Product.objects.filter(id__in=ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['total_price'] = Decimal(
                item['product'].price) * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, item, quantity=1, override=False):
        product_id = str(item.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': quantity}
        elif override:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove(self, item):
        product_id = str(item.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        del self.session[settings.CART_SESSION_KEY]
        self.save()

    def save(self):
        self.session.modiefied = True

    def get_total_price(self):
        return sum(Decimal(item['total_price']) for item in self.cart.values())
