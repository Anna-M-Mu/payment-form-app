from django.urls import path
from .views import buy_item, item_detail, create_order, save_order, order_detail, pay_for_order, create_payment_intent, payment_page

urlpatterns = [
    path('buy/<int:id>/', buy_item, name='buy_item'),
    path('item/<int:id>/', item_detail, name='item_detail'),
    path('createorder/', create_order, name='create_order'),
    path('saveorder/', save_order, name='save_order'),
    path('order/<int:id>/', order_detail, name='order_detail'),
    path('payfororder/<int:id>/', pay_for_order, name='pay_for_order'),
    path('paymentintent/<int:id>/', create_payment_intent, name='create_payment_intent'),
    path('paymentpage/', payment_page, name='payment_page'),
]
