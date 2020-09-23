from django.contrib import admin

from .models import Checkout, ItemGroup, Item

admin.site.register(Checkout)
admin.site.register(ItemGroup)
admin.site.register(Item)
