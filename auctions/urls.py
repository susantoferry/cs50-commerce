from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("category/<str:cat_name>/<str:cat_id>", views.category, name="category"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("auction/<str:title>/<str:id>", views.item_detail, name="item_detail"),
    path("comment/<str:title>/<str:id>", views.comment , name="comment"),
    path("bid/<str:id>", views.bid , name="bid"),
    path("auction-image/<str:id>", views.auction_image, name="auction_image"),
    path("post-listing", views.post_listing, name="post_listing"),
    path("close-auction/<str:id>", views.close_auction, name="close_auction"),
    path("my-watchlist", views.my_watchlist, name="my_watchlist"),
    path("my-watchlist/status/<str:cat>", views.watchlist_by_cat, name="watchlist_by_cat"),
    path("watchlist/<str:id>", views.watchlist , name="watchlist"),
    path("messages", views.message, name="message"),
    path("messages-detail/<str:id>", views.message_detail, name="message_detail")
]
