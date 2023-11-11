# coinmarketapp/models.py
from django.contrib.auth.models import User
from django.db import models

class CryptoCurrency(models.Model):
    name = models.CharField(max_length=100)
    id = models.AutoField(primary_key=True)
    symbol = models.CharField(max_length=10)
    market_cap = models.DecimalField(max_digits=20, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    volume_24h = models.DecimalField(max_digits=15, decimal_places=2)
    quantity = models.DecimalField(max_digits=15, decimal_places=4, default=0)

    def __str__(self):
        return self.name



class UserWallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currencies = models.ManyToManyField(CryptoCurrency)

    def __str__(self):
        return f"{self.user.username}'s Wallet"