from transaction_checker import TransactionChecker
from twitter_bot import TwitterBot
import time

TC = TransactionChecker()
bot = TwitterBot()
# bot.authenticate()

data = TC.get_transactions()
if data:
    try:
        for transaction in data['transactions']:

            formatted_crypto_amount = f"{round(float(transaction['amount'])):,}"
            formatted_dollar_amount = f"{round(float(transaction['amount_usd'])):,}"

            # TODO: find a better blockchain explorer as cmp does not support all coins currently.
            msg_body = f"🚨 Someone has moved ~{formatted_crypto_amount} #{(transaction['symbol']).upper()} worth " \
                       f"~${formatted_dollar_amount} 🚨\nCheck out the full details at: " \
                       f"https://blockchain.coinmarketcap.com/tx/{transaction['blockchain']}/{transaction['hash']}"
            bot.send_tweet(message=msg_body)

            # prevents sending too many requests to twitter api if there are many transactions.
            time.sleep(15)

    except KeyError:
        print('No transactions found')


