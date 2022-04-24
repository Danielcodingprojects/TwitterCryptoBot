import tweepy
import os

bearer_token = os.environ['TWITTER_BEARER_TOKEN']
client_id = os.environ['TWITTER_CLIENT_ID']
client_secret = os.environ['TWITTER_CLIENT_SECRET']


class TwitterBot:
    def __init__(self):
        self.consumer_key = os.environ['TWITTER_CONSUMER_KEY']
        self.consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
        self.access_token = os.environ['TWITTER_ACCESS_TOKEN']
        self.access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

        self.client = tweepy.Client(
            consumer_key=self.consumer_key, consumer_secret=self.consumer_secret,
            access_token=self.access_token, access_token_secret=self.access_token_secret
        )

    def send_tweet(self, message):
        response = self.client.create_tweet(
            text=message
        )
        print(f"https://twitter.com/user/status/{response.data['id']}")

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

