from apscheduler.schedulers.background import BackgroundScheduler
from twitterbot.twitter_bot import Bot
from twitterbot.transaction_checker import TransactionChecker
from twitterbot.db_models import db, Pagination_Key, Transactions
import time

bot = Bot()
TC = TransactionChecker()


def scheduled_tweeter():
    status = TC.get_status()
    if status["result"] == "success":
        pagination_key = db.session.query(Pagination_Key).first()
        cursor = pagination_key.cursor
        print(cursor)
        data = TC.get_transactions(cursor=cursor)
        try:
            for transaction in data['transactions']:
                msg_body = bot.create_tweet_body(transaction)
                bot.send_tweet(message=msg_body)

                new_entry = Transactions(
                    blockchain=transaction["blockchain"],
                    coin=transaction["symbol"],
                    amount_crypto=transaction["amount"],
                    amount_usd=transaction["amount_usd"],
                    hash=transaction["hash"],
                    from_addr=transaction["from"]["address"],
                    to_addr=transaction["to"]["address"]
                )
                db.session.add(new_entry)
                db.session.commit()
                # prevents sending too many requests to Twitter api if there are many transactions.
                time.sleep(3)

            if cursor is None:
                new_entry = Pagination_Key(cursor=data['cursor'])
                db.session.add(new_entry)
                db.session.commit()
            else:
                cursor_to_update = Pagination_Key.query.first()
                cursor_to_update.cursor = data['cursor']
                db.session.commit()

        except KeyError:
            print('No transactions found')
    else:
        print('Could not connect to whale alert api.')


scheduler = BackgroundScheduler()

scheduler.add_job(func=bot.get_public_metrics, trigger="cron", day='*', hour=12)
scheduler.add_job(func=scheduled_tweeter, trigger="interval", minutes=5)
