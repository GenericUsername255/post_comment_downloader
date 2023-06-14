import configparser
import praw
import json

config = configparser.ConfigParser()
config.read('settings.ini')


reddit_client = config['reddit_client']
client_id=reddit_client['client_id'],
client_secret=reddit_client['client_secret'],
user_agent=reddit_client['user_agent']

print(client_id, client_secret, user_agent)

