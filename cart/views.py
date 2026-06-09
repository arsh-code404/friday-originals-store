from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from hii.models import Product
from .cart import Cart
from .models import Order
import json
from datetime import datetime


def cart_summary(request):
    cart = Cart(request)
    return render(request, "cart/cart_summary.html", {"cart": cart})


def cart_add(request):
    if not request.user.is_authenticated:
        return JsonResponse({
            "login_required": True
        })

    if request.method == "POST":
        cart = Cart(request)

        product_id = request.POST.get("product_id")
        quantity = int(request.POST.get("quantity", 1))

        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, quantity=quantity)

        return JsonResponse({
            "cartq": cart.item_count()
        })

    return JsonResponse({"error": "Invalid request"}, status=400)


def cart_update(request):
    if request.method == "POST":
        cart = Cart(request)

        product_id = request.POST.get("product_id")
        quantity = int(request.POST.get("quantity", 1))

        product = get_object_or_404(Product, id=product_id)

        cart.add(
            product=product,
            quantity=quantity,
            update=True
        )

        item = cart.cart[str(product_id)]

        return JsonResponse({
            "success": True,
            "item_total": float(item["price"]) * item["quantity"],
            "cart_total": cart.get_total_price(),
            "cartq": cart.item_count()
        })

    return JsonResponse({"error": "Invalid request"}, status=400)


def cart_delete(request):
    if request.method == "POST":
        cart = Cart(request)
        product_id = request.POST.get("product_id")

        if product_id:
            cart.remove(product_id)

            return JsonResponse({
                "success": True,
                "cart_total": cart.get_total_price(),
                "cartq": cart.item_count()
            })

    return JsonResponse({"error": "Invalid request"}, status=400)


def save_order(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            
            # Generate order ID
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            order_id = f"ORD{timestamp}"
            
            # Create order
            order = Order.objects.create(
                order_id=order_id,
                user=request.user if request.user.is_authenticated else None,
                customer_name=data.get('customer_name', 'Guest'),
                customer_email=data.get('customer_email', ''),
                customer_phone=data.get('customer_phone', ''),
                items=json.dumps(data.get('items', [])),
                subtotal=data.get('subtotal', 0),
                delivery_fee=data.get('delivery_fee', 250),
                total=data.get('total', 0),
                status='pending',
                whatsapp_sent=True
            )

            # Clear the cart session
            cart = Cart(request)
            cart.cart.clear()
            cart.session.modified = True
            
            return JsonResponse({
                "success": True,
                "order_id": order_id,
                "message": "Order saved successfully"
            })
        except Exception as e:
            return JsonResponse({
                "success": False,
                "error": str(e)
            }, status=400)
    
    return JsonResponse({"error": "Invalid request method"}, status=405)