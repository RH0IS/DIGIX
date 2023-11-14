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

    
class RowSelectionForm(forms.Form):
    ROW_CHOICES = [
        (10, '10'),
        (20, '20'),
        (50, '50'),
    ]

    number_of_rows = forms.ChoiceField(choices=ROW_CHOICES, initial=10)

    
