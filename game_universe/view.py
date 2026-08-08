from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.decorators.http import require_POST
from django.conf import settings
import requests
import json

from accounts.models import Profile, Province, city
from .models import Game, Order, OrderGame
from .cart import Cart
from .forms import OrderForm


def index2(request):
    games = Game.objects.all()
    return render(request, "index2.html", {'games': games})


def review(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    return render(request, "review.html", {'game': game})


def detail(request, id: int):
    game = get_object_or_404(Game, id=id)
    context = {'game': game}
    return render(request, "detail.html", context)


def index(request):
    return render(request, "index.html")


def action(request):
    games = Game.objects.filter(category__title='Action')
    return render(request, "action.html", {'games': games})


def strategy(request):
    games = Game.objects.filter(category__title='Strategy')
    return render(request, "strategy.html", {'games': games})


def persian(request):
    games = Game.objects.filter(category__title='Persian')
    return render(request, "persian.html", {'games': games})


def puzzle(request):
    games = Game.objects.filter(category__title='Puzzle & Mystery')
    return render(request, "puzzle.html", {'games': games})


def multi(request):
    games = Game.objects.filter(category__title='Multiplayer')
    return render(request, "multi.html", {'games': games})


def new(request):
    games = Game.objects.filter(category__title='Hot & new')
    return render(request, "new.html", {'games': games})


def online(request):
    return render(request, "online.html")


@require_POST
def add_to_cart(request):
    game_id = request.POST.get('game_id')
    quantity = request.POST.get('quantity', 1)
    update = True if request.POST.get('update') == '1' else False
    game = get_object_or_404(Game, id=game_id)

    cart = Cart(request)
    cart.add(game_id, game.price, int(quantity), update)

    return redirect(reverse('cart_detail'))

def cart_detail(request):
    cart = Cart(request)
    return render(request, "cart_detail.html", {'cart': cart})

def remove_from_cart(request, game_id):
    if Game.objects.filter(id=game_id).exists():
        cart = Cart(request)
        cart.remove(game_id)
        return redirect(reverse('cart_detail'))
    raise Http404('Game does not exist.')


def save_order_different(cart, order_form, request):
    if not order_form.is_valid():
        raise ValueError("Order form is not valid")

    order = Order.objects.create(
        user=request.user,
        total_price=cart.get_total_price,
        note=request.POST.get('note', ''),
        diffrent_address=True,
        first_name=order_form.cleaned_data['first_name'],
        last_name=order_form.cleaned_data['last_name'],
        mobile=order_form.cleaned_data['mobile'],
        postal_code=order_form.cleaned_data['postal_code'],
        address=order_form.cleaned_data['address'],
        city=order_form.cleaned_data['city'],
    )

    for item in cart:
        OrderGame.objects.create(
            order=order,
            game_id=item['game_id'],
            quantity=item['quantity'],
            price=item['price']
        )

    return order


@login_required
def checkout(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return redirect(reverse('accounts:edit_profile'))

    cart = Cart(request)


    if len(cart.cart) == 0:
        return redirect('cart_detail')

    if request.method == 'POST':
        different_address = request.POST.get('different_address')

        if different_address == '1':
            order_form_data = {
                'first_name': request.POST.get('first_name'),
                'last_name': request.POST.get('last_name'),
                'mobile': request.POST.get('mobile'),
                'postal_code': request.POST.get('postal_code'),
                'address': request.POST.get('address'),
                'city': request.POST.get('city'),
            }

            order_form = OrderForm(order_form_data)
            if order_form.is_valid():
                order = save_order_different(cart, order_form, request)
                cart.clear()
                return redirect(reverse('to_bank', args=[order.id]))
            else:
                context = {
                    'form': order_form,
                    'provinces': Province.objects.all(),
                    'error': 'Please fill out the form correctly.',
                    'profile': profile,
                }
                return render(request, "checkout.html", context=context)
        else:

            order = Order.objects.create(
                user=request.user,
                total_price=cart.get_total_price,
                note=request.POST.get('note', ''),
                diffrent_address=False,
                first_name=request.user.first_name or 'unknow',
                last_name=request.user.last_name or 'unknow',
                mobile=request.user.mobile,
                postal_code=profile.postal_code,
                address=profile.address,
                city=profile.city,
            )

            for item in cart:
                OrderGame.objects.create(
                    order=order,
                    game_id=item['game_id'],
                    quantity=item['quantity'],
                    price=item['price']
                )

            cart.clear()
            return redirect(reverse('to_bank', args=[order.id]))

    context = {
        'provinces': Province.objects.all(),
        'profile': profile,
    }
    return render(request, "checkout.html", context=context)

def contact(request):
        return render(request, "contact.html")

def to_bank(request, order_id):
    order = get_object_or_404(Order, id=order_id, status__isnull=True)


    request.session['payment_order_id'] = order.id
    request.session['payment_amount'] = order.total_price



    return render(request, 'zarinpal_simulator.html', {
        'order': order,
        'merchant_name': 'Game Store',
        'amount': order.total_price,
        'description': f'Buy Game - Order {order.id}',
    })


def simulate_payment(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        action = request.POST.get('action')

        if order_id and action == 'success':
            order = get_object_or_404(Order, id=order_id)
            order.status = True
            order.save()

            # delete session
            if 'payment_order_id' in request.session:
                del request.session['payment_order_id']
            if 'payment_amount' in request.session:
                del request.session['payment_amount']

            return render(request, 'payment_success.html', {
                'order': order,
                'ref_id': f'ZP{order.id}123456',
                'success': True,
                'message': 'Payment was successful!'
            })

    return redirect('/checkout/')


from django.http import HttpResponse
import os
from django.conf import settings


def search_view(request):
    query = request.GET.get('q', '').strip()

    if query:
        game = Game.objects.filter(title__icontains=query).first()

        if game:
            return redirect('detail', id=game.id)

    return redirect('home')


def download_game(request, order_game_id):

    try:
        order_game = get_object_or_404(OrderGame, id=order_game_id)


        if order_game.order.user != request.user:
            return Http404("You are not authorized to download this file.")


        if not order_game.order.status:
            return Http404("The order has not yet been paid for.")
        game_content = f"""
🎮 Game: {order_game.game.title}
🏷️ Category: {order_game.game.category.title if order_game.game.category else 'Unknow'}
💰 Price: {order_game.price} $
📦 Quantity: {order_game.quantity}

🔥 Order_number: {order_game.order.id}
📅 Date: {order_game.order.created_at}
🔐 Serial_number: GP{order_game.order.id}{order_game.game.id}123

─────────────────────────────────
🚀  how to Install:
1.extract  file 
2.Run setup.exe  
3. Use activity code: {order_game.game.title[:3].upper()}{order_game.order.id}
4. Enjoy it! 🎮

✨ اThanks for shopping
🌐  GameUniverse-khanali
        """
        # create response for download
        response = HttpResponse(game_content, content_type='text/plain; charset=utf-8')
        filename = f"{order_game.game.title.replace(' ', '_')}_Game.txt"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        return response

    except OrderGame.DoesNotExist:
        raise Http404("we cant't find the game")



