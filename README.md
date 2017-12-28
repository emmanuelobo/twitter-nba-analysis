# twitter-nba-analysis

Get a pulse of what people are talking about on twitter related to the NBA by analyzing the sentiments of each tweet.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

```
python 2.7 
pip
virtualenv
twitter developer account
```

### Installing

A step by step series of examples that tell you have to get a development env running

## Set up virtual environment

Navigate to code directory in Terminal and run following command

* Create and activate virtual environment for directory.

		virtualenv venv
		. venv/bin/activate

* Install requirements for app

		pip install -r requirements.txt


## Create Twitter Application/Account

* Create new app here, <https://dev.twitter.com/apps>.
* Set application as **Read and Write** capable

Click the button on the bottom of your app to create an OAUTH Key and Secret for yourself to use.

### Set up Twitter Credentials

In your Application settings, find the tokens and keys, you will need these to use the Twitter API.

Create **.env** file with the following


	OAUTH_TOKEN=YOUROAUTHTOKENHERE
	OAUTH_SECRET=YOUROAUTHSECRETHERE
	CONSUMER_KEY=YOURCONSUMERKEYHERE
	CONSUMER_SECRET=YOURCONSUMERSECRETHERE

Save as **.env** in your code directory.


## Start the server
Run the following code inside the project's directory
```bazaar
python app.py
```