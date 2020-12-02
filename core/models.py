from django.db import models
import uuid

CATEGORY_CHOICES = (
    ('A', 'Art'),
    ('F', 'Fun'),
    ('H', 'Home'),
    ('KB', 'Kitchen & Bar'),
    ('G', 'Garden'),
    ('T', 'Tech'),
)


class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)
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

    @property
    def cart_total(self):
        total = sum([item.get_total() for item in self.items])
        return total
