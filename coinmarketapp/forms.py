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
        if currency is not None:
            self.fields['crypto_currency'].initial = currency
        self.fields['email'].label = "Email"
        if email is not None:
            self.fields['email'].initial = email


class RowSelectionForm(forms.Form):
    ROW_CHOICES = [
        (10, '10'),
        (20, '20'),
        (50, '50'),
    ]

    number_of_rows = forms.ChoiceField(choices=ROW_CHOICES, initial=10)


class ChangeProfilePictureForm(forms.Form):
    new_profile_picture = forms.ImageField(label='New Profile Picture')


class SellForm(forms.Form):
    wallet_id = forms.CharField(widget=forms.HiddenInput(), disabled=True, initial=1)
    price = forms.DecimalField(widget=forms.HiddenInput(), disabled=True, initial=1)
    crypto_currency_name = forms.CharField(label='Crypto Currency', initial="", disabled=True, required=False)
    crypto_amount = forms.DecimalField(label='Crypto Amount', min_value=0.000001, max_digits=10, decimal_places=6,
                                       widget=forms.NumberInput())
    email = forms.EmailField(label='Email')
    card_number = forms.CharField(label='Card Number', max_length=19)

    def set(self, email=None, currency=None, wallet_id=None, price=None, max_amount=None):
        if currency is not None:
            self.fields['crypto_currency_name'].initial = currency
        if email is not None:
            self.fields['email'].initial = email
        if wallet_id is not None:
            self.fields['wallet_id'].initial = wallet_id
        if price is not None:
            self.fields['price'].initial = price
        if max_amount is not None:
            self.fields['crypto_amount'].widget = forms.NumberInput(
                attrs={'min': 0.000001, 'max': max_amount, 'step': 0.000001,'onchange': 'showPriceChanges()'})
            self.fields['crypto_amount'].label = "Crypto Amount (Max: " + str(max_amount) + ")"
