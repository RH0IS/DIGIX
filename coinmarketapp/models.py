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



class Order(models.Model):
    # user information
    user_id = models.CharField(max_length=50)
    email = models.EmailField()
    # payment information that Stripe returns
    payment_intent = models.CharField(max_length=50)
    clientSecret = models.CharField(max_length=50)
    # what user bought
    crypto_currency = models.ForeignKey(CryptoCurrency, on_delete=models.PROTECT)
    crypto_amount = models.DecimalField(max_digits=10, decimal_places=6)
    # what user paid
    amount = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True, default=None )
    currency = models.CharField(max_length=10)
    # order information
    created = models.DateTimeField(auto_now_add=True)
    order_status = models.IntegerField(default=0,
                                       choices=[(-1, 'Refunded'), (0, 'Created'), (1, 'paid'), (2, 'Completed'),
                                                (3, 'Cancelled')])

    def __str__(self):
        return self.user_id + ': ' + self.payment_intent + '(' + str(self.order_status) + ')'




class UserWallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currencies = models.ManyToManyField(CryptoCurrency)
    amount = models.DecimalField(max_digits=12, decimal_places=6)

    def __str__(self):
        return self.user.username + "'s Wallet"

