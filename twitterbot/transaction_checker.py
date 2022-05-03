import requests
from datetime import datetime
import calendar
import os


class TransactionChecker:
    def __init__(self):
        self.api_key = os.environ['WHALE_ALERT.IO_APIKEY']

    def get_status(self):
        url = f'https://api.whale-alert.io/v1/status?api_key={self.api_key}'
        status = requests.get(url).json()

        return status

    def get_transactions(self):
        # gets time and converts to unix format.
        now = datetime.utcnow()
        unixtime = calendar.timegm(now.utctimetuple())

        min_value = '500001'
        start = str(unixtime - 60 * 5)
        url = f'https://api.whale-alert.io/v1/transactions?api_key={self.api_key}&min_value={min_value}&start={start}'
        data = requests.get(url).json()

        return data
