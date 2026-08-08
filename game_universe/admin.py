from django.contrib import admin
from . import models


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    search_fields = ['title']

    def delete_queryset(self, request, queryset):
        for category in queryset:
            category.delete()

class GameAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'price', 'quantity', 'status']
    search_fields = ['title']
    list_filter = ['status']

    def delete_queryset(self, request, queryset):
        for game in queryset:
            game.delete()

admin.site.register(models.Cart)
admin.site.register(models.Order)
admin.site.register(models.OrderGame)
admin.site.register(models.PaymentLog)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Game, GameAdmin)
