from django.contrib import admin

from .models import Auction, AuctionImage, Bid, Category, Comment, NotificationMsg, User, Watchlist

# Register your models here.

""" class FlightAdmin(admin.ModelAdmin):
    list_display = ("__str__", "duration")

class PassengerAdmin(admin.ModelAdmin):
    filter_horizontal = ("flights",) """

admin.site.register(Auction)
admin.site.register(AuctionImage)
admin.site.register(Bid)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(User)
admin.site.register(Watchlist)
admin.site.register(NotificationMsg)