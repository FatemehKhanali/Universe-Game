from decimal import Decimal

CART_SESSION_ID = 'cart'


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    @property
    def game_ids(self):
        return self.cart.keys()

    @property
    def get_total_price(self):
        return sum(int(item['price']) * item['quantity'] for item in self.cart.values())

    def __getitem__(self, item):
        return self.cart[item]

    def __iter__(self):
        for item in self.cart.values():
            yield item

    def __len__(self):

        return len(self.cart)

    def add(self, game_id, game_price, quantity, update):
        game_id = str(game_id)

        if game_id not in self.cart:
            self.cart[game_id] = {
                'game_id': int(game_id),
                'quantity': 0,
                'price': int(game_price)
            }

        if update:
            self.cart[game_id]['quantity'] = int(quantity)
        else:
            self.cart[game_id]['quantity'] += int(quantity)

        self.session[CART_SESSION_ID] = self.cart
        self.session.modified = True

    def clear(self):

        del self.session[CART_SESSION_ID]
        self.session.modified = True

    def remove(self, game_id):

        game_id = str(game_id)
        if game_id in self.cart:
            del self.cart[game_id]
            self.session.modified = True

    def get_total_items(self):

        return sum(item['quantity'] for item in self.cart.values())

    def is_empty(self):

        return len(self.cart) == 0