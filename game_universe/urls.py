from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

from game_universe import view

urlpatterns = [

    path('i18n/', include('django.conf.urls.i18n')),
]
urlpatterns = i18n_patterns(

    path("admin/", admin.site.urls),


    path('', view.index2, name="home"),

    path('index/', view.index, name="index"),

    path('contact/', view.contact, name="contact"),

    path('index2/', view.index2, name="index2"),

    path('action/', view.action, name="action"),

    path('strategy/', view.strategy, name="strategy"),

    path('persian/', view.persian, name="persian"),

    path('puzzle/', view.puzzle, name="puzzle"),

    path('multi/', view.multi, name="multi"),

    path('new/', view.new, name="new"),

    path('online/', view.online, name="online"),

    path('search/', view.search_view, name='search'),


    path('detail/<int:id>/', view.detail, name="detail"),


    path('review/<int:game_id>/', view.review, name="review"),

    path('add-to-cart/', view.add_to_cart, name="add_to_cart"),

    path('cart/', view.cart_detail, name="cart_detail"),


    path('cart/remove/<int:game_id>/', view.remove_from_cart, name="remove_from_cart"),

    path('checkout/', view.checkout, name="checkout"),


    path('to-bank/<int:order_id>/', view.to_bank, name="to_bank"),

    path('accounts/', include('accounts.urls', namespace='accounts')),

    path('simulate-payment/', view.simulate_payment, name="simulate_payment"),


    path('download/<int:order_game_id>/', view.download_game, name='download_game'),

)

"""
urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls),
    path('index/', view.index, name="index"),
    path('contact/', view.contact, name="contact"),
    path('index2/', view.index2, name="index2"),
    path('action/', view.action, name="action"),
    path('strategy/', view.strategy, name="strategy"),
    path('persian/', view.persian, name="persian"),
    path('puzzle/', view.puzzle, name="puzzle"),
    path('multi/', view.multi, name="multi"),
    path('new/', view.new, name="new"),
    path('online/', view.online, name="online"),
    path('search/', view.search_view, name='search'),
    path('detail/<int:id>/', view.detail, name="detail"),
    path('review/<int:game_id>/', view.review, name="review"),
    path('add-to-cart/', view.add_to_cart, name="add_to_cart"),
    path('cart/', view.cart_detail, name="cart_detail"),
    path('cart/remove/<int:game_id>/', view.remove_from_cart, name="remove_from_cart"),
    path('checkout/', view.checkout, name="checkout"),
    path('to-bank/<int:order_id>/', view.to_bank, name="to_bank"),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('simulate-payment/', view.simulate_payment, name="simulate_payment"),
    path('download/<int:order_game_id>/', view.download_game, name='download_game'),
)
"""

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
