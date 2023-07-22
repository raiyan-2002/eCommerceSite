from django.contrib.auth.models import AbstractUser
from django.db import models

from . import *

class User(AbstractUser):

    user_id = models.AutoField(primary_key=True, editable=False)
    def __str__(self):
        return f"{self.username}"

class Category(models.Model):
    category_id = models.AutoField(primary_key=True, editable=False)
    type = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.type}"

class Listing(models.Model):
    listing_id = models.AutoField(primary_key=True, editable=False)
    title = models.CharField(max_length=100, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False )
    time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField(max_length = 10000, null=True, blank=True)
    image = models.CharField(max_length=1000, null=True, blank=True)
    active = models.BooleanField(default=True)
    watchers = models.ManyToManyField(User, blank=True, related_name="watchlisters")
    winner = models.ForeignKey(User, blank=True, null = True, on_delete=models.CASCADE, related_name="winner1")
    
    def __str__(self):
        return f"{self.title}: {self.price} by {self.user}"

class Bid(models.Model):
    bid_id = models.AutoField(primary_key=True, editable=False)
    time = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="allbids", default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.user}: {self.amount} on {self.listing.title}"
    

class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True, editable=False)
    time = models.DateTimeField(auto_now=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="allcomments", default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length = 10000, default="comment text")

    def __str__(self):
        return f"{self.user}: {self.description} on {self.listing.title}"
    

