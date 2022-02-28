from django.urls import path

from . import views
app_name = 'auctions'
urlpatterns = [
    path("", views.index, name="index"),
    path("list/<slug>/<id>", views.detail_page, name="detail"),
    path("category/<slug>/<id>", views.category_page, name="category"),
    path("create-list", views.create_list, name="create-list"),
    path("close-listing/<id>", views.close_listing, name="close-listing"),
    path("wathlist", views.wathlist, name="wathlist"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("nav", views.nav_view, name="nav"),
    path("add-bid/<id>", views.add_bid, name="add-bid"),
]
