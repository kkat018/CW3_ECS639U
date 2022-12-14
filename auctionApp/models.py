from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class Item(models.Model):
    name = models.CharField(max_length=100)
    starting_price = models.FloatField(blank=False)
    description = models.CharField(max_length=250, blank=True)
    date_posted = models.DateField('Date Posted', auto_now=True)
    image = models.ImageField(blank=True)
    user = models.ForeignKey("User", null=True, blank=True, related_name= "owns", on_delete=models.CASCADE)
    expiry_date = models.DateTimeField('Bid Expiry Date')

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            'id':self.id,
            'name': self.name,
            'starting_price': self.starting_price,
            'description': self.description,
            'date_posted': self.date_posted,
            'image': self.image.url if self.image else None,
            'user': self.user.id if self.user else None,
            'owner': self.user.username if self.user else None,
            'expiry_date': self.expiry_date,
        }


class User(AbstractUser):

    username = models.CharField(max_length=50, unique=True)
    date_of_birth = models.DateField('Date of Birth', null=True, blank=True)
    city = models.CharField(max_length=50, unique=False, blank=True)
    image = models.ImageField(upload_to='profile_picture', blank=True)

    questions = models.ManyToManyField(
        to=Item,
        blank=True,
        symmetrical=False,
        through = "QuestionDetails",
        related_name='question_of_user',
    )
# one bid many user???
    bids = models.ManyToManyField(
        to=Item,
        blank=True,
        symmetrical=False,
        through = "BidDetails",
        related_name='bid_by_user',
    )


    REQUIRED_FIELDS = []


    def __str__(self):
        return self.username


    def to_dict(self):
        return {
            'id':self.id,
            'username': self.username,
            'date_of_birth': self.date_of_birth,
            'city': self.city,
            'image': self.image.url if self.image else None,
            'bids': [bid.to_dict() for bid in self.bids.all()],
            'questions': [question.to_dict() for question in self.questions.all()],
        }


class BidDetails(models.Model):
    user = models.ForeignKey(User, related_name= "user_details_for_bid", on_delete=models.CASCADE)
    item = models.ForeignKey(Item, related_name="item_bid_on", on_delete=models.CASCADE)
    amount = models.FloatField()
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.item.name
        # see if above worksASK PAULO


    def to_dict(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'time': self.time,
            'user': self.user.to_dict() if self.user else None,
            'item': self.item.to_dict() if self.item else None,
        }


# keep two models for questions and answers so you can distinguish. make sure
#  item owner is the one who is answering the quesiton for the item
# questions and answers have one to one relationship
class QuestionDetails(models.Model):
    text = models.CharField(max_length=250)
    time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        to=User,
        related_name='sender',
        on_delete=models.CASCADE
    )
    item = models.ForeignKey(
        to=Item,
        related_name='question_for_item',
        on_delete=models.CASCADE
    )


    def __str__(self):
        return self.text


    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'time': self.time,
            'user': self.user.to_dict() if self.user else None,
            'item': self.item.to_dict() if self.item else None,
        }


class AnswerDetails(models.Model):
    text = models.CharField(max_length=250)
    time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        to= User,
        related_name='answered_by',
        on_delete=models.CASCADE
    )
    question = models.OneToOneField(
        to=QuestionDetails,
        related_name='related_to_question',
        on_delete=models.CASCADE
    )


    def __str__(self):
        return self.text


    def to_dict(self):
        return {
            'id':self.id,
            'text': self.text,
            'time': self.time,
            'user': self.user.to_dict() if self.user else None,
            'question': self.question.to_dict() if self.question else None,
        }


