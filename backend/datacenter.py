import json
import requests
import operator
from indicators import *


class Stock():
    def __init__(self, ticker):
        self.ticker = ticker

        self.url = 'https://api.iextrading.com/1.0/stock/%s/chart/5y'
        self.company_url = 'https://api.iextrading.com/1.0/stock/%s/company'

        self.data = self.download_data(ticker)
        self.company_info = self.download_company_info(ticker)
        self.company_tags = [str(i) for i in self.company_info['tags']]

    def proccess_response(self, response):
        if response.status_code == 200:
            return response
        else:
            print 'error proccessing response: ' + str(response.status_code)
            return -1

    def sort_by_date(self, in_list):
        return sorted(in_list, key=operator.itemgetter(0))

    def get_data(self, start, end, option):
        li = self.data
        if li == -1:
            return -1
        if len(start.split('-')) == 3:
            out = []
            add_values = False
            for value in li:
                if value['date'] == end:
                    return out
                if value['date'] == start:
                    add_values = True

                if add_values is True:
                    out.append(value[option])
            return out

        elif len(start.split('-')) == 2:
            out = []
            add_values = False
            for value in li:
                current_date = value['date'].split('-')[0] + "-" + value['date'].split('-')[1]
                if current_date == end:
                    return out
                if current_date == start:
                    add_values = True

                if add_values is True:
                    out.append(value[option])
            return out

        elif len(start.split('-')) == 1:
            out = []
            add_values = False
            for value in li:
                current_date = value['date'].split('-')[0]
                if current_date == end:
                    return out
                if current_date == start:
                    add_values = True

                if add_values is True:
                    out.append(value[option])
            return out

    def get_close(self, start, end):
        return self.get_data(start, end, "close")

    def get_open(self, start, end):
        return self.get_data(start, end, "open")

    def get_rsi(self, start, end):
        closes = self.get_data(start, end, "close")
        return rsi(closes, 9)

    def download_data(self, ticker):
        url = self.url % (ticker)
        response = requests.get(url)

        response = self.proccess_response(response)
        if response != -1:
            data = json.loads(response.text)
            return data
        else:
            return -1

    def download_company_info(self, ticker):
        url = self.company_url % (ticker)
        response = requests.get(url)

        response = self.proccess_response(response)
        if response != -1:
            data = json.loads(response.text)
            return data
        else:
            return -1
