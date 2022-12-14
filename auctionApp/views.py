from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse, Http404, HttpResponseBadRequest
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, SignupForm
from .models import User, Item
import json



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


# @login_required
def create_item_api(request: HttpRequest) -> JsonResponse:
    if request.method == "POST":
        # Create a new item in the database
        print(request.body)
        newItem = Item.objects.create(
            name = request.POST['name'],
            description = request.POST['description'],
            starting_price = request.POST['price'],
            expiry_date = request.POST['date'],
            user = User.objects.get(id=request.POST['user_id'])
        )

        # Check if an image was uploaded
        if 'image' in request.FILES:
            # Set the image to the image uploaded
            newItem.image = request.FILES['image']

        # Save the new item to the database
        newItem.save()

        # Return the new item
        return JsonResponse(newItem.to_dict())





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
            # username validation 
            username = form.cleaned_data['username']

            if not username:
                form.add_error('username', 'Please choose a username')
                return render(request, 'auctionApp/auth/signup.html', {'form': form})

            if User.objects.filter(username=username).exists():
                form.add_error('username', 'Username already exists')
                return render(request, 'auctionApp/auth/signup.html', {'form': form})

            # password validation
            if form.cleaned_data['password'] != form.cleaned_data['password_confirm']:
                form.add_error('password', 'Passwords to not match')
                form.add_error('password_confirm', 'Passwords to not match')
                return render(request, 'auctionApp/auth/signup.html', {'form': form})

            password = form.cleaned_data['password']

            #email validation
            email = form.cleaned_data['email']
            if not email:
                form.add_error('email', 'Please provide an email')
                return render(request, 'auctionApp/auth/signup.html', {'form': form})

            #city validation
            city = form.cleaned_data['city']
            if not city:
                form.add_error('city', 'Please provide a city')
                return render(request, 'auctionApp/auth/signup.html', {'form': form})

            # date of birth validation
            date_of_birth = form.cleaned_data['date_of_birth']
            if not date_of_birth:
                form.add_error('date_of_birth', 'Please provide a date of birth')
                return render(request, 'auctionApp/auth/signup.html', {'form': form})

            # create a new user
            new_user = User.objects.create(username=username)
            # set user's details
            new_user.set_password(password)
            new_user.city = city
            new_user.email = email
            new_user.date_of_birth = date_of_birth
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
    '''
    Checks if user is authenticated -- returns user details as a dictionary if they are
    '''
    if request.method == 'GET':
        if request.user.is_authenticated:
            return JsonResponse(request.user.to_dict())
        return HttpResponse("Unauthourised", status=401)

def profile_api(request):
    '''
    This method is responsible for handling edit requests for the Profile API:

    PUT - For editing user (profile) details
    POST - For editing image of user
    '''

    if request.method == 'PUT':

        body_unicode = request.body.decode('utf8')
        body = json.loads(body_unicode)

        user_id = body['id']
        user = get_object_or_404(User, id=user_id)

        user.username = body['username'];
        user.email = body['email'];
        user.date_of_birth = body['date_of_birth'];
        user.city = body['city'];
        user.save()

        return JsonResponse( user.to_dict())

    if request.method == 'POST':
        # Check if an image was uploaded
        if 'image' in request.FILES:

            #Get user to update their image
            user = User.objects.get(id=request.POST['user_id'])

            # Set the image to the image uploaded
            user.image = request.FILES['image']
            user.save()
            return JsonResponse( user.to_dict())
