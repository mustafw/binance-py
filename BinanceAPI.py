#!/usr/bin/python3
import requests, json, sys, pathlib

class CheckVersion:
    def __init__(self, update=False):
        current_version=0.1
        r=requests.get("https://raw.githubusercontent.com/mustafw/binance-py/main/README.md").text.splitlines()
        git_version="".join(i.replace("version=", "") if "version" in i else "" for i in r)
        if git_version!=current_version:
            print(f"There is a new version \"{git_version}\" available on https://github.com/mustafw/binance-py! You must run CheckVersion(update=True) to update automatically")
            if update:
                new_text=requests.get("https://raw.githubusercontent.com/mustafw/binance-py/main/BinanceAPI.py").text
                with open(__file__, "w", encoding="utf8") as f: # f"{pathlib.Path('python3').resolve()}/Lib/site-packages/BinanceAPI.py"
                    f.write(new_text)
                    exit(f"BinanceAPI has been updated to version {git_version} from {current_version}.")

class Prices:
    def __init__(self):
        CheckVersion(update=False)
        self.sites, self.get_json, self.coins, self.currencies = {
                                                                     "coins": "https://www.binance.com/gateway-api/v2/public/asset-service/product/get-products?includeEtf=true",
                                                                     "coins_status": "https://www.binance.com/gateway-api/v1/friendly/margin/symbols",
                                                                     "currencies": "https://www.binance.com/gateway-api/v1/public/asset-service/product/currency",
                                                                 }, lambda page: requests.get(page).json(), {}, {}

    def get_coin_status(self, base: str = "ETH", quote: str = "BTC"):

        base, quote, json_ = base.upper(), quote.upper(), self.get_json(self.sites["coins_status"])["data"]
        for i in json_:
            if i["symbol"] == f"{base}{quote}":
                return {i["symbol"]: {"isMarginTrade": i["isMarginTrade"], "isBuyAllowed": i["isMarginTrade"],
                                      "isSellAllowed": i["isSellAllowed"], "status": i["status"]}}

    def get_coin(self, base: str = "BTC", quote: str = "USDT", pass_status=False):
        base, quote, coin_output, make_float = base.upper(), quote.upper(), {"pair": base + quote, "from": None,
                                                                             "to": None, "rate": None,
                                                                             "24H": {"HIGH": None, "LOW": None,
                                                                                     "AVERAGE": None}}, lambda x: float(
            str(x).replace(",", "."))
        if base == quote: return "An error raised: " + (
            f"{base} is equals to {quote}" if base == quote else "")
        json_ = self.get_json(self.sites["coins"])["data"]
        for coin in json_:
            self.coins[coin["s"]] = coin
        if f"{base}{quote}" in self.coins:
            coin = self.coins[f"{base}{quote}"]
            coin_output["from"] = coin["qn"]
            coin_output["to"] = coin["an"]
            coin_output["rate"] = coin["c"]
            coin_output["24H"]["HIGH"] = coin["h"]
            coin_output["24H"]["LOW"] = coin["l"]
            coin_output["24H"]["AVERAGE"] = coin["o"]
        else:
            try:
                coin, coin2 = self.coins[quote + ("BTC" if quote != "BTC" else "USDT")], self.coins[
                    base + ("BTC" if base != "BTC" else "USDT")]
            except:
                return (coin_output, self.get_coin_status(base,
                                                          quote if base != "BTC" else "ETH")) if not pass_status else coin_output
            coin_output["from"] = coin["qn"]
            coin_output["to"] = coin["an"]
            coin_output["rate"] = str(make_float(coin["c"]) / make_float(coin2["c"]))
            coin_output["24H"]["HIGH"] = str(make_float(coin["h"]) / make_float(coin2["h"]))
            coin_output["24H"]["LOW"] = str(make_float(coin["l"]) / make_float(coin2["l"]))
            coin_output["24H"]["AVERAGE"] = str(make_float(coin["o"]) / make_float(coin2["o"]))
        return (
        coin_output, self.get_coin_status(base, quote if base != "BTC" else "ETH")) if not pass_status else coin_output

    def get_currency(self, base: str = "EUR", quote: str = "USD"):
        base, quote = base.upper(), quote.upper()
        json_ = self.get_json(self.sites["currencies"])["data"]
        currency_output = {i: None for i in ["pair", "rate", "symbol", "fullName", "imageUrl"]}
        for currency in json_:
            self.currencies[currency["pair"]] = currency
        if self.currencies.__contains__(f"{quote}_{base}"):
            currency = self.currencies[f"{quote}_{base}"]
            currency_output["pair"] = f"{base}_{quote}"
            currency_output["fullName"] = currency["fullName"]
            currency_output["symbol"] = currency["symbol"]
            currency_output["rate"] = float(currency["rate"])
            currency_output["imageUrl"] = currency["imageUrl"]
        else:
            currency, currency2 = self.currencies[f"{quote}_{'USD' if quote != 'USD' else 'EUR'}"], self.currencies[
                f"{base}_{'USD' if base != 'USD' else 'EUR'}"]
            currency_output["pair"] = f"{base}_{quote}"
            currency_output["fullName"] = currency2["fullName"]
            currency_output["symbol"] = currency2["symbol"]
            currency_output["rate"] = str(float(currency["rate"]) / float(currency2["rate"]))[:5]
            currency_output["imageUrl"] = currency2["imageUrl"]

        return currency_output


"""

------------------------------------
----------|    EXAMPLE   |----------
------------------------------------

"""

if __name__ == "__main__":
    jd = lambda x: json.dumps(x, indent=2)  ###  THIS MAKES JSON BEAUTIFUL! IT'S OPTIONAL  ###
    b = Prices()

    "---------|   WITH JSON BEAUTIFUL FUNCTION   |---------"
    print(jd(b.get_currency("eur", "usd")), "\n", jd(b.get_coin("xrp", "usdt",
                                                                pass_status=False)), )  ### YOU MAY SET "pass_status=False" to "pass_status=True" IF YOU WANT MORE DETAILS

    "---------|   WITHOUT JSON BEAUTIFUL FUNCTION   |---------"
    print(b.get_currency("eur", "usd"), "\n", b.get_coin("xrp", "usdt",
                                                         pass_status=False), )  ### YOU MAY SET "pass_status=False" to "pass_status=True" IF YOU WANT MORE DETAILS
