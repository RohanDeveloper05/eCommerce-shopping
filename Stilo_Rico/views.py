from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .middlewares import auth, guest
from .models import Store, Product, Cart, CartItem
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import logging
from django.urls import reverse

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
logger = logging.getLogger(__name__)

@guest
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Registration failed. Please check the form for errors.')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})

@guest
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Login failed. Please check your username and password.')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

@auth
def home(request):
    stores = Store.objects.all()
    return render(request, 'index.html', {'stores': stores})

def store_products(request, store_name):
    store = get_object_or_404(Store, name=store_name)
    products = store.products.all()
    return render(request, 'product.html', {'store': store, 'products': products})

@auth
@csrf_exempt
def checkout_view(request):
    cart = Cart.objects.filter(user=request.user).first()

    if not cart or cart.items.count() == 0:
        messages.info(request, 'Your cart is empty.')
        return redirect('checkout')

    total_amount = int(cart.total_amount() * 100)  # Convert to paisa
    currency = 'INR'

    try:
        logger.debug(f"Creating Razorpay order with amount: {total_amount}, currency: {currency}")

        razorpay_order = razorpay_client.order.create({
            'amount': total_amount,
            'currency': currency,
            'payment_capture': '1'
        })

        razorpay_order_id = razorpay_order['id']
        callback_url = reverse('payment_success')

        context = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            'amount': total_amount,
            'currency': currency,
            'callback_url': callback_url,
        }

        return render(request, 'checkout.html', context )

    except razorpay.errors.BadRequestError as e:
        logger.error(f"Razorpay BadRequestError: {str(e)}")
        messages.error(request, 'There was an error processing your payment. Please try again.')
        return redirect('checkout')

@csrf_exempt
def payment_success(request):
    response = request.POST
    params_dict = {
        'razorpay_order_id': response.get('razorpay_order_id'),
        'razorpay_payment_id': response.get('razorpay_payment_id'),
        'razorpay_signature': response.get('razorpay_signature')
    }
    try:
        razorpay_client.utility.verify_payment_signature(params_dict)
        messages.success(request, 'Payment was successful.')
        return render(request, 'payment_success.html')
    except razorpay.errors.SignatureVerificationError as e:
        logger.error(f"Payment verification failed: {str(e)}")
        messages.error(request, 'Payment failed. Please try again.')
        return render(request, 'payment_failure.html')

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
    else:
        cart_item.quantity = 1
    cart_item.save()
    messages.success(request, f'{product.name} was added to your cart.')
    return redirect('cart_view')

@login_required
def cart_view(request):
    cart = Cart.objects.filter(user=request.user).first()
    if cart is None or cart.items.count() == 0:
        messages.info(request, 'Your cart is currently empty.')
        return redirect('home')

    total_items = cart.total_items()
    total_amount = cart.total_amount()

    context = {
        'cart': cart,
        'total_items': total_items,
        'total_amount': total_amount,
    }
    return render(request, 'cart.html', context)

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('cart_view')

@login_required
def user_profile_view(request):
    return render(request, 'user_profile.html', {'user': request.user})

def logout_view(request):
    logout(request)
    return redirect('login')
