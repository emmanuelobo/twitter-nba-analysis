from flask import Flask, render_template
from threading import Lock
import re
from flask_socketio import SocketIO, emit
import tweepy
from decouple import config
from havenondemand.hodclient import *
from havenondemand.hodresponseparser import *


class NBAStreamListener(tweepy.StreamListener):
	def on_status(self, status):
		print(status)

	def on_error(self, status_code):
		if status_code == 420:
			print('You are about to hit a RateLimit Exception.\n Disconnecting from server...')
			return False


client = HODClient(config('HOD_API_KEY'), version='v2')
parser = HODResponseParser()

app = Flask(__name__)
auth = tweepy.OAuthHandler(config('CONSUMER_KEY'), config('CONSUMER_SECRET'))
auth.set_access_token(config('ACCESS_TOKEN'), config('ACCESS_TOKEN_SECRET'))

api = tweepy.API(auth)

thread = None
thread_lock = Lock()
socketio = SocketIO(app)
streamListener = NBAStreamListener
myStream = tweepy.Stream(auth=api.auth, listener=streamListener())
tweet_sentiment = None


def parse_link(tweet):
	'''
	Remove the link from the tweet for a more accurate sentiment analysis
	:param tweet:
	:return:
	'''
	pass


def background_process():
	count = 0
	nba_tweets = api.search(q='nba', tweet_mode='extended')

	hodApp = HODApps.ANALYZE_SENTIMENT
	paramArr = {}
	paramArr["lang"] = "eng"
	context = {"hodapp": hodApp}
	while True:
		try:
			global tweet_sentiment
			print(nba_tweets[count]._json['full_text'])
			paramArr["text"] = nba_tweets[count]._json['full_text']
			client.post_request(params=paramArr, hodApp=hodApp, async=False, callback=callback, **context)
			socketio.sleep(5)
			socketio.emit('stream',
						  {'tweet': nba_tweets[count]._json['full_text'], 'count': count, 'sentiment': tweet_sentiment})
			count += 1
		except IndexError:
			continue


def callback(response, **context):
	payload = parser.parse_payload(response)
	global tweet_sentiment
	tweet_sentiment = payload['aggregate']['sentiment']
	print(payload['aggregate']['sentiment'])


@socketio.on('connect')
def handle_connection():
	global thread
	with thread_lock:
		if thread is None:
			thread = socketio.start_background_task(target=background_process)
		print('Connection Established')


@app.route('/')
def home():
	return render_template('homepage.html')


if __name__ == '__main__':
	app.run(debug=True)
