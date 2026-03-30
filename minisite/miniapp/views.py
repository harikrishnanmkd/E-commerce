from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart, Order
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm
from django.contrib import messages

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


def products(request):
    items = Product.objects.all()
    return render(request, 'products.html', {'items': items})

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'product_detail.html', {'product': product})


@login_required
def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')



@login_required
def cart(request):
    items = Cart.objects.filter(user=request.user)

    # Calculate total price
    total_price = sum(item.product.price * item.quantity for item in items)

    if request.method == "POST":

        #  DELETE ITEM
        if 'delete_item' in request.POST:
            item_id = request.POST.get('delete_item')
            Cart.objects.filter(id=item_id, user=request.user).delete()
            return redirect('cart')

        # PLACE ORDER
        selected_ids = request.POST.getlist('selected_items')

        if selected_ids:
            selected_items = Cart.objects.filter(id__in=selected_ids, user=request.user)

            for item in selected_items:
                Order.objects.create(
                    user=request.user,
                    product=item.product,
                    quantity=item.quantity
                )

            selected_items.delete()
            return redirect('success')

    # ✅ Pass total_price to template
    return render(request, 'cart.html', {'items': items, 'total_price': total_price})

@login_required
def place_order(request):
    cart_items = Cart.objects.filter(user=request.user)

    for item in cart_items:
        Order.objects.create(
            user=request.user,
            product=item.product,
            quantity=item.quantity
        )

    cart_items.delete()
    return redirect('success')


@login_required
def orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders.html', {'orders': orders})


def success(request):
    return render(request, 'success.html')


# Registration View
def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = request.POST.get('confirm_password')

            #  Check password match
            if password != confirm_password:
                messages.error(request, "Passwords do not match")
                return render(request, 'register.html', {'form': form})

            #  Check username/email existence
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already taken")
                return render(request, 'register.html', {'form': form})
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already registered")
                return render(request, 'register.html', {'form': form})

            # Create user
            user = User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, "Registration successful! You can login now.")
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


# Login View
def login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user:
                auth_login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


# Logout View
def logout(request):
    auth_logout(request)
    return redirect('login')


