from django.contrib import admin
from wishlist.models import Wishlist


class WishlistAdmin(admin.ModelAdmin):
    list_display = (
        'profile',
        'product',
    )

    ordering = ('profile',)


admin.site.register(Wishlist, WishlistAdmin)
