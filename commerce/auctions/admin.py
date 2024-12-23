from django.contrib import admin
from .models import Auction, Watchlist, Bid, Closed_Deals, Comment

# Register your models here.

admin.site.register(Auction)
admin.site.register(Watchlist)
admin.site.register(Bid)
admin.site.register(Closed_Deals)
admin.site.register(Comment)