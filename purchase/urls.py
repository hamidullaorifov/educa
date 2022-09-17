from django.urls import path
from . import views


urlpatterns = [
    path('checkout/<int:pk>',views.checkout,name='checkout'),
    path('create-payment-intent/<int:pk>',views.create_payment_intent,name='create-payment-intent'),
    path('confirm-payment-intent/',views.confirm_payment_intent,name='confirm-payment-intent'),
    path('create-checkout-session/<int:pk>/',views.create_checkout_session,name='create-checkout-session'),
]
