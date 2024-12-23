from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import AuctionForm, BidForm, CommentForm

from .models import User, Auction, Watchlist, Bid, Closed_Deals, Comment


def index(request):
    return render(request, "auctions/index.html",{
        "auctions": Auction.objects.filter(closed=False)
    })


def login_view(request):
    next=""
    if request.user.is_authenticated:
        return render(request, "auctions/index.html",{
        "auctions": Auction.objects.all()
        })
    elif request.method == "POST":

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

login_required(login_url='login')
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

def listing(request, auction_id):
    try:
        auction = Auction.objects.get(pk=auction_id)
    except Auction.DoesNotExist:
        return render(request, "auctions/404.html", {
            "info": f"{auction_id} Product Could not Found!!!"
        })
    in_watchlist = False
    user_bid=False
    max_bid = "-"
    last_bid = "-"

    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        watchlist = Watchlist.objects.filter(user=user).first()
        if watchlist:
            if auction in watchlist.item.all():
                in_watchlist=True
        bid = Bid.objects.filter(owner=user, product=auction).first()
        if bid:
            user_bid=True
            last_bid = bid.bid

    bid_offers = Bid.objects.filter(product=auction)
    if bid_offers:
        max_bid=auction.price
        for bid_offer in bid_offers:
            if bid_offer.bid > max_bid:
                max_bid = bid_offer.bid

    form = BidForm()
    comment_form = CommentForm()

    comments = Comment.objects.filter(comment_product=auction)
    return render(request, "auctions/listing.html", {
        "auction": auction, 
        "in_watchlist":in_watchlist,
        "form":form,
        "comment_form":comment_form,
        "user_bid":user_bid,
        "max_bid":max_bid,
        "last_bid":last_bid,
        "comments":comments
    })

@login_required(login_url="login")
def watchlist(request):
    if request.method == "POST":
        auction_id = request.POST["auction_id"]
        user = User.objects.get(id=request.user.id)
        watchlist = Watchlist.objects.filter(user=user).first()
        auction = Auction.objects.get(pk=auction_id)
        if watchlist:
            if auction in watchlist.item.all():
                watchlist.item.remove(auction) 
                return HttpResponseRedirect(reverse("index"))  
            else:
                watchlist.item.add(auction)            
        else:
            new_watchlist = Watchlist.objects.create(user=user)
            new_watchlist.item.add(auction_id)

        return HttpResponseRedirect(reverse("watchlist"))
    else:
        user = User.objects.get(id=request.user.id)
        watchlist = Watchlist.objects.filter(user=user).first()
        if watchlist:
            auctions = Auction.objects.filter(pk__in=watchlist.item.all())
            return render(request, "auctions/watchlist.html", {
                "auctions": auctions, 
            })
        else:
            new_watchlist = Watchlist.objects.create(user=user)
            return HttpResponseRedirect(reverse("watchlist"))

@login_required(login_url="login")
def create(request):
    if request.method == "POST":
        form = AuctionForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data["category"]
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            price = form.cleaned_data["price"]
            image = form.cleaned_data["image"]
            new_auction = Auction(
                seller=User.objects.get(id=request.user.id),
                category= category,
                title = title,
                description= description,
                price= price,
                image = image,
            )
            new_auction.save()
            return listing(request, new_auction.id) 
        else:
            return render(request, "auctions/404.html", {
                "info":"Product Could not Created!!!"
            })       
    else:
        form = AuctionForm()
        return render(request, "auctions/create.html", {
            "form":form
        })
    
