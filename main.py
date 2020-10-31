import tweepy
import requests
import os
from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")

CONSUMER_KEY = config["key"]["consumer_key"]
CONSUMER_SECRET = config["key"]["consumer_secret"]

ACCESS_TOKEN = config["key"]["access_token"]
ACCESS_SECRET = config["key"]["access_secret"]

USERNAME = config["option"]["user_id"]

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth)

dir = "./results/" + USERNAME + "/"
if not os.path.exists(dir): os.makedirs(dir)

print("[INFO] Searching for {}'s timeline".format(USERNAME))

for tweet in tweepy.Cursor(api.user_timeline, id=USERNAME).items():
    if hasattr(tweet, 'extended_entities'):
        for media in tweet.extended_entities["media"]:
            if media["type"] == "video":

                # Searching for best video quality
                url = ""
                for idx in range(len(media["video_info"]["variants"]), 0, -1):
                    if (media["video_info"]["variants"][idx-1]["content_type"] == "video/mp4"):
                        url = media["video_info"]["variants"][idx-1]["url"].split("?")[0]
                        break

            elif media["type"] == "photo":
                url = media["media_url"]

            # Processing URL
            filename = tweet.created_at.strftime("%y%m%d") + "_" + url.split('/')[-1]
            if (os.path.exists(dir + filename)):
                print("[INFO] File {} exists, skipping...".format(filename))
            else:
                print("[INFO] Downloading {}".format(url))
                r = requests.get(url)
                with open(dir + filename, 'wb') as f:
                    f.write(r.content)

    elif "media" in tweet.entities:
        for media in tweet.entities["media"]:
            url = media["media_url"]

            # Processing URL
            filename = tweet.created_at.strftime("%y%m%d") + "_" + url.split("/")[-1]
            if (os.path.exists(dir + filename)):
                print("[INFO] File {} exists, skipping...".format(filename))
            else:
                print("Downloading {}".format(url))
                r = requests.get(url)
                with open(dir + filename, 'wb') as f:
                    f.write(r.content)

print("[INFO] Done!")