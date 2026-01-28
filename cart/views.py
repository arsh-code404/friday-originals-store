from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from hii.models import Product
from .cart import Cart


def cart_summary(request):
    cart = Cart(request)
    return render(
        request,
        "cart/cart_summary.html",
        {"cart": cart}
    )

def cart_add(request):
    cart = Cart(request)

    if request.method == "POST":
        product_id = request.POST.get("product_id")
        quantity = int(request.POST.get("quantity", 1))

        product = get_object_or_404(Product, id=product_id)
        cart.add(product, quantity)

        return JsonResponse({
            "cartq": cart.item_count()
        })

    return JsonResponse({"error": "Invalid request"}, status=400)

def cart_update(request):
    if request.method == "POST":
        cart = Cart(request)

        product_id = request.POST.get("product_id")
        quantity = int(request.POST.get("quantity"))

        product = Product.objects.get(id=product_id)
        cart.add(product, quantity, update=True)

        item = cart.cart[str(product_id)]

        return JsonResponse({
            "item_total": float(item["price"]) * item["quantity"],
            "cart_total": cart.get_total_price(),
        })

    return JsonResponse({"error": "Invalid request"}, status=400)



def cart_delete(request):
    cart = Cart(request)

    if request.POST.get("action") == "delete":
        product_id = request.POST.get("product_id")
        cart.remove(product_id)

        return JsonResponse({
            "cart_total": cart.get_total_price(),
            "cart_count": cart.item_count()
        })
