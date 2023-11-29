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
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=False)
    currency = models.ForeignKey(CryptoCurrency, on_delete=models.CASCADE, unique=False)
    amount = models.DecimalField(max_digits=12, decimal_places=6, default=0.0)

    def __str__(self):
        return self.user.username + "'s Wallet"


class Order(models.Model):
    REFUNDED = -1
    CREATED = 0
    PAID = 1
    COMPLETED = 2
    CANCELLED = 3
    SOLD = 11
    id = models.BigAutoField(primary_key=True, auto_created=True)
    # user information
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=False, default=1)
    email = models.EmailField()
    # payment information that Stripe returns
    payment_intent = models.CharField(max_length=50, default="")
    clientSecret = models.CharField(max_length=50, default="")
    # what user bought
    crypto_currency = models.ForeignKey(CryptoCurrency, on_delete=models.PROTECT)
    crypto_amount = models.DecimalField(max_digits=10, decimal_places=6)
    # what user paid
    amount = models.PositiveIntegerField(default=1)  # in cents not dollars
    currency = models.CharField(max_length=10, default="")
    card_number = models.CharField(max_length=19, default="")
    # order information
    created = models.DateTimeField(auto_now_add=True)
    order_status = models.IntegerField(
        default=0,
        choices=[
            (REFUNDED, "Refunded"),
            (CREATED, "Created"),
            (PAID, "Paid"),
            (COMPLETED, "Completed"),
            (CANCELLED, "Cancelled"),
            (SOLD, "Sold"),
        ],
    )

    def __str__(self):
        return (
            str(self.user.id)
            + " (use "
            + str(self.amount)
            + str(self.currency)
            + " to buy "
            + str(self.crypto_amount)
            + " "
            + str(self.crypto_currency.symbol)
            + ")"
        )


class trending_crypto(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    rank = models.IntegerField()
    image = models.ImageField(
        upload_to="crypto_images/"
    )  # Change 'crypto_images/' to your desired upload path
    price = models.DecimalField(decimal_places=2, max_digits=12, default=0)
    price_change_percentage_24h = models.DecimalField(decimal_places=2, max_digits=12)

    def __str__(self):
        return self.name
