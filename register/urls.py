# # register/urls.py
#
# from django.urls import path
# from .views import register, custom_login, stock_add, profile, exchangerates
#
# app_name = 'register'
# urlpatterns = [
#     path('', register, name='register'),
#     path('login/', custom_login, name='login'),
#     path('profile/', profile, name='profile'),
#     path('stock_add/', stock_add, name='stock_add'),
#     path('exchangerates/', exchangerates, name='exchangerates'),
#
# ]
from django.urls import path
from .views import register, custom_login, stock_add, profile, exchangerates, generate_arrays, stock_graph_view

app_name = 'register'
urlpatterns = [
    path('', register, name='register'),
    path('login/', custom_login, name='login'),
    path('profile/', profile, name='profile'),
    path('stock_add/', stock_add, name='stock_add'),
    path('exchangerates/', exchangerates, name='exchangerates'),
    path('display_data/', generate_arrays, name='display_data'),
    path('graph/', stock_graph_view, name='stock_graph'),


]