# # #
# # #
# # # import os
# # # import json
# # #
# # # def get_latest_price_by_symbol(symbol):
# # #     # Directory containing the stock data files
# # #     data_dir = r"C:\Users\cryse\OneDrive\Pulpit\Investment-Portfolio\portfolio\stock_data"
# # #
# # #     # Get all files in the directory
# # #     files = os.listdir(data_dir)
# # #
# # #     # Extract relevant information from each file
# # #     file_info_list = []
# # #
# # #     for file in files:
# # #         if file.lower().endswith(".json"):
# # #             # Extract date and symbol from the filename
# # #             parts = file.lower().split("_")
# # #             if len(parts) >= 4:
# # #                 date_str = parts[-3]  # Assuming the date is at the third-to-last position
# # #                 file_info_list.append((file, date_str))
# # #
# # #     # Sort files based on date in descending order
# # #     sorted_files = sorted(file_info_list, key=lambda x: x[1], reverse=True)
# # #
# # #     if not sorted_files:
# # #         print(f"No matching files found for symbol: {symbol}")
# # #         return None
# # #
# # #     # Get the latest file
# # #     latest_file, latest_date = sorted_files[0]
# # #     print(f"Latest File for {symbol} (Date: {latest_date}): {latest_file}")
# # #
# # #     # Construct the full path to the latest file
# # #     file_path = os.path.join(data_dir, latest_file)
# # #
# # #     # Read JSON data from the file
# # #     with open(file_path, 'r') as file:
# # #         data = json.load(file)
# # #
# # #     print(f"JSON data for {symbol} in file {latest_file}:")
# # #     print(json.dumps(data, indent=2))
# # #
# # #     # Extract and return the closing price for the asset
# # #     return data.get(symbol, {}).get('closing_price', None)
# # #
# # # # Test with user input symbol
# # # user_symbol = input("Enter the asset symbol: ")
# # # latest_price = get_latest_price_by_symbol(user_symbol)
# # #
# # # if latest_price is not None:
# # #     print(f"Closing price of {user_symbol} in the latest available file: {latest_price}")
# # # else:
# # #     print(f"No data found for {user_symbol}")
# # #
# # import os
# # import json
# #
# # def get_latest_price_by_symbol(symbol):
# #     # Directory containing the stock data files
# #     data_dir = r"C:\Users\cryse\OneDrive\Pulpit\Investment-Portfolio\portfolio\stock_data"
# #
# #     # Get all files in the directory
# #     files = os.listdir(data_dir)
# #
# #     # Extract relevant information from each file
# #     file_info_list = []
# #
# #     for file in files:
# #         if file.lower().endswith(".json"):
# #             # Extract date and symbol from the filename
# #             parts = file.lower().split("_")
# #             if len(parts) >= 4:
# #                 date_str = parts[-3]  # Assuming the date is at the third-to-last position
# #                 file_info_list.append((file, date_str))
# #
# #     # Sort files based on date in descending order
# #     sorted_files = sorted(file_info_list, key=lambda x: x[1], reverse=True)
# #
# #     if not sorted_files:
# #         print(f"No matching files found for symbol: {symbol}")
# #         return None
# #
# #     # Get the latest file
# #     latest_file, latest_date = sorted_files[0]
# #     print(f"Latest File for {symbol} (Date: {latest_date}): {latest_file}")
# #
# #     # Construct the full path to the latest file
# #     file_path = os.path.join(data_dir, latest_file)
# #
# #     # Read JSON data from the file
# #     with open(file_path, 'r') as file:
# #         data = json.load(file)
# #
# #     # Extract and return the closing price for the asset
# #     closing_price = data.get(symbol, {}).get('closing_price', None)
# #
# #     return closing_price
# #
# # # Test with user input symbol
# # user_symbol = input("Enter the asset symbol: ")
# # latest_price = get_latest_price_by_symbol(user_symbol)
# #
# # if latest_price is not None:
# #     print(f"Closing price of {user_symbol} in the latest available file: {latest_price}")
# # else:
# #     print(f"No data found for {user_symbol}")
#
#
# # views.py
#
# from django.shortcuts import render
# from .models import Profile, Stock
# from datetime import datetime
#
# def generate_arrays(request):
#     # Assuming the user is authenticated
#     user = request.user
#     profile = Profile.objects.get(user=user)
#
#     # Fetch all stocks associated with the user's profile
#     assets = Stock.objects.filter(profile=profile)
#
#     # Process data into arrays
#     dates = []
#     gain_loss_values = []
#
#     for asset in assets:
#         # Assuming trade_date is a DateTimeField in your Stock model
#         trade_date = asset.trade_date.strftime('%Y-%m-%d') if asset.trade_date else None
#         dates.append(trade_date)
#
#         # Replace with your actual calculation logic for gain/loss
#         gain_loss = asset.calculate_gain_loss()
#         gain_loss_values.append(gain_loss)
#
#     # Print arrays for verification
#     print("Dates:", dates)
#     print("Gain/Loss Values:", gain_loss_values)
#
#     # Pass the arrays to the template or return as JSON
#     context = {
#         'dates': dates,
#         'gain_loss_values': gain_loss_values,
#     }
#
#     return render(request, 'arrays_display.html', context)
# views.py

from django.shortcuts import render
from models import Profile, Stock
from datetime import datetime

def generate_arrays(request):
    # Assuming the user is authenticated
    user = request.user
    profile = Profile.objects.get(user=user)

    # Fetch all stocks associated with the user's profile
    assets = Stock.objects.filter(profile=profile)

    # Process data into arrays
    dates = []
    gain_loss_values = []

    for asset in assets:
        # Assuming trade_date is a DateTimeField in your Stock model
        trade_date = asset.trade_date.strftime('%Y-%m-%d') if asset.trade_date else None
        dates.append(trade_date)

        # Replace with your actual calculation logic for gain/loss
        gain_loss = asset.calculate_gain_loss()
        gain_loss_values.append(gain_loss)

    # Print arrays for verification
    print("Dates:", dates)
    print("Gain/Loss Values:", gain_loss_values)

    # If you want to return arrays as JSON, you can use JsonResponse
    # from django.http import JsonResponse
    # return JsonResponse({'dates': dates, 'gain_loss_values': gain_loss_values})

    # Customize the view based on the user
    context = {
        'user': user,
        'dates': dates,
        'gain_loss_values': gain_loss_values,
    }

    return render(request, 'arrays_display.html', context)
