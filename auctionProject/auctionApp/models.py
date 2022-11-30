from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):

    username = models.CharField(max_length=50, unique=True)
    date_of_birth =  models.DateField('Date of Birth')
    city = models.CharField(max_length=50, unique=False, blank=True)
    image = models.ImageField(upload_to='profile_picture', blank=True)


    bids = models.ManyToManyField(
        # to='self', ASKPAULO
        blank=True,
        symmetrical=True,
        related_name='bid',
    )


    REQUIRED_FIELDS = []


    def __str__(self):
        return self.username


    def to_dict(self):
        return {
            'username': self.username,
            'date_of_birth': self.date_of_birth,
            'city': self.city,
            'image': self.image.url if self.image else None,
            'bids': [bid.to_dict() for bid in self.bids]
        }


class Bid(models.Model):
    amount = models.FloatField()
    time = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)


    def __str__(self):
        return self.item.name
        # see if above worksASK PAULO


    def to_dict(self):
        return {
            'amount': self.amount,
            'time': self.time,
            'user': self.user.to_dict() if self.user else None,
            'item': self.item.to_dict() if self.item else None,
        }


class Item(models.Model):
    name = models.CharField()
    starting_price = models.FloatField(blank=False)
    description = models.CharField(max_length=250, blank=True)
    date_posted =  models.DateField('Date Posted')
    image =models.ImageField(blank=True)
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    bids = models.ManyToManyField(
        # to='self', ASKPAULO
        blank=True,
        symmetrical=True,
        related_name='bid',
    )
    questions = models.ManyToManyField(
        # to='self', ASKPAULO
        blank=True,
        symmetrical=True,
        related_name='questions',
    )


    def __str__(self):
        return self.name


    def to_dict(self):
        return {
            'name': self.name,
            'starting_price': self.starting_price,
            'description': self.description,
            'date_posted': self.date_posted,
            'image': self.image.url if self.image else None,
            'user': self.user.to_dict() if self.user else None,
            'bids': [bid.to_dict() for bid in self.bids],
            'questions': [questions.to_dict() for question in self.questions],
        }

class Question(models.Model):
    text = models.CharField(max_length='250')
    time = models.DateTimeField(default=timezone.now)
    user= models.ForeignKey(
        to=User,
        related_name='posted',
        on_delete=models.CASCADE
    )
    item = models.ForeignKey(
        to=Item,
        related_name='for',
        on_delete=models.CASCADE
    )
    answers = models.ManyToManyField(
        # to='self', ASKPAULO
        blank=True,
        symmetrical=True,
        related_name='questions',
    )


     def __str__(self):
        return self.text


    def to_dict(self):
        return {
            'text': self.text,
            'time': self.time
            'user': self.user.to_dict() if self.user else None,
            'answers': [answer.to_dict() for answer in self.answers],
        }


class Answer(models.Model):
    text = models.CharField(max_length='250')
    time = models.DateTimeField(default=timezone.now)
    user= models.ForeignKey(
        to= User,
        related_name='answered_by',
        on_delete=models.CASCADE
    )
    question = models.ForeignKey(
        to= Question,
        related_name='related_to',
        on_delete=models.CASCADE
    )


     def __str__(self):
        return self.text


    def to_dict(self):
        return {
            'text': self.text,
            'time': self.time
            'user': self.user.to_dict() if self.user else None,
        }