@login_required(login_url="login")
def bid(request):
    if request.method == "POST":
        form = BidForm(request.POST)
        if form.is_valid():
            auction_id = request.POST["auction_id"]
            auction = Auction.objects.get(pk=auction_id)
            user = User.objects.get(id=request.user.id)
            bid = form.cleaned_data["bid"] 
            user_offer = Bid.objects.filter(owner=user, product=auction).first()
            max_offer = "-"
            product_offers = Bid.objects.filter(product=auction)
            if product_offers:
                max_offer=auction.price
                for product_offer in product_offers:
                    if product_offer.bid > max_offer:
                        max_offer = product_offer.bid
                if bid <= max_offer:
                    return render(request, "auctions/404.html", {
                    "info":f"Bid Could not Created Min Offer is must be greater than {max_offer}"
                })
            else:
                if bid<auction.price:
                    return render(request, "auctions/404.html", {
                    "info":f"Bid Could not Created Min Offer is must be equal or greater than {auction.price}"
                })

            if user_offer is None:
                Bid.objects.create(owner=user, product=auction, bid=bid)
            else:
                user_offer.bid = bid
                user_offer.save()

            return HttpResponseRedirect(reverse("bid"))
        else:
            return render(request, "auctions/404.html", {
                "info":"There is problem about Your Bid"
            })   
    else:
        user = User.objects.get(id=request.user.id)
        bids = Bid.objects.filter(owner=user)
        return render(request, "auctions/bid.html", {
                    "bids":bids
        })
    
@login_required(login_url="login")
def delete_bid(request):
    if request.method == "POST":
        auction_id = request.POST["auction_id"]
        auction = Auction.objects.get(pk=auction_id)
        user = User.objects.get(pk=request.user.id)
        bid = Bid.objects.filter(owner=user, product=auction)
        bid.delete()
    return HttpResponseRedirect(reverse("bid"))


@login_required(login_url="login")
def close_deal(request):
    if request.method == "POST":
        user = User.objects.get(pk=request.user.id)
        auction_id = request.POST["auction_id"]
        auction = Auction.objects.get(pk=auction_id)
        if user == auction.seller:
            offers = Bid.objects.filter(product=auction)
            max_bid = 0
            if offers:
                for offer in offers:
                    if offer.bid>max_bid:
                        max_bid=offer.bid
                auction.closed = True
                auction.save()
                max_offer = Bid.objects.filter(product=auction, bid=max_bid).first()
                deal = Closed_Deals.objects.create(
                    deal_buyer=max_offer.owner,
                    deal_seller=user,
                    deal_product=auction,
                    deal_price=max_offer.bid
                )
                deal.save()
                offers.delete()
                return listing(request, auction.id) 
            else:
                return render(request, "auctions/404.html", {
                    "info":f"There is no offer"
                })

    else:
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/404.html", {
                    "info":f"Unkown Error"
                })


@login_required(login_url="login")
def deals(request):
    user = User.objects.get(pk=request.user.id)
    bought_deals = Closed_Deals.objects.filter(deal_buyer=user)
    sold_deals = Closed_Deals.objects.filter(deal_seller=user)
    return render(request, "auctions/deals.html", {
        "bought_deals":bought_deals,
        "sold_deals":sold_deals,
    })
   
def category(request, auction_category):

    category_choices = ["FSH","ELC","FOD","BVR","FNT","MDA"]

    if auction_category in category_choices:
        try:
            auctions = Auction.objects.filter(category=auction_category, closed=False)
        except:
            return  render(request, "auctions/404.html", {
                "info": f"{auction_category} Could not Found!!!"
            })
        return render(request, "auctions/category.html",{
                "auctions": auctions,
                "category": auction_category
            })
    else: 
        try:
            user = User.objects.get(username=auction_category)
        except User.DoesNotExist:
            return  render(request, "auctions/404.html", {
                "info": f"{auction_category} Could not Found!!!"
            })
        auctions = Auction.objects.filter(seller=user, closed=False)
        if auctions:
            return render(request, "auctions/category.html",{
                    "auctions": auctions,
                    "category": auction_category
                })
        return  render(request, "auctions/404.html", {
                "info": f"{auction_category} Could not Found!!!"
            })
    
@login_required(login_url="login")
def comment(request):
    if request.method == "POST":
        user = User.objects.get(pk=request.user.id)
        auction_id = request.POST["auction_id"]
        auction = Auction.objects.get(pk=auction_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data["comment_text"]
            comment = Comment.objects.create(
                comment_user = user,
                comment_product = auction,
                comment_text = text,
            )
            comment.save()
            return listing (request, auction_id)
        else:
            return render(request, "auctions/404.html", {
                "info":"There is problem about Your Comment"
            })   
    else:
        return HttpResponseRedirect(reverse("index"))