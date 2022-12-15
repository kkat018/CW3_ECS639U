from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse, Http404, HttpResponseBadRequest
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, SignupForm
from .models import User, Item, BidDetails, QuestionAnswer
import json
from django.db.models import Q
from datetime import datetime
from django.core.mail import BadHeaderError, send_mail

# def send_email(request):
#     subject = 'You won the Bid!'
#     message = 'Follow the link to pay now.'
#     from_email = 'group50.middleeast@gmail.com',
#     if subject and message and from_email:
#         try:
#             send_mail(subject, message, from_email, ['durrao.brien@gmail.com'])
#         except BadHeaderError:
#             return HttpResponse('Invalid header found.')
#         return HttpResponseRedirect('/')
#     else:
#         return HttpResponse('Make sure all fields are entered and valid.')

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

def add_question(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf8')
        body = json.loads(body_unicode)

        user_id = body['user_id']
        user = get_object_or_404(User, id=user_id)

        item_id = body['item_id']
        item = get_object_or_404(Item, id=item_id)

        print("TEST")
        print(item)

        newQuestionAnswer = QuestionAnswer.objects.create(
           question = body['question'],
           posted_by = user,
        )
        newQuestionAnswer.save()
        print(newQuestionAnswer.id)
        print('id above')

        item.questions.add(newQuestionAnswer)
        item.save()

        return JsonResponse(item.to_dict())

def get_pending_questions(request, item_id: int):

    item = get_object_or_404(Item, id=item_id)
    print(item.get_all_questions())
    # return JsonResponse( [item.get_all_questions()])
    return JsonResponse({
            'questions': [ item.get_all_questions()]
        })

def get_all_users(request):
    return JsonResponse({
        'users': [ user.to_dict() for user in User.objects.all() ]
    })

# def user_is_superuser(request, user_id: int):
#     user = get_object_or_404(User, id=user_id)
#     print(user.is_superuser)
#     return JsonResponse( {'superuser' : user.is_superuser} )

def add_answer(request):
    body_unicode = request.body.decode('utf8')
    body = json.loads(body_unicode)

    question_id = body['question_id']
    question = get_object_or_404(QuestionAnswer, id=question_id)
    question.answer = body['answer']
    question.save()

    print(question.answer)
    # return JsonResponse( { 'questionAnswer': question.to_dict() })
    return JsonResponse( question.to_dict() )




