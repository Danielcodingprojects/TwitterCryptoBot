from twitterbot import app

if __name__ == '__main__':
    app.run(debug=True)

# TC = TransactionChecker()
# bot = TwitterBot()
# bot.authenticate()
# recent_tweets = bot.get_recent_tweets(100)

# status = TC.get_status()
# if status["result"] == "success":
#     while True:
#         data = TC.get_transactions()
#         print(data)
#         try:
#             for transaction in data['transactions']:
#
#                 formatted_crypto_amount = f"{round(float(transaction['amount'])):,}"
#                 formatted_dollar_amount = f"{round(float(transaction['amount_usd'])):,}"
#
#                 # TODO: find a better blockchain explorer as cmp does not support all coins currently.
#                 msg_body = f"🚨 Someone has moved ~{formatted_crypto_amount} #{(transaction['symbol']).upper()} worth " \
#                            f"~${formatted_dollar_amount} 🚨\nCheck out the full details at: " \
#                            f"https://blockchain.coinmarketcap.com/tx/{transaction['blockchain']}/{transaction['hash']}"
#                 bot.send_tweet(message=msg_body)
#
#                 # prevents sending too many requests to Twitter api if there are many transactions.
#                 time.sleep(15)
#
#         except KeyError:
#             print('No transactions found')
#         time.sleep(1800)
# else:
#     print('Could not connect to whale alert api.')
