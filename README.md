A simple Binance API made for **Python3.5x** \
This module lets you get live financial reports from **www.binance.com** 


Installation steps:
- Install package using `git clone https://github.com/mustafw/binance-py.git`
- Change directory into file `cd binance-py-main`
- Download **requests** module through `pip install requests` or `python -m pip install requests`
- Here you go! You may run the file with `python BinanceAPI.py` to see how module works or continue reading

Usage:
-
- import the module into yours with `import BinanceAPI`  
- Get the **_USDT_** price of a coin live with `BinanceAPI.BinancePrices().get_coin("THE_SHORT_NAME_OF_THE_COIN", "USDT")` and you may use `pass_status=True` to pass some information about is coin able to trade
- Get the **_EUR_** price of a currency with `BinanceAPI.BinancePrices().get_currency("THE_SHORT_NAME_OF_THE_CURRENCY", "EUR")`







