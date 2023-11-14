from django import forms

from coinmarketapp.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['crypto_amount', 'crypto_currency']
        weidgets = {
            'crypto_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Amount'}),
            'crypto_currency': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Currency'}),
        }

    email = forms.EmailField(required=True)
