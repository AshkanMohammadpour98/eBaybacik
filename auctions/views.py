from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import User
from lists.models import List, Category, Comment, Bid
from django.contrib.auth.decorators import login_required
from .forms import Create


def index(request):
    list = List.objects.status_list()
    context = {'title': 'home', 'list': list}
    return render(request, "auctions/index.html", context)


def detail_page(request, slug, id):
    list = get_object_or_404(List.objects.active_list(slug, id))
    close = False
    if request.user.is_authenticated and list.created_user_id == request.user.id:
            close = True
    if request.method == 'POST':
        text = request.POST.get('text-comment')
        Comment.objects.create(user_id=request.user.id, text=text, list_id=list.id)
    comments = Comment.objects.filter(list_id=list.id)
    context = {'title': list.title, 'list': list, 'close': close, 'comments': comments}
    return render(request, "auctions/singelpageslog.html", context)


def category_page(request, slug, id):
    category = Category.objects.get(id=id, slug=slug)
    lists = List.objects.filter(category=category)
    context = {'title': 'category', 'category': category, 'lists': lists}
    return render(request, "auctions/category_page.html", context)

@login_required(login_url='auctions:login')
def create_list(request):
    category = Category.objects.status_category()
    create_form = Create(request.POST or None)
    if create_form.is_valid():
        title = create_form.cleaned_data.get('title')
        descriptions = create_form.cleaned_data.get('descriptions')
        initial_price = create_form.cleaned_data.get('initial_price')
        image_url = create_form.cleaned_data.get('image_url')
        categories = request.POST.get('categories')
        categories_slug = Category.objects.get(slug=categories)
        list = List.objects.create(title=title, descriptions=descriptions, Initial_price=initial_price, created_user_id=request.user.id, image_url=image_url, slug=title)
        for cat in categories:
            list.category.add(categories_slug.id)
        list.save()
        return redirect('auctions:wathlist')
    context = {'category': category, 'form': create_form}
    return render(request, 'auctions/CreateListing.html', context)

@login_required(login_url='auctions:login')
def close_listing(request, id):
    list = List.objects.filter(id=id, created_user_id=request.user.id)
    list.delete()
    return redirect('auctions:index')

@login_required(login_url='auctions:login')
def wathlist(request):
    lists = List.objects.filter(created_user_id=request.user.id)
    context = {'title': 'wathlist', 'lists': lists}
    return render(request, 'auctions/wathlist.html', context)

@login_required(login_url='auctions:login')
def add_bid(request, id):
    list = List.objects.get(id=id)
    if request.method == "POST":
        bid = request.POST.get('bid')
        if bid is not None:
            Bid.objects.create(user_id=request.user.id, list_id=list.id, price=bid)
    return redirect('auctions:detail', list.slug, list.id)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('auctions:index')
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

@login_required(login_url='auctions:login')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


def register(request):
    if request.user.is_authenticated:
        return redirect('auctions:index')

    if request.method == "POST":
        email = request.POST["email"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username=email, first_name=firstname, last_name=lastname, email=email, password=password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")

def nav_view(request):
    category = Category.objects.status_category()
    context = {'category': category}
    return render(request, 'auctions/nav.html', context)