
import os
import json
import glob
import requests
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Profile, Stock
from .forms import StockAddForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.db.models import F
from datetime import datetime, timedelta, date
from django.utils.dateparse import parse_date
import logging
from decimal import Decimal
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from decimal import Decimal
from django.utils import timezone
from io import StringIO
import sys


def stock_graph_view(request):
    return render(request, 'register/stock_graph.html')



@login_required
def profile(request):
    user = request.user
    stock_list = Stock.objects.filter(user=user)

    # Fetch the latest closing prices for each asset symbol and update stock instances
    for stock in stock_list:
        latest_price = get_latest_closing_price(stock.asset)
        stock.latest_closing_price = latest_price
        stock.save()  # Save the updated stock instance with the latest closing price

    # Refresh the stock list to include the latest closing prices
    stock_list = Stock.objects.filter(user=user)

    return render(request, 'register/profile.html', {'user': user, 'stock_list': stock_list})


def stock_add(request):
    json_file_path = os.path.join(settings.BASE_DIR, 'portfolio', 'assets_list.json')

    if request.method == 'POST':
        try:
            # Decode the JSON data from the request body
            data = json.loads(request.body.decode('utf-8'))

            # Create a form instance with the decoded data
            form = StockAddForm(data)

            if form.is_valid():
                stock = form.save(commit=False)
                stock.user = request.user
                stock.save()

                # Get the user's saved stocks
                user_profile = Profile.objects.get_or_create(user=request.user)[0]
                stock_ownership_list = user_profile.stockownership_set.all()

                # Load assets from JSON file
                with open(json_file_path, 'r') as file:
                    assets_list = json.load(file)

                # Return a JSON response with success status and updated data
                response_data = {
                    'status': 'success',
                    'assets_list': assets_list,
                    'stock_ownership_list': [{'asset': s.asset, 'num_shares': s.num_shares, 'purchase_price': s.purchase_price} for s in stock_ownership_list]
                }

                return JsonResponse(response_data)
            else:
                # Return a JSON response with validation errors
                return JsonResponse({'status': 'error', 'message': 'Invalid form data', 'errors': form.errors.as_json()}, status=400)

        except json.JSONDecodeError as e:
            # Handle JSON decoding error
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data', 'errors': str(e)}, status=400)

    else:
        form = StockAddForm()

    # Load assets from JSON file
    with open(json_file_path, 'r') as file:
        assets_list = json.load(file)

    # Get the user's saved stocks
    user_profile = Profile.objects.get_or_create(user=request.user)[0]
    stock_ownership_list = user_profile.stockownership_set.all()

    return render(request, 'stock_add.html', {'form': form, 'assets_list': assets_list, 'stock_ownership_list': stock_ownership_list})


def custom_login(request, **kwargs):
    response = LoginView.as_view(template_name='register/login.html')(request, **kwargs)
    if request.method == 'POST' and response.status_code == 302:
        # Redirect to the profile page upon successful login
        return redirect('register:profile')
    return response



def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'register/register.html', {'form': form})



def get_latest_closing_price(asset_symbol):
    stock_data_path = os.path.join(settings.BASE_DIR, 'portfolio', 'stock_data')

    # Get all files in the directory
    files = os.listdir(stock_data_path)

    # Sort files based on filename in descending order
    sorted_files = sorted(files, key=lambda x: x.lower(), reverse=True)

    # Find the first file with the correct extension and extract date from the filename
    for filename in sorted_files:
        if filename.lower().endswith(".json"):
            # Extract date and symbol from the filename
            parts = filename.lower().split("_")
            if len(parts) >= 4:
                date_str = parts[-3]  # Assuming the date is at the third-to-last position
                file_path = os.path.join(stock_data_path, filename)

                print(f"Latest File for {asset_symbol} (Date: {date_str}): {file_path}")

                # Read JSON data from the file
                with open(file_path, 'r') as file:
                    data = json.load(file)

                # Extract and return the closing price for the asset
                closing_price = data.get(asset_symbol, {}).get('closing_price', 'N/A')

                print(f"Closing price for {asset_symbol}: {closing_price}")  # Add this line for debugging

                return closing_price

    # If no matching files are found
    print(f"No matching files found for symbol: {asset_symbol}")
    return 'N/A'


