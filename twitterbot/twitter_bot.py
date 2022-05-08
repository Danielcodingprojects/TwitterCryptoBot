from twitterbot import db
from twitterbot.db_models import FollowerCount
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

    def send_tweet(self, message):
        response = self.client.create_tweet(
            text=message
        )
        print(f"https://twitter.com/user/status/{response.data['id']}")

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




