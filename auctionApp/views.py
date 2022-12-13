from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse, Http404, HttpResponseBadRequest
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, SignupForm
from .models import User, Item, BidDetails
import json
from django.db.models import Q
from datetime import datetime


# @login_required
def index(request: HttpRequest) -> HttpResponse:
    """
    Initial index url path will route here
    """
    title = "test"
    return render(request, "auctionApp/pages/index.html", {
        'title': title,
    })


# @login_required
def items_api(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        return JsonResponse({
            'items': [
                item.to_dict() for item in Item.objects.all()
            ]
        })

    return HttpResponseBadRequest("Invalid method request")


@login_required
def create_item_api(request: HttpRequest) -> JsonResponse:
    if request.method == 'POST':
        body_unicode = request.body.decode('utf8')
        body = json.loads(body_unicode)

        name =  body['name']
        price = body['price']
        description = body['description']
        # image = body['image']
        expiry_date = body['expiry_date']

        newItem = Item.objects.create (
            name = name,
            starting_price = price,
            description = description,
            expiry_date = expiry_date,
        )

        return JsonResponse(newItem.to_dict())
    return HttpResponseBadRequest("Invalid method request")


def search(request: HttpRequest, search_input: str) -> JsonResponse:
    if request.method == "GET":
        items = Item.objects.filter(
            Q(description__contains=search_input) |
            Q(name__contains=search_input)
        )
        return JsonResponse({
                'items': [
                    item.to_dict() for item in items
                ]
            })


def make_bid(request: HttpRequest) -> JsonResponse:
    if request.method == 'PUT':
        bid_data = json.loads(request.body)
        # print(bid_data['item_id'])
        
        item_id = bid_data['item_id']
        amount = bid_data['amount']
        user_id = bid_data['user_id']
        
        user = User.objects.get(id=user_id)
        item = Item.objects.get(id=item_id)

        bids = BidDetails.objects.filter(item__id=item_id)
        bid = None
        # print(bids[0].amount)
        if bids:
            highest_amount = bids[0].amount
            if amount > highest_amount:
                # post       
                bid = get_object_or_404(BidDetails, id=bids[0].id)     
                bid.item = item
                bid.user = user
                bid.amount = amount
                bid.time = datetime.now()
                # bids[0].save()
                bid.save()
            else:
                return JsonResponse({'message': 'Sorry, you cannot bid under the current price.'})
        else:
            starting_price = item.starting_price
            if amount > starting_price:
                bid = BidDetails.objects.create(
                    user = user,
                    item = item,
                    time = datetime.now(),
                    amount = amount,
                )
            else:
                return JsonResponse({'message': 'Sorry, you cannot bid under the current price.'})

        return JsonResponse(bid.to_dict())

    return HttpResponseBadRequest("Invalid request method")



def item_api(request: HttpRequest, item_id: int) -> JsonResponse:
    """
    Edits the series, or deletes, or gets, based on request
    """
    item = get_object_or_404(Item, id=item_id)

    # if request.method == 'PUT':
    #     data = json.loads(request.body)
    #     series.series_title = data['serie_title']
    #     series.release_date = data['release_date']
    #     series.has_ended = data['has_ended']
    #     series.number_of_seasons = data['number_of_seasons']
    #     series.save()
    #     return JsonResponse({})

    # if request.method == 'DELETE':
    #     series.delete()
    #     return JsonResponse({})

    if request.method == 'GET':
        return JsonResponse({
            'item': 
                # item.to_dict() for item in Item.objects.all()
                # Item.objects.get(item_id)
                item.to_dict()
            
        })
    return HttpResponseBadRequest("Invalid method request")



def signup_view(request):
    '''
    Signup function
    Users creating an account
    '''

    form = SignupForm()

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']

            if not username:
                form.add_error('username', 'Please choose a username')
                return render(request, 'auctionApp/auth/signup.html', {'form': form})

            if User.objects.filter(username=username).exists():
                form.add_error('username', 'Username already exists')
                return render(request, 'auctionApp/auth/signup.html', {'form': form})

            if form.cleaned_data['password'] != form.cleaned_data['password_confirm']:
                form.add_error('password', 'Passwords to not match')
                form.add_error('password_confirm', 'Passwords to not match')
                return render(request, 'auctionApp/auth/signup.html', {'form': form})

            password = form.cleaned_data['password']
            # create a new user
            new_user = User.objects.create(username=username)
            # set user's password
            new_user.set_password(password)
            new_user.save()
            # authenticate user
            # establishes a session, will add user object as attribute
            # on request objects, for all subsequent requests until logout
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('auctionApp:home')

    return render(request, 'auctionApp/auth/signup.html', {'form': SignupForm})


def login_view(request):
    '''
    Login function
    Users logging into the app
    '''

    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('http://localhost:8001/')

            # failed authentication
            form.add_error('username', 'Invalid credentials')
            form.add_error('password', 'Invalid credentials')
            return render(request, 'auctionApp/auth/login.html', {'form': form})

    return render(request, 'auctionApp/auth/login.html', {'form': form})


@login_required
def logout_view(request):
    '''
    Once users logout they are redirected to login page
    '''

    auth.logout(request)
    return redirect('auctionApp:login')


def check_user_authenticated(request):
    if request.method == 'GET':
        print(request)
        if request.user.is_authenticated:
            return JsonResponse({
                'user_id': request.user.id
            })
        return HttpResponse("Unauthourised", status=401)

