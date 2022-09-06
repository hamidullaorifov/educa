from django.urls import path
from . import views


urlpatterns = [
    path('checkout/',views.checkout,name='checkout'),
    path('create-payment-intent/',views.create_payment_intent,name='create-payment-intent'),
    path('create-checkout-session/<int:pk>/',views.create_checkout_session,name='create-checkout-session'),
]