def exchangerates(request):
    api_url = "https://api.currencybeacon.com/v1/latest?api_key=WFyLL2mc6CUPYA2OjH4J0g5NrcVmHbMZ"
    response = requests.get(api_url)
    data = response.json()

    rates = data["response"]["rates"]

    if request.method == 'POST':
        from_currency = request.POST.get('from_currency')
        to_currency = request.POST.get('to_currency')
        amount = float(request.POST.get('amount', 0))

        if from_currency and to_currency and amount:
            exchange_rate = rates.get(to_currency, 1) / rates.get(from_currency, 1)
            converted_amount = round(amount * exchange_rate, 2)

            result = {
                'amount': converted_amount,
                'to_currency': to_currency,
            }

            context = {
                "date": data["response"]["date"],
                "base": data["response"]["base"],
                "exchange_rates": rates,
                "result": result,
            }

            return render(request, "register/exchangerates.html", context)

    context = {
        "date": data["response"]["date"],
        "base": data["response"]["base"],
        "exchange_rates": rates,
    }

    return render(request, "register/exchangerates.html", context)


def get_closing_price_at_date(asset_symbol, target_date):
    stock_data_path = os.path.join(settings.BASE_DIR, 'portfolio', 'stock_data')

    # Get all files in the directory
    files = os.listdir(stock_data_path)

    # Sort files based on filename in ascending order
    sorted_files = sorted(files, key=lambda x: x.lower())

    for filename in sorted_files:
        if filename.lower().endswith(".json"):
            # Extract date from the filename
            date_parts = filename.lower().split("_")[-3:]
            date_str = "_".join(date_parts)

            # Check if the date string has a valid format
            try:
                # Attempt to convert date string to a date object
                file_date = datetime.strptime(date_str, '%Y_%m_%d').date()

                if file_date >= target_date:
                    # Read JSON data from the file
                    file_path = os.path.join(stock_data_path, filename)
                    with open(file_path, 'r') as file:
                        data = json.load(file)

                    # Extract and return the closing price for the asset
                    closing_price = data.get(asset_symbol, {}).get('closing_price', 'N/A')

                    # If closing price is not available, log a warning
                    if closing_price == 'N/A':
                        logging.warning(f"Closing price not available for {asset_symbol} on {file_date}")
                        continue

                    return closing_price
            except ValueError as e:
                # Log a warning for invalid date format
                logging.warning(f"Invalid date format in filename: {filename}. Error: {e}")

    # If no matching files are found
    logging.warning(f"No matching files found for symbol: {asset_symbol}")


def calculate_gain_loss(stock, current_date=None):
    if current_date is None:
        current_date = timezone.now().date()

    trade_date = stock.trade_date

    if not trade_date:
        return 'N/A'

    # Fetch the latest closing price for the asset symbol at the trade date
    start_closing_price = get_closing_price_at_date(stock.asset, trade_date)
    if start_closing_price is None:
        print(f"Start closing price not available for {stock.asset} at trade date {trade_date}")
        return 'N/A'

    # Calculate cost of investment at the trade date
    start_cost_of_investment = Decimal(stock.num_shares) * Decimal(stock.purchase_price)

    # Fetch the latest closing price for the asset symbol at the current date
    end_closing_price = get_latest_closing_price(stock.asset)
    if end_closing_price is None:
        print(f"End closing price not available for {stock.asset}")
        return 'N/A'

    # Calculate current market value at the current date
    end_current_market_value = Decimal(stock.num_shares) * Decimal(end_closing_price)

    # Calculate gain/loss
    gain_loss = end_current_market_value - start_cost_of_investment

    print(f"Asset: {stock.asset}, Trade Date: {trade_date}, Start Closing Price: {start_closing_price}, End Closing Price: {end_closing_price}, Gain/Loss: {gain_loss}")

    return gain_loss



