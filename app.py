from flask import Flask, render_template
import tweepy
from decouple import config
from havenondemand.hodclient import *
from havenondemand.hodresponseparser import *

client = HODClient(config('HOD_API_KEY'), version='v2')
parser = HODResponseParser()

app = Flask(__name__)
auth = tweepy.OAuthHandler(config('CONSUMER_KEY'), config('CONSUMER_SECRET'))
auth.set_access_token(config('ACCESS_TOKEN'), config('ACCESS_TOKEN_SECRET'))


api = tweepy.API(auth)

def callback(response, **context):
	payload = parser.parse_payload(response)
	print(payload)


@app.route('/')
def home():
	user = api.me()
	timeline = api.home_timeline()
	text = ["I like dogs. They are loyal animals."]
	hodApp = HODApps.ANALYZE_SENTIMENT
	paramArr = {}
	paramArr["text"] = text
	paramArr["lang"] = "eng"
	context = {"hodapp": hodApp}
	print(timeline[2])
	client.post_request(params=paramArr, hodApp=hodApp, async=False, callback=callback, **context)
	return render_template('homepage.html', user=user, timeline=timeline[0]._json)


if __name__ == '__main__':
	app.run(debug=True)
