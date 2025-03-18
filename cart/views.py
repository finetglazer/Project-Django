# cart/views.py
from django.shortcuts import render, get_object_or_404

from book.models import Item
from .models import Cart, CartItem
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from decimal import Decimal


def cart_view(request):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        messages.error(request, "Please log in to view your cart.")
        return redirect('login')  # Make sure you have a URL named 'login'

    # Retrieve the cart for the logged-in user, or create one if it doesn't exist
    cart, created = Cart.objects.get_or_create(user=request.user)

    context = {
        'carts': cart.cart_items.all(),
        'totalPrice': cart.total_price(),
        'customerId': request.user.id,
        'cart_count': cart.cart_items.count(),  # For header display
    }
    return render(request, 'cart.html', context)


def add_to_cart(request, item_id):
    if request.method != "POST":
        messages.error(request, "Invalid request method.")
        return redirect('search')

    item = get_object_or_404(Item, pk=item_id)

    # Debug: print user info
    print("User:", request.user, "Authenticated:", request.user.is_authenticated)

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        else:
            cart_item.quantity = 1
            cart_item.save()
        print("Database cart updated for user", request.user)
    else:
        # Fallback for anonymous users: use session cart
        session_cart = request.session.get('cart', {})
        item_key = str(item_id)
        if item_key in session_cart:
            session_cart[item_key] += 1
        else:
            session_cart[item_key] = 1
        request.session['cart'] = session_cart
        print("Session cart updated:", request.session['cart'])

    messages.success(request, f"Added {item.name} to your cart.")
    return redirect('search')


def cart_remove(request, customerId):
    if request.method != "POST":
        messages.error(request, "Invalid request method.")
        return redirect('cart:cart_view')

    if not request.user.is_authenticated:
        messages.error(request, "Please log in to modify your cart.")
        return redirect('login')

    # Ensure the logged-in user's ID matches the customerId in the URL
    if request.user.id != int(customerId):
        messages.error(request, "You are not authorized to modify this cart.")
        return redirect('cart:cart_view')

    # Retrieve the item ID from the POST data
    item_id = request.POST.get("itemId")
    if not item_id:
        messages.error(request, "No item specified.")
        return redirect('cart:cart_view')

    # Get (or create) the user's cart
    cart, _ = Cart.objects.get_or_create(user=request.user)

    # Try to find the cart item and delete it
    try:
        cart_item = CartItem.objects.get(cart=cart, item__id=item_id)
        cart_item.delete()
        messages.success(request, "Item removed from your cart.")
    except CartItem.DoesNotExist:
        messages.error(request, "Item not found in your cart.")

    return redirect('cart:cart_view')
