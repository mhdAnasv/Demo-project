from django.contrib import admin
from cart.models import Cart,placeorder,account

admin.site.register(Cart)
admin.site.register(placeorder)
admin.site.register(account)
