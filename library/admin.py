from django.contrib import admin

from library.models import Checkout, Item, ItemGroup, Member

# Register your models here.
admin.site.register(Checkout)
admin.site.register(ItemGroup)
admin.site.register(Item)
admin.site.register(Member)
