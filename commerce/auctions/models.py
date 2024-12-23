from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Auction (models.Model):
    fashion = "FSH"
    electronics = "ELC"
    food = "FOD"
    beverages = "BVR"
    furniture = "FNT"
    media = "MDA"

    category_choices = {
        (fashion, 'Fashion'),
        (electronics, 'Electronics'),
        (food, 'Food'),
        (beverages, 'Beverages'),
        (furniture, 'Furniture'),
        (media, 'Media')
    }

    id = models.BigAutoField(primary_key=True)
    category = models.CharField(max_length=3, choices=category_choices, default=fashion)
    seller = models.ForeignKey(User ,on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=64, default="")
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False, default=0.00)
    image = models.URLField(max_length=200, blank=True)
    date = models.DateField(auto_now=True)
    closed = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f"{self.title}"
    
class Watchlist(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    item = models.ManyToManyField(Auction, related_name="item")
    
    def __str__(self) -> str:
        return f"{self.user}"
    
class Bid(models.Model):
    id = models.BigAutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    product = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="procuct")
    bid = models.DecimalField(max_digits=11, decimal_places=2)
    date = models.DateField(auto_now=True)
    
    def __str__(self) -> str:
        return f"{self.id}"
    
class Closed_Deals(models.Model):
    id = models.BigAutoField(primary_key=True)
    deal_buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="deal_buyer")
    deal_seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="deal_seller")
    deal_product = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="deal_product")
    deal_price = models.DecimalField(max_digits=11, decimal_places=2)
    date = models.DateField(auto_now=True)
    
    def __str__(self) -> str:
        return f"{self.deal_buyer}"
    
class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_user")
    comment_product = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="comment_product")
    comment_text = models.TextField(blank=False)
    comment_date = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.comment_product.title}"

