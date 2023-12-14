from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q, Count
from datetime import datetime

from .models import Auction, Bid, Category, Comment, NotificationMsg ,User, Watchlist
from .forms import CommentsForm, CommentForm, SellForm

# Create your views here.

def category(request, cat_name, cat_id):
    notifications = get_notifications(request.user.id)
    return render(request, "auctions/index.html", {
        "auctions": Auction.objects.filter(category_id=cat_id).select_related(),
        "notifications": notifications,
        "title": "Active Listings " + cat_name.replace("-", " "),
        "cat_name": cat_name,
        "categories": Category.objects.all()
    })

def get_winner_bidding():
    actual_bid = Bid.objects.all()

    return actual_bid

def get_notifications(user_id):
    notifications = NotificationMsg.objects.filter(user=user_id, read=False).count()

    return notifications

def index(request):
    wlist = Watchlist.objects.filter(user = request.user.id)
    auctions = Auction.objects.filter(active = True).annotate(total=Count('bid_item')).order_by('-create_date')
    categories = Category.objects.all()
    notifications = get_notifications(request.user.id)

    return render(request, "auctions/index.html", {
        "auctions": auctions,
        "categories": categories,
        "title": "Active Listings",
        "notifications": notifications
    })

def item_detail(request, title, id):
    auction = Auction.objects.get(pk = id)
    comments = Comment.objects.filter(auction_item = id).order_by('-date')
    watchlist = Watchlist.objects.filter(auction_item = id, user = request.user.id)
    bids = Bid.objects.filter(auction = id).order_by('-date')
    bidder = Bid.objects.values('auction_id').filter(auction_id=id).annotate(total=Count('user', distinct=True))
    notifications = get_notifications(request.user.id)
    print(datetime.now())
    try:
        winner = Bid.objects.filter(auction = id).latest('amount').user
    except Bid.DoesNotExist:
        winner = ""

    
    if Bid.objects.filter(auction = auction):
        actual_bid = Bid.objects.filter(auction = auction).latest('amount').amount
    else:
        actual_bid = auction.price
    
    return render(request, "auctions/auction_detail.html", {
        "auction" : auction,
        "categories": Category.objects.all(),
        "bid": actual_bid,
        "commentform": CommentForm(),
        "comments": comments,
        "bids": bids,
        "watchlist": watchlist,
        "total_bid_by_user": bidder,
        "notifications": notifications,
        "winner": winner
    })

def adding_bid(request, title, id):
    filter = Auction.objects.get(id = id)
    item_stuff = details_and_comments(id)
    if request.method == "POST":
        form = BidForm(request.POST)
        if form.is_valid():
            bid_value = form.cleaned_data["bid_value"]
            if bid_value <= actual_bid(id):
                return render(request, "auctions/items-page.html", {
                    "BidForm": BidForm(),
                    "CommentForm": CommentsForm(),
                    "value": actual_bid(id),
                    "comments": item_stuff['comments'],
                    "items": item_stuff['details'],
                    "message" : 'Invalid value'
                })
            else:
                Bids.objects.create(
                    buyer = request.user,
                    bid_value = bid_value,
                    item_id = filter,
                )
    return HttpResponseRedirect(reverse("item_detail", args=(title, id,)))

def bid(request, id):
    listing_item = Auction.objects.get(pk=id)
    if request.method == "POST":
        if len(request.POST["bid_value"]) != 0:
            try:
                last_bid = Bid.objects.filter(auction = id).latest('amount').amount + 5
            except Bid.DoesNotExist:
                last_bid = listing_item.price + 5
            if float(request.POST["bid_value"]) >= last_bid:
                bid = Bid(auction=listing_item, 
                        user=request.user, 
                        amount=request.POST["bid_value"])
                bid.save()
                messages.add_message(request, messages.SUCCESS, "You're the high bidder on this item.")
                return HttpResponseRedirect(reverse("item_detail", args=(listing_item.title, id,)))
            else:
                messages.add_message(request, messages.WARNING, "You must bid at least $" + str(last_bid) + ".")
                return HttpResponseRedirect(reverse("item_detail", args=(listing_item.title, id,)))
        else:
            messages.add_message(request, messages.ERROR, "You bid cannot be empty.")
            return HttpResponseRedirect(reverse("item_detail", args=(listing_item.title, id,)))

def comment1(request, title, id):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            auction = Auction.objects.get(pk=list_id)
            data = form.save(commit=False)
            data.user = request.user
            data.auction_item = auction
            data.save()
            messages.add_message(request, messages.SUCCESS, "Your comment was successfully posted.")
            return HttpResponseRedirect(reverse("item_detail", args=(title, id,)))
        else:
            return render(request, "auctions/index.html", {
        "auctions": Auction.objects.all(),
        "categories": Category.objects.all()
    })

def comment(request, title, id):
    get_auction_id = Auction.objects.get(pk = id)
    if request.method == "POST":
        if (request.POST["comment"] != ""):
            comment = Comment(
                        comment=request.POST["comment"], 
                        user=request.user, 
                        auction_item=get_auction_id
                      )
            comment.save()
            messages.success(request, "Your comment has been posted!")
            return HttpResponseRedirect(reverse("item_detail", args=(title.replace(" ", "-"), id,)))
        else:
            messages.success(request, "Failed to post your comment!")
            return HttpResponseRedirect(reverse("item_detail", args=(title.replace(" ", "-"), id,)))

