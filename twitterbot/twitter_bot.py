from twitterbot import db
from twitterbot.db_models import FollowerCount, Tweets
import tweepy
import os
from datetime import datetime

client_id = os.environ['TWITTER_CLIENT_ID']
client_secret = os.environ['TWITTER_CLIENT_SECRET']


class Bot:
    def __init__(self):
        self.consumer_key = os.environ['TWITTER_CONSUMER_KEY']
        self.consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
        self.access_token = os.environ['TWITTER_ACCESS_TOKEN']
        self.access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']
        self.bearer_token = os.environ['TWITTER_BEARER_TOKEN']
        self.account_id = 1517899963300261888

        self.client = tweepy.Client(
            consumer_key=self.consumer_key, consumer_secret=self.consumer_secret,
            access_token=self.access_token, access_token_secret=self.access_token_secret,
            bearer_token=self.bearer_token
        )

    def authenticate(self):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.secure = True
        auth_url = auth.get_authorization_url()

        print('Please authorize: ' + auth_url)

        # verifier is the oauth token in your url
        verifier = input('PIN: ').strip()

        auth.get_access_token(verifier)

        print("ACCESS_KEY = '%s'" % auth.access_token)
        print("ACCESS_SECRET = '%s'" % auth.access_token_secret)

    def create_tweet_body(self, transaction):
        blockchain_explorer_dict = {
            "bitcoin": "https://www.blockchain.com/btc/tx/",
            "ethereum": "https://etherscan.io/tx/",
            "stellar": "https://stellar.expert/explorer/public/tx/",
            "ripple": "https://xrpscan.com/ledger/",
            "neo": "https://neoscan.io/transaction/",
            "tron": "https://tronscan.io/#/transaction/",
            "eos": "https://www.eosx.io/tx/",
        }
        for blockchain in blockchain_explorer_dict:
            if transaction['blockchain'] == blockchain:
                formatted_crypto_amount = f"{round(float(transaction['amount'])):,}"
                formatted_dollar_amount = f"{round(float(transaction['amount_usd'])):,}"

                msg_body = f"🚨 Someone has moved ~{formatted_crypto_amount} #{(transaction['symbol']).upper()} worth " \
                           f"~${formatted_dollar_amount} 🚨\nCheck out the full details at: " \
                           f"{blockchain_explorer_dict[blockchain]}{transaction['hash']}"
                return msg_body

    def send_tweet(self, message):
        response = self.client.create_tweet(text=message)
        new_entry = Tweets(
            tweet_id=response.data['id'],
            tweet_body=response.data['text'],
            created_at=datetime.now()
        )
        db.session.add(new_entry)
        db.session.commit()

    def get_recent_tweets(self, amount):
        response = self.client.get_users_tweets(self.account_id, max_results=amount)
        print(response)

    def get_public_metrics(self):
        response = self.client.get_user(id=self.account_id, user_fields=['public_metrics'])
        data = response.data
        new_entry = FollowerCount(
            count=data.public_metrics['followers_count'],
            datetime=datetime.today()
        )
        db.session.add(new_entry)
        db.session.commit()




