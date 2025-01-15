from django.db import models
from django.contrib.auth.models import User
import json




class StockData(models.Model):
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=255)
    closing_price = models.DecimalField(max_digits=10, decimal_places=2)
    # Add other fields as needed

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Remove the owned_stocks field from here

class StockOwnership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)  # Add a foreign key to Profile
    stock = models.ForeignKey(StockData, on_delete=models.CASCADE)
    num_shares = models.PositiveIntegerField()
    buying_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.stock} - {self.user.username}"

class Stock(models.Model):
    asset = models.CharField(max_length=50)
    num_shares = models.IntegerField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    trade_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Assuming you have a User model imported from django.contrib.auth.models
    currency_code = models.CharField(max_length=3)  # Add the currency code field
    latest_closing_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Add this field

    def cost_of_investment(self):
        return self.num_shares * self.purchase_price

    def current_market_value(self):
        if self.latest_closing_price is not None:
            return self.num_shares * self.latest_closing_price
        else:
            return 'N/A'

    def gain_loss(self):
        if self.latest_closing_price is not None:
            return self.current_market_value() - self.cost_of_investment()
        else:
            return 'N/A'

class Price(models.Model):
    symbol = models.CharField(max_length=10)
    closing_price = models.FloatField()
    volume_weighted = models.FloatField()
    open_price = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()
    timestamp = models.BigIntegerField()
    num_trades = models.IntegerField()

class StockDataProcessor:
    @staticmethod
    def fetch_stock_data():
        # Fetch data for stocks from the database or API
        stocks = Stock.objects.all()

        # Initialize an empty list to store stock data
        stock_data = []

        # Iterate over fetched stocks and create data for each stock
        for stock in stocks:
            trade_dates = []
            closing_prices = []

            # Fetch associated stock data for the current stock
            stock_data_instances = stock.stockdata_set.all()

            # Extract trade dates and closing prices from the StockData instances
            for stock_data_instance in stock_data_instances:
                trade_dates.append(stock_data_instance.trade_date.strftime('%b. %d, %Y'))
                closing_prices.append(stock_data_instance.closing_price)

            stock_info = {
                'labels': trade_dates,
                'data': closing_prices,
                'borderColor': 'green',  # Example border color, replace with your logic
                'label': stock.name  # Assuming 'name' is a field in your Stock model
            }
            # Append the stock info to the list
            stock_data.append(stock_info)

        # Convert data to JSON format
        json_stock_data = json.dumps(stock_data)

        # Print the JSON data to verify in the console
        print("JSON Stock Data:", json_stock_data)

        return json_stock_data
