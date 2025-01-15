from django.contrib import admin
from .models import StockData, Profile, StockOwnership, Stock

admin.site.register(StockData)
admin.site.register(Profile)
admin.site.register(StockOwnership)
admin.site.register(Stock)
