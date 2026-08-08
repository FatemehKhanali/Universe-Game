from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from game_universe.models import Game
from .models import Order, OrderGame, Cart
from accounts.models import User,Profile
#from .cart import SessionCart


#@receiver(user_logged_in)
#def sync_session_with_db(sender, request, user, **kwargs):
# cart = SessionCart(request)
    #   for item in cart:
#   Cart.objects.get_or_create(
        #  user_id=user.id,
        #  product_id=item['product_id'],
        #  defaults={
                     #       'quantity': item['quantity']
                            #      }
                     #   )


@receiver(post_save, sender=Game)
def soft_delete_cart(sender, instance, created, **kwargs):
    if not created:
        game: Game = instance
        if game.deleted:
            carts = Cart.objects.filter(game=game)
            for cart in carts:
                cart.delete()

            order_games = OrderGame.objects.filter(game=game)
            for order_game in order_games:
                order_game.delete()


@receiver(post_save, sender=User)
def soft_delete_cart(sender, instance, created, **kwargs):
    if not created:
        user: User = instance
        if user.deleted:
            try:
                Profile.objects.get(user=user).delete()
            except Profile.DoesNotExist:
                pass
            carts = Cart.objects.filter(user=user)
            for cart in carts:
                cart.delete()

          #  try:
           #     Profile.objects.get(user=user).delete()
           # except Profile.DoesNotExist:
            #    pass

            orders = Order.objects.filter(user=user)
            for order in orders:
                order.delete()


@receiver(post_save, sender=Order)
def soft_delete_order_game(sender, instance, created, **kwargs):
    if not created:
        order: Order = instance
        if order.deleted:
            order_games = OrderGame.objects.filter(order=order)
            for order_game in order_games:
                order_game.delete()
