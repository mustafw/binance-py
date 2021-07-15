A simple Currency/Coin Price Scrape Module it uses Binance Web API \


Installation steps:
- Install package using `git clone https://github.com/mustafw/binance-py.git`
- Change directory into file `cd binance-py`
- Download **requests** module `python -m pip install requests`
- Run the module `python BinanceAPI.py` 

Module Usage:
-
- import the module into yours with `import BinanceScrape`  
- Get the **_USDT_** price of a coin live with `BinanceScrape.Prices().get_coin("FROM THIS", "TO THIS")`
- Get the **_EUR_** price of a currency with `BinanceScrape.Prices().get_currency("FROM THIS", "TO THIS")`







