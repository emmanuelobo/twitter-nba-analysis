from flask import Flask, render_template
from threading import Lock
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

def background_process():
	count = 0
	nba_tweets = api.search('nba')
	while True:
		try:
			socketio.sleep(5)
			socketio.emit('stream', {'tweet': nba_tweets[count]._json['text'], 'count': count})
			count += 1
		except IndexError:
			socketio.sleep(5)
			socketio.emit('stream', {'tweet': nba_tweets[count]._json['text'], 'count': count})
			count += 1

def callback(response, **context):
	payload = parser.parse_payload(response)
	print(payload)


@socketio.on('connect')
def handle_connection():
	global thread
	with thread_lock:
		if thread is None:
			thread = socketio.start_background_task(target=background_process)
		print('Connection Established')


@socketio.on('stream event')
def handle_tweet_stream(message):
	emit('stream', message)

@app.route('/')
def home():
	text = ["I like dogs. They are loyal animals."]
	hodApp = HODApps.ANALYZE_SENTIMENT
	paramArr = {}
	paramArr["text"] = text
	paramArr["lang"] = "eng"
	context = {"hodapp": hodApp}
	client.post_request(params=paramArr, hodApp=hodApp, async=False, callback=callback, **context)
	return render_template('homepage.html')


if __name__ == '__main__':
	app.run(debug=True)
