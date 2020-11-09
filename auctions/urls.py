from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("category/<str:cat_name>/<int:cat_id>", views.category, name="category"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("auction/<str:title>/<int:id>", views.item_detail, name="item_detail"),
    path("comment/<str:title>/<int:id>", views.comment , name="comment"),
    path("bid/<int:id>", views.bid , name="bid"),
    path("post-listing", views.post_listing, name="post_listing"),
    path("close-auction/<int:id>", views.close_auction, name="close_auction"),
    path("my-watchlist", views.my_watchlist, name="my_watchlist"),
    path("my-watchlist/status/<str:cat>", views.watchlist_by_cat, name="watchlist_by_cat"),
    path("watchlist/<int:id>", views.watchlist , name="watchlist"),
    path("messages", views.message, name="message"),
    path("messages-detail/<int:id>", views.message_detail, name="message_detail")
]
