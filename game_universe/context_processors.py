from .cart import Cart
from .models import Game
from decimal import Decimal


def cart(request):
    try:
        cart_session = Cart(request)
        all_total_price = 0
        cart_length = 0

        if cart_session and hasattr(cart_session, 'cart') and cart_session.cart:
            game_ids = cart_session.game_ids
            games = Game.objects.filter(id__in=game_ids)


            for game in games:
                if str(game.id) in cart_session.cart:
                    cart_session.cart[str(game.id)]['game'] = game


            for item in cart_session:
                try:
                    item['total_price'] = Decimal(str(item['price'])) * Decimal(str(item['quantity']))
                    all_total_price += item['total_price']
                    cart_length += item['quantity']
                except (ValueError, KeyError, TypeError):
                    continue

        # Setting values ​​in cart_session
        cart_session.all_total_price = all_total_price
        cart_session.cart_length = cart_length

        return {
            'cart': cart_session,
            'all_total_price': all_total_price,
            'cart_length': cart_length
        }

    except Exception as e:

        return {
            'cart': Cart(request),
            'all_total_price': 0,
            'cart_length': 0
        }