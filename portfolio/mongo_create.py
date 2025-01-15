# models.py
from djongo import models, setup
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
setup()

class StockData(models.Model):
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    price = models.FloatField()
    volume = models.IntegerField()
    latest_trading_day = models.DateField()
    previous_close = models.FloatField()
    change = models.FloatField()
    change_percent = models.FloatField()

    class Meta:
        abstract = True