def get_closing_price_at_date(asset_symbol, target_date):
    stock_data_path = os.path.join(settings.BASE_DIR, 'portfolio', 'stock_data')

    # Construct the filename based on the target date
    filename = f"stock_data_polygon_{target_date.strftime('%Y-%m-%d').replace('-', '_')}.json"

    # Check if the file exists
    if not os.path.exists(os.path.join(stock_data_path, filename)):
        # File does not exist, return None

        return None

    # Read the JSON data from the file
    with open(os.path.join(stock_data_path, filename), 'r') as file:
        data = json.load(file)

    # Extract the closing price for the asset symbol if available
    if asset_symbol in data:
        closing_price = data[asset_symbol].get('closing_price')
        if closing_price is not None:
            # Closing price is available, return it
            return closing_price

    print(f"Closing price not available for {asset_symbol} at trade date {target_date}")

    # Closing price not available for the specified asset and date
    # Check if we can use the fallback date (November 1, 2023)
    fallback_date = "2023-11-01"  # Use hyphens instead of underscores
    fallback_filename = f"stock_data_polygon_{fallback_date.replace('-', '_')}.json"

    if os.path.exists(os.path.join(stock_data_path, fallback_filename)):
        print(f"Attempting to retrieve fallback closing price from file {fallback_filename}")
        # Read the JSON data from the fallback file
        with open(os.path.join(stock_data_path, fallback_filename), 'r') as fallback_file:
            fallback_data = json.load(fallback_file)

        # Extract the closing price for the asset symbol if available
        if asset_symbol in fallback_data:
            fallback_closing_price = fallback_data[asset_symbol].get('closing_price')
            if fallback_closing_price is not None:
                # Fallback closing price is available, return it
                print(f"Fallback closing price found: {fallback_closing_price}")
                return fallback_closing_price

    # Fallback closing price not available, return None
    print("Fallback closing price not available.")
    return None


@login_required
def display_user_stocks(request):
    # Fetch the stocks associated with the logged-in user
    user_stocks = Stock.objects.filter(user=request.user)

    # Pass the stocks data to the template
    return render(request, 'display_data.html', {'user_stocks': user_stocks})



def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)


def get_closing_price(asset, date):
    date_str = date.strftime('%Y_%m_%d')
    file_name = f"stock_data_polygon_{date_str}.json"
    file_path = os.path.join("path_to_json_files_directory",
                             file_name)  # Replace "path_to_json_files_directory" with the actual path
    if os.path.exists(file_path):
        data = load_json(file_path)
        if asset in data:
            return data[asset].get('closing_price')
    return None  # Return None if data for the asset and date is not found







from django.shortcuts import render
from .models import Stock, StockDataProcessor




def generate_arrays(request):
    # Assuming the user is authenticated
    user = request.user

    # Fetch all stocks associated with the user
    user_stocks = Stock.objects.filter(user=user)

    # Process data into arrays
    user_stock_data = []
    for stock in user_stocks:
        # Generate trade dates list from trade_date to current_date
        trade_dates = []
        closing_prices = []  # List to store closing prices
        current_date = date.today()
        while current_date >= stock.trade_date:
            trade_date_str = current_date.strftime('%b. %d, %Y')  # Format date as desired

            # Get the closing price for the current date
            closing_price = get_closing_price_at_date(stock.asset, current_date)

            # Add the date and closing price to the lists if the price is not None
            if closing_price is not None:
                trade_dates.append(trade_date_str)
                closing_prices.append(closing_price)

            current_date -= timedelta(days=1)  # Move to the previous day

        user_stock_data.append({
            'asset': stock.asset,
            'trade_dates': trade_dates,
            'closing_prices': closing_prices,
        })

    # Return JSON response with the data
    return JsonResponse({'user_stocks': user_stock_data})

def stock_graph_view(request):
    # Fetch stock data using the generate_arrays view
    json_stock_data = generate_arrays(request).content.decode('utf-8')

    # Pass the JSON data to the template
    return render(request, 'register/stock_graph.html', {'json_stock_data': json_stock_data})




