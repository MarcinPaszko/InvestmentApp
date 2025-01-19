----|||| Investmnent Portfolio Dashboard ||||----

This is Investment Portfolio project site, simulating real time investor tool dashboard for stock data.
Based on:
-Python Django framework - exposed at 8000:8000;
-Node JS search engine used to browse data from Mongo DB stored stock assets price - exposed art 3000:3000;
-Mongo DB database used to store data from STOCK API - exposed at port 27017:27017;

Users are able to log, add stock to their portfolio and receive information about gain loss on their securities based on current FX rate.
Users are able to create accounts.

Descriptions of subsites:

-Home - using API provided latest news from MarketWatch, updated based on refreshing site;
-Database - date of stock asset stored, user can search based on stock symbol (like Apple - AAPL, Disney - DIS etc.), powered by node;
-Login/Register - used to login/register by users;
-Stock Add - used by user to add stock if user for example brought stock he can provide amount of shares, price and other factors to determine gain loss and graph view on his profile page;
-Exchange Rates - used to calculate amount of cash in sme currency into other currencies;
-Profile - user profile with all data about stock held, gain losses, current protfolio, gauges of gain loss and graphs;
-Arrays - used for backed, JSONed data about current logged user portfolio;
-Graph - used to display graph of user held securities;

Entering DJANGO container exposed at 8000 port using exec there is file Stock_API.py located in main path ./portfolio, executing this using command "python Stock_API.py" user is able to manually launch Stock API used to derive proces from Polygon API.
This API provides data for 50 assets max per 60 seconds, so trying to derive 51 asset prices/data per once will provide error and return no data.
Considering this there is sleep function exposed in Stock_API whoch derives 50 assets provded in JSON stock list, then awaits 60 seconds to derive another batch of assets. Once whole list is complete function ends.
Function launched in CLI ask user to provide date on whoch data should be feetched, after collection data is stored in MongoDB and stored in JSON format at ./portfolio/stock_data.
