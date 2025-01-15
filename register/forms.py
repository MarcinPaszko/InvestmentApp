# register/forms.py

from django import forms
from .models import Stock

class StockAddForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['asset', 'num_shares', 'purchase_price', 'trade_date', 'currency_code']
