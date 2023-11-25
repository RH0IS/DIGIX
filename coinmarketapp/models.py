# coinmarketapp/models.py
from django.contrib.auth.models import User
from django.db import models

class CryptoCurrency(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    market_cap = models.DecimalField(max_digits=20, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    volume_24h = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return self.name




class UserWallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currencies = models.ManyToManyField(CryptoCurrency)

    def __str__(self):
        return self.user.username + "'s Wallet"

class trending_crypto(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    rank = models.IntegerField()
    image = models.ImageField(upload_to='crypto_images/')  # Change 'crypto_images/' to your desired upload path
    price = models.DecimalField(decimal_places=2,max_digits=12,default=0)
    price_change_percentage_24h = models.DecimalField(decimal_places=2, max_digits=12)

    def __str__(self):
        return self.name