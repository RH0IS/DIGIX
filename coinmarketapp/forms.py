from django import forms

from coinmarketapp.models import CryptoCurrency, Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['crypto_currency', 'crypto_amount']
        widgets = {
            'crypto_currency': forms.Select(),
            'crypto_amount': forms.NumberInput(attrs={'min': 0.000001}),
        }

    email = forms.EmailField(required=True)

    def set(self, email=None, currency=None):
        self.fields['crypto_amount'].label = "Crypto Amount"
        self.fields['crypto_currency'].label = "Crypto Currency"
        self.fields['crypto_currency'].initial = currency
        self.fields['email'].label = "Email"
        self.fields['email'].initial = email


class RowSelectionForm(forms.Form):
    ROW_CHOICES = [
        (10, '10'),
        (20, '20'),
        (50, '50'),
    ]

    number_of_rows = forms.ChoiceField(choices=ROW_CHOICES, initial=10)
