from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories/", views.categories, name="categories"),
    path("categories/<str:type>", views.category, name="category"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("create", views.create, name="create"),
    path("listing/<int:num>", views.listing, name="listing"),
    path("winnings/", views.winnings, name="winnings")
]
