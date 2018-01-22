import uuid
import time
import threading

import requests
from decimal import *


class Client(object):
    def __init__(self, url, public_key, secret):
        self.url = url + "/api/2"
        self.session = requests.session()
        self.session.auth = (public_key, secret)


    def get_symbol_list(self):
        """Get list of symbols."""
        return self.session.get("%s/public/symbol" % self.url).json()

    def get_candles(self, limit, period, symbol):
        """Get candles for a specific symbol."""

        data = {'limit': limit, 'period':period}
        return self.session.get("%s/public/candles/%s" % (self.url, symbol), params = data).json()


    def get_symbol(self, symbol_code):
        """Get symbol."""
        return self.session.get("%s/public/symbol/%s" % (self.url, symbol_code)).json()

    def get_orderbook(self, symbol_code):
        """Get orderbook."""
        return self.session.get("%s/public/orderbook/%s" % (self.url, symbol_code)).json()

    def get_address(self, currency_code):
        """Get address for deposit."""
        return self.session.get("%s/account/crypto/adress/%s" % (self.url, currency_code)).json()

    def get_account_balance(self):
        """Get main balance."""
        return self.session.get("%s/trading/balance" % self.url).json()

    def get_trading_balance(self):
        return self.session.get("%s/account/balance" % self.url).json()

    def transfer(self, currency_code, amount, to_exchange):
        return self.session.post("%s/account/transfer" % self.url, data={'currency': currency_code, 'amount': amount,
'type': 'bankToExchange' if to_exchange else 'exchangeToBank'}).json()

    def new_order(self, client_order_id, symbol_code, side, quantity, price=None):
        """Place an order"""
        data = {'symbol': symbol_code, 'side': side, 'quantity': quantity}
        if price is not None:
            data['price'] = price
        return self.session.put("%s/order/%s" % (self.url, client_order_id), data=data).json()

    def get_order(self, client_order_id, wait=None):
        """Get order info."""
        data = {'wait':wait} if wait is not None else {}
        return self.session.get("%s/order/%s" % (self.url, client_order_id), params=data).json()

    def cancel_order(self, client_order_id):
        """Cancel order."""
        return self.session.delete("%s/order/%s" % (self.url, client_order_id)).json()

    def withdraw(self, currency_code, amount, address, network_fee = None):
        """Withdraw."""

        data = {'currency': currency_code, 'amount': amount, 'address': address}


        if network_fee is not None:
            data['networkfee'] = network_fee
        return self.session.post("%s/account/crypto/withdraw" % self.url, data=data).json()

    def get_transaction(self, transaction_id):
        """Get transaction info."""
        return self.session.get("%s/account/transactions/%s" % (self.url, transaction_id)).json()


def get_highs(client, public_key, secret):
    """Get the maximum for the last ten days for each instrument and write it to a file"""
    symbol_list_json = client.get_symbol_list()
    symbol_list = []

    for symbol in symbol_list_json:
        if symbol['quoteCurrency'] == 'USD':
            symbol_list.append(symbol['id'])

    print(symbol_list)

    filename = "highs.txt"
    file = open(filename, "a")

    for symbol in symbol_list:
        candles = client.get_candles('240', 'H1', symbol)
        highs = []
        for candle in candles:
            highs.append(candle['max'])

        symbol_high = max(highs)
        print(symbol, symbol_high)
        file.write(symbol + " " + symbol_high + ",")
        time.sleep(1)






if __name__ == "__main__":

    public_key = "e12c91bee2ef48e5c0d69b1db6764450"
    secret = "0f2835b6a0a18264ae6490a8703346bf"
    btc_address = "3GxjEYuEjTVagWAhBEDVJxvL2zoyAfeYs9"

    client = Client("https://api.hitbtc.com", public_key, secret)

    get_highs(client,public_key,secret)






