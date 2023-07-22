from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.forms import ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import *


def index(request):

    listings = Listing.objects.filter(active=True).order_by("-time")
    
    return render(request, "auctions/index.html", {
        "listings": listings,
        "page_text": "Active Listings"
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def categories(request):
    categories = Category.objects.all().order_by("type")
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def category(request, type):
    if type.lower() == "unspecified":
        listings = Listing.objects.filter(category=None).filter(active=True).order_by("-time")
        return render(request, "auctions/index.html", {
            "page_text": "Unspecified",
            "listings": listings
        })

    categories = Category.objects.all().values()
    for i in categories:
        if type.lower() == i["type"].lower():
            category = Category.objects.get(type=type.capitalize())
            break
    else:
        return render(request, "auctions/error.html", {
            "message": "This category does not exist!"
        })
    
    listings = Listing.objects.filter(category=category).filter(active=True).order_by("-time")
    return render(request, "auctions/index.html", {
        "page_text":category.type,
        "listings": listings
    })

@login_required(login_url="login")
def watchlist(request):
    listings = Listing.objects.filter(watchers=request.user).filter(active=True)
    return render(request, "auctions/index.html", {
        "page_text": "Watchlist",
        "listings": listings
    })

@login_required(login_url="login")
def create(request):
    if request.method == "POST":
        
        image = request.POST["image"]
        description = request.POST["description"]

        if "category" in request.POST:
            category=request.POST["category"]
            category=Category.objects.get(category_id=category)
        else:
            category=None
        
        if request.POST["title"] != "":
            title = request.POST["title"]
        else: 
            title = None

        bid = request.POST["starting_bid"]
        try:
            listing = Listing(
                title=title,
                price=bid,
                user=request.user,
                category=category,
                description=description,
                image=image
                )
            listing.save()
            
        except (ValidationError, IntegrityError) as error:
            return render(request, "auctions/create.html", {
                "bad_message": "Must fill out all required fields",
                "image_copy":image,
                "description_copy":description,
                "title_copy":title,
                "bid_copy":bid,
                "categories": Category.objects.all().order_by("type"),
                "category": category
            })
        
        return render(request, "auctions/create.html", {
                "categories": Category.objects.all().order_by("type"),
                "good_message": "Listing created!"
        })

    return render(request, "auctions/create.html", {
        "categories": Category.objects.all().order_by("type")
    })

def listing(request, num):
    if request.method == "POST":
        item = Listing.objects.get(listing_id=num)
        user = request.user
        watchers = item.watchers.all()
        comments= Comment.objects.filter(listing=item).order_by("-time")
        bid_count = Bid.objects.filter(listing=item).count()
        try:
            recent_bidder = Bid.objects.filter(listing=item).order_by("-time").first().user
        except AttributeError:
            recent_bidder = None

        if "comment_button" in request.POST:
            description = request.POST["comment"]
            comment = Comment(
                listing=item,
                user=user,
                description=description
            )
            comment.save()
            comments= Comment.objects.filter(listing=item).order_by("-time")
            return render(request, "auctions/listing.html", {
                "listing": item,
                "comments":comments,
                "good_message":"Comment added!",
                "watchers": watchers,
                "bid_count": bid_count,
                "recent_bidder": recent_bidder

            })
        elif "watchlist" in request.POST:
            item.watchers.add(request.user)
            watchers = item.watchers.all()
        
            return render(request, "auctions/listing.html", {
                "listing": item,
                "comments":comments,
                "good_message":"Added to watchlist!",
                "watchers": watchers,
                "bid_count": bid_count,
                "recent_bidder": recent_bidder
            })
        elif "rm_watchlist" in request.POST:
            item.watchers.remove(request.user)
            watchers = item.watchers.all()

            return render(request, "auctions/listing.html", {
                "listing": item,
                "comments":comments,
                "good_message":"Removed from watchlist!",
                "watchers": watchers,
                "bid_count": bid_count,
                "recent_bidder": recent_bidder
            })
        elif "close" in request.POST:

            if recent_bidder:
                item.winner = recent_bidder
            else: 
                item.winner = None
            
            item.active = False
            item.save()

            return render(request, "auctions/listing.html", {
                "listing": item,
                "comments":comments,
                "good_message":"Auction closed!",
                "watchers": watchers,
                "bid_count": bid_count,
                "recent_bidder": recent_bidder
            })
        elif "bid_button" in request.POST:
            bid = float(request.POST["bid"])
            if (bid_count == 0 and bid < item.price) or (bid_count >= 1 and bid <= item.price):
                return render(request, "auctions/listing.html", {
                    "listing":item,
                    "bad_message":"Bid must be higher than price!",
                    "comments":comments,
                    "watchers": watchers,
                    "bid_count": bid_count,
                    "recent_bidder": recent_bidder
                    })
            else:
                item.price = bid
                item.save()
                new_bid = Bid(
                        amount=bid,
                        listing=item,
                        user=request.user
                    )
                new_bid.save()
                bid_count += 1
                recent_bidder = request.user

                return render(request, "auctions/listing.html", {
                    "listing":item,
                    "good_message":"Bid placed!",
                    "comments":comments,
                    "watchers": watchers,
                    "bid_count": bid_count,
                    "recent_bidder": recent_bidder
                    })

    try:
        item = Listing.objects.get(listing_id=num)
    except Exception as e:
        return render(request, "auctions/error.html", {
            "message": "This listing does not exist!",
        })
    comments= Comment.objects.filter(listing=item).order_by("-time")
    watchers = item.watchers.all()
    bid_count = Bid.objects.filter(listing=item).count()
    try:
        recent_bidder = Bid.objects.filter(listing=item).order_by("-time").first().user
    except AttributeError:
        recent_bidder = None
    return render(request, "auctions/listing.html", {
        "listing":item,
        "comments":comments,
        "watchers": watchers,
        "bid_count": bid_count,
        "recent_bidder": recent_bidder
    })

def winnings(request):
    listings = Listing.objects.filter(winner=request.user)
    return render(request, "auctions/index.html", {
        "page_text": "Winnings",
        "listings": listings
    })