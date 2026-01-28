from hii.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get("session_key")

        if not cart:
            cart = self.session["session_key"] = {}

        self.cart = cart

    # ADD / UPDATE
    def add(self, product, quantity, update=False):
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {
                "price": str(product.price),
                "quantity": 0,
            }

        if update:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity

        if self.cart[product_id]["quantity"] <= 0:
            del self.cart[product_id]

        self.session.modified = True

    # REMOVE
    def remove(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.session.modified = True

    # ITERATE (FIXED)
    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        product_map = {str(p.id): p for p in products}

        for product_id, item in self.cart.items():
            product = product_map.get(product_id)
            if not product:
                continue

            item_copy = item.copy()
            item_copy["product"] = product
            item_copy["price"] = float(item["price"])
            item_copy["total_price"] = item_copy["price"] * item["quantity"]

            yield item_copy

    # TOTAL
    def get_total_price(self):
        return sum(item["total_price"] for item in self)

    def item_count(self):
        return len(self.cart)
