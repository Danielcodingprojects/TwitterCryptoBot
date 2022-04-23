import requests
from datetime import datetime
import calendar
import os

class TransactionChecker:
    def get_transactions(self):
        now = datetime.utcnow()
        unixtime = calendar.timegm(now.utctimetuple())
        since = unixtime

        apikey = os.environ['WHALE_ALERT.IO_APIKEY']
        print(apikey)
        min_value = str(500001)
        start = str(since-60*5)
        url = f'https://api.whale-alert.io/v1/transactions?api_key={apikey}&min_value={min_value}&start={start}'
        data = requests.get(url).json()

        return data
