from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"

    def cat_title_to_url(self):
        return self.name.replace(' ', '-')

class Auction(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category_auction")
    price = models.DecimalField(max_digits=12, decimal_places=2)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.URLField()
    active = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField()

    def __str__(self):
        return f"({self.id}) {self.title}, {self.category}, {self.price}"

    def title_to_url(self):
        return self.title.replace(' ', '-')

class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bid_item")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="buyer")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}, {self.auction.id}, ${self.amount}, {self.user}"

class Watchlist(models.Model):
    auction_item = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="auction_item")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.id}, {self.auction_item}, {self.auction_item.title}, {self.user}"

class Comment(models.Model):
    auction_item = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="item_id")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.auction_item}, {self.user}, {self.comment}"

class NotificationMsg(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction_item = models.ForeignKey(Auction, on_delete=models.CASCADE)
    message = models.TextField()
    read = models.BooleanField(default=False)
    is_status = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}, {self.auction_item}, {self.message}, {self.read}, {self.is_status}, {self.create_date}"



