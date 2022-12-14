from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse, Http404, HttpResponseBadRequest
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, SignupForm
from .models import QuestionDetails, User, Item
import json
from django.core import serializers
# from django.contrib.auth.models import User


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
            'item': [
                # item.to_dict() for item in Item.objects.all()
                # Item.objects.get(item_id)
                item.to_dict()
            ]
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


def add_question(request):
    print("checkk1")
    if request.method == 'POST':
        body = json.loads(request.body)
        user = get_curr_user(body['user_id'])
        item = body['item']
        item_ = Item.objects.get(id=item[0]['id'])
        question = QuestionDetails.objects.create(
            text = body['text'],
            user= user,
            item = item_
        )
        question.save()
    return JsonResponse({})


def render_questions(request: HttpRequest, item_id : int ):
    if request.method == 'GET':
        item = Item.objects.get(id=item_id)
        questions = QuestionDetails.objects.filter(item=item)
        qs_json = serializers.serialize('json', questions)
        return HttpResponse(qs_json, content_type='application/json')


def get_curr_user(id):
    return User.objects.get(pk=id)
