from django import forms

class RowSelectionForm(forms.Form):
    ROW_CHOICES = [
        (10, '10'),
        (20, '20'),
        (50, '50'),
    ]

    number_of_rows = forms.ChoiceField(choices=ROW_CHOICES, initial=10)