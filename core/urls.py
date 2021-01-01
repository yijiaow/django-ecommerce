from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('payment/', views.PaymentView.as_view(), name='payment'),
    path('payment/create-payment-intent', views.create_payment),
]
