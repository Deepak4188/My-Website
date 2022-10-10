from django import template
from cart.models import CartItem

register = template.Library()

@register.filter(name="is_in_cart")
def is_in_cart(product, user):
    if CartItem.objects.filter(productId=product, userId=user).exists():
        return True
    return False


@register.filter(name="product_count")
def cart_count(product, user):
    item = CartItem.objects.filter(productId=product, userId=user)
    if item != None:
        return item[0].quantity
    return 0