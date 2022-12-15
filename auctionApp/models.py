from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class Item(models.Model):
    name = models.CharField(max_length=100)
    starting_price = models.FloatField(blank=False)
    description = models.CharField(max_length=250, blank=True)
    date_posted = models.DateField('Date Posted', auto_now=True)
    image = models.ImageField(upload_to='assets/', default="default.jpg")
    expiry_date = models.DateTimeField('Bid Expiry Date')
    user = models.ForeignKey("User", null=True, blank=True, related_name= "owns", on_delete=models.CASCADE)
    questions = models.ManyToManyField("QuestionAnswer")


    def __str__(self):
        return self.name

    def get_all_questions(self):
        qs =  [ q.to_dict() for q in self.questions.all()]
        print(qs)
        return qs


    def to_dict(self):
        return {
            'id':self.id,
            'name': self.name,
            'starting_price': self.starting_price,
            'description': self.description,
            'date_posted': self.date_posted,
            'image': self.image.url if self.image else None,
            'user': self.user.id,
            'owner': self.user.username,
            'expiry_date': self.expiry_date,
        }


class User(AbstractUser):

    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField( max_length=254 )
    date_of_birth = models.DateField('Date of Birth', auto_now=True, null=True)
    city = models.CharField(max_length=50)
    image = models.ImageField(upload_to='assets/', blank=True)



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
            'email': self.email,
            'date_of_birth': self.date_of_birth,
            'city': self.city,
            'image': self.image.url if self.image else None,
            'bids': [bid.to_dict() for bid in self.bids.all()],
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


class QuestionAnswer(models.Model):
    question = models.CharField(max_length=250, null=False)
    answer = models.CharField(max_length=250, blank=True)
    posted_by = models.ForeignKey(
        to=User,
        null=False,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.question

    def to_dict(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'posted_by': self.posted_by.id
        }
