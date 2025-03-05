import os
import stripe
import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_protect
from .models import Item, Order, Tax, Discount

stripe.api_key = os.getenv('STRIPE_SECRET_KEY', settings.STRIPE_SECRET_KEY)

def buy_item(request, id):
    item = get_object_or_404(Item, id=id)

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': item.currency,
                'product_data': {'name': item.name},
                'unit_amount': item.price,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://localhost:8000/success',
        cancel_url='http://localhost:8000/cancel',
    )

    return JsonResponse({'session_id': session.id})

def item_detail(request, id):
    item = get_object_or_404(Item, id=id)
    return render(request, 'orderpayment/item_detail.html', {
        'item': item,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY 
    })
    
def order_detail(request, id):
    order = get_object_or_404(Order, id=id)
    return render(request, 'orderpayment/order_detail.html', {
        'order': order,
        'currency': order.items.first().currency,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY 
    })

def pay_for_order(request, id):
    order = get_object_or_404(Order, id=id)
    
    def create_stripe_tax(tax):
        if not tax.stripe_tax_id:
            stripe_tax = stripe.TaxRate.create(
                display_name=tax.name,
                percentage=tax.percentage,
                inclusive=False
            )
            tax.stripe_tax_id = stripe_tax.id
            tax.save() 
        return tax.stripe_tax_id

    def create_stripe_discount(discount):
        if not discount.stripe_coupon_id:  
            stripe_coupon = stripe.Coupon.create(
                percent_off=discount.percent_off, 
                duration="once"
            )
            discount.stripe_coupon_id = stripe_coupon.id
            discount.save()
        return discount.stripe_coupon_id

    discounts = []
    if order.discount:
        discounts.append({
            'coupon': create_stripe_discount(order.discount)
        })

    tax_rates = []
    if order.tax:
        tax_rates.append(create_stripe_tax(order.tax))
        
    line_items=[
        {
            'price_data': {
                'currency': order.items.first().currency,
                'product_data': {'name': f"Order ID: {order.id}"},
                'unit_amount': order.total_price,
            },
            'quantity': 1,
            'tax_rates': tax_rates,
        }
    ]
        
    metadata={
            'order_id': order.id,
            'total_price': order.total_price,
            'item_ids': ', '.join(str(item.id) for item in order.items.all()),
            'discount': str(order.discount) if order.discount else "0",
            'tax': str(order.tax) if order.tax else "0"
    }

    
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        metadata=metadata,
        discounts=discounts,
        success_url='http://localhost:8000/success',
        cancel_url='http://localhost:8000/cancel',
    )
    
    return JsonResponse({'session_id': session.id})

def create_order(request):
    items = Item.objects.all()
    return render(request, "orderpayment/create_order.html", {"items": items})
    
@csrf_protect
def save_order(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body) 
            item_ids = data.get("items", []) 
            discount = Discount.objects.order_by("?").first() 
            tax = Tax.objects.order_by("?").first() 

            if not item_ids:
                return JsonResponse({"error": "No items selected"}, status=400)

            order = Order.objects.create()
            order.items.set(Item.objects.filter(id__in=item_ids)) 
            order.discount = discount 
            order.tax = tax 
            order.save() 
            order.update_total_price()

            return JsonResponse({"order_id": order.id}) 

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)

def create_payment_intent(request, id):
    order = get_object_or_404(Order, id=id) 
    order_currency = order.items.first().currency
    total_price = order.total_price 

    tax_amount = order.get_tax_amount()  
    discount_amount = order.get_discount_amount()

    final_amount = total_price + tax_amount - discount_amount

    final_amount = int(final_amount)

    try:
        intent = stripe.PaymentIntent.create(
            amount=final_amount,
            currency=order_currency,
            payment_method_types=["card"],
            metadata={
                'order_id': order.id,
                'tax_amount': tax_amount,
                'discount_amount': discount_amount
            }
        )
        return JsonResponse({
            'client_secret': intent.client_secret,
            'total_price': total_price,
            'final_amount': final_amount,
            'tax_amount': tax_amount,  
            'discount_amount': discount_amount,
            'currency':order_currency
        })
    except stripe.error.StripeError as e:
        return JsonResponse({'error': str(e)}, status=400)

def payment_page(request):
    client_secret = request.GET.get('clientSecret')
    total_price = request.GET.get('totalPrice')
    final_amount = request.GET.get('finalAmount')
    discount = request.GET.get('discount')
    tax = request.GET.get('tax')
    currency = request.GET.get('currency')
    return render(request, 'orderpayment/payment_page.html', {
        'client_secret': client_secret,
        'total_price': total_price,
        'final_amount': final_amount,
        'discount': discount,
        'tax': tax,
        'currency': currency,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    })