@login_required()
def post_listing(request):
    if request.method == "POST":
        get_cat_id = Category.objects.get(pk = request.POST["category"])
        auction = Auction(
            title = request.POST["title"],
            description = request.POST['description'],
            category = get_cat_id,
            price = request.POST["price"],
            seller = request.user,
            image = request.POST['image'],
            modify_date = datetime.now()
        )
        auction.save()
        wlist = Watchlist.objects.filter(user = request.user.id)
        messages.add_message(request, messages.SUCCESS, "Your listing has been successfully posted.")
        return HttpResponseRedirect(reverse("index"))
    
    return render(request, "auctions/create_auction.html", {
        "notifications": get_notifications(request.user.id),
<<<<<<< HEAD
        "categories": Category.objects.all(),
=======
        "categories": Category.objects.all().order_by("name"),
>>>>>>> 1f067c3 (re-indexing)
        "sellForm": SellForm(),
    })

@login_required
def close_auction(request, id):
    if request.method == "POST":
        auction = Auction.objects.get(pk=id)
        if request.user.id == auction.seller_id:
            auction.active = False
            auction.modify_date = datetime.now()
            auction.save()
            send_notification(auction.id)
            messages.add_message(request, messages.SUCCESS, "Your listing has been closed")
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.add_message(request, messages.ERROR, "Oops.. Something wrong when closing the listing.")
            return HttpResponseRedirect(reverse("index"))

def send_notification(id):
    rslt = False
    try:
        users = Bid.objects.filter(auction = id).values('user').distinct()
    except Bid.DoesNotExist:
        users = ""
    
    if users:
        winner = Bid.objects.filter(auction = id).latest('amount').user
        auction = Auction.objects.get(pk=id)
        rslt = True
        for user in users:
            notification = NotificationMsg()
            uid = User.objects.get(pk = user['user'])
            notification.user = uid
            notification.auction_item = auction
            if user['user'] == winner.id:
                notification.message = "You've won the auction!"  
                notification.is_status = 1
            else:
                notification.message = "Sorry, you didn't win this auction."
            notification.save()
    return rslt


def declare_winner(id, user):
    filter = Auction.objects.get(id = id)
    query = Bids.objects.filter(item_id = filter)
    if query:
        winner = query.latest('bid_value').buyer
    else:
        winner = 'There is no winner'
    return winner

@login_required
def message(request):
    auctions = Auction.objects.filter(active = False).annotate(total=Count('bid_item')).order_by('-create_date')
    notif_msg = NotificationMsg.objects.filter(user = request.user.id)
    notifications = get_notifications(request.user.id)
    categories = Category.objects.all()
    return render(request, "auctions/message.html", {
        "auctions": auctions,
        "categories": categories,
        "notif_msg": notif_msg,
        "notifications": notifications,
        "title": "Messages"
    })

@login_required
def message_detail(request, id):
    """ notif_msg = NotificationMsg()
    notif_msg.read = True
    notif_msg.save() """
    NotificationMsg.objects.filter(auction_item=id, user=request.user.id).update(read=True)
    auctions = Auction.objects.filter(active = True).annotate(total=Count('bid_item'))
    categories = Category.objects.all()
    notifications = get_notifications(request.user.id)
    return HttpResponseRedirect(reverse("message"))

@login_required
def watchlist(request, id):
    watched = Watchlist.objects.filter(auction_item=id, user=request.user.id)
    comments = Comment.objects.filter(auction_item = id).order_by('-date')
    # checking if it is already added to the watchlist
    if watched:
        # if its already there then user wants to remove it from watchlist
        watched.delete()
        # returning the updated content
        listing_item = Auction.objects.get(id=id)
        added = Watchlist.objects.filter(auction_item=id, user=request.user.id)
        return HttpResponseRedirect(reverse("item_detail", args=(listing_item.title.replace(" ", "-"), id,)))
    else:
        # if it not present then the user wants to add it to watchlist
        listing_item = Auction.objects.get(pk=id)
        watched = Watchlist()
        watched.user = request.user
        watched.auction_item = listing_item
        watched.save()
        # returning the updated content
        
        added = Watchlist.objects.filter(auction_item=id, user=request.user)
        return HttpResponseRedirect(reverse("item_detail", args=(listing_item.title.replace(" ", "-"), id,)))

def my_watchlist(request):
    watchlist_arr = []
    categories = Category.objects.all()
    notifications = get_notifications(request.user.id)
    watchlist = Watchlist.objects.filter(user = request.user.id)
    auctions = Auction.objects.annotate(total=Count('bid_item')).filter(active = True).order_by('-modify_date')
    if auctions:
        for auction in auctions:
            watchlist = Watchlist.objects.filter(user = request.user.id, auction_item__id = auction.id).first()
            if watchlist:
                watchlist_arr.append(watchlist)
    print(watchlist_arr)
    return render(request, "auctions/watchlist.html", {
        "auctions": watchlist_arr,
        "categories": categories,
        "notifications": notifications,
        "title": "Watchlist"
    })

def watchlist_by_cat(request, cat):
    status = False
    watchlist_arr = []
    if cat == "active":
        status = True
    categories = Category.objects.all()
    notifications = get_notifications(request.user.id)
    watchlist = Watchlist.objects.filter(user = request.user.id)
    auctions = Auction.objects.annotate(total=Count('bid_item')).filter(active = status).order_by('-modify_date')
    if auctions:
        for auction in auctions:
            watchlist = Watchlist.objects.filter(user = request.user.id, auction_item__id = auction.id).first()
            if watchlist:
                watchlist_arr.append(watchlist)
    
    return render(request, "auctions/watchlist.html", {
        "auctions": watchlist_arr,
        "categories": categories,
        "notifications": notifications,
        "title": "Watchlist"
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
        return render(request, "auctions/login.html", {
            "categories": Category.objects.all()
        })


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