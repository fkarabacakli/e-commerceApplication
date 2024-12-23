from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("listing/<int:auction_id>",views.listing, name="listing"),
    path("create", views.create, name="create"),
    path("bid",views.bid, name="bid"),
    path("bid/delete", views.delete_bid, name="delete_bid"),
    path("close_deal", views.close_deal, name="close_deal"),
    path("deals", views.deals, name="deals"),
    path("category/<str:auction_category>",views.category, name="category" ),
    path("comment", views.comment, name="comment")
]
