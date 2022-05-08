from apscheduler.schedulers.background import BackgroundScheduler
from twitterbot.twitter_bot import Bot
from twitterbot.transaction_checker import TransactionChecker
import time

bot = Bot()
TC = TransactionChecker()


def scheduled_tweeter():
    status = TC.get_status()
    if status["result"] == "success":
        data = TC.get_transactions()
        try:
            for transaction in data['transactions']:

                formatted_crypto_amount = f"{round(float(transaction['amount'])):,}"
                formatted_dollar_amount = f"{round(float(transaction['amount_usd'])):,}"

                # TODO: find a better blockchain explorer as cmp does not support all coins currently.
                msg_body = f"🚨 Someone has moved ~{formatted_crypto_amount} #{(transaction['symbol']).upper()} worth " \
                           f"~${formatted_dollar_amount} 🚨\nCheck out the full details at: " \
                           f"https://blockchain.coinmarketcap.com/tx/{transaction['blockchain']}/{transaction['hash']}"
                bot.send_tweet(message=msg_body)

                # prevents sending too many requests to Twitter api if there are many transactions.
                time.sleep(5)

        except KeyError:
            print('No transactions found')
    else:
        print('Could not connect to whale alert api.')


scheduler = BackgroundScheduler()

scheduler.add_job(func=bot.get_public_metrics, trigger="cron", day='*', hour=12)
scheduler.add_job(func=scheduled_tweeter, trigger="interval", minutes=5)
