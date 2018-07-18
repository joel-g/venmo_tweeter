import requests, tweepy, time, urllib
from random import shuffle

with open('config.ini','r') as config:
  tokens = config.readlines()
  TW_CONSUMER_KEY = tokens[0].rstrip()
  TW_CONSUMER_SECRET = tokens[1].rstrip()
  TW_ACCESS_KEY = tokens[2].rstrip()
  TW_ACCESS_SECRET = tokens[3].rstrip()

def authenticate_twitter():
  print('Authenticating twitter...')
  auth = tweepy.OAuthHandler(TW_CONSUMER_KEY, TW_CONSUMER_SECRET)
  auth.set_access_token(TW_ACCESS_KEY, TW_ACCESS_SECRET)
  twitter = tweepy.API(auth)
  print('Twitter authenticated.\n')
  return twitter

def get_venmos(num):
    vens = requests.get("https://venmo.com/api/v5/public?limit=" + str(num))
    return vens.json()['data']

def summarize(json):
    actor = json['actor']['name']
    target = json['transactions'][0]['target']['name']
    method = json['type']
    message = json['message']
    if method == 'payment':
        method = 'paid'
    elif method == 'charge':
        method = 'charged'
    return actor + ' ' + method + ' ' + target + ' for "' + message + '"'

def tweet(twitter, ven):
    summary = summarize(ven)
    if 'payment' == ven['type']:
        photo = ven['actor']['picture']
    elif 'charge' == ven['type']:
        photo = ven['transactions'][0]['target']['picture']
    if "no-image" in photo:
        print("Tweeting without photo")
        try:
            twitter.update_status(summary)
        except:
            print("Error tweeting")
    else:
        print("Tweeting with photo")
        urllib.request.urlretrieve(photo, "photo.png")
        try:
            twitter.update_with_media("photo.png", summary)
        except:
            print("Error tweeting")

def check_for_drugs(json):
    drugs = ['heroin', 'marijuana', 'drug', 'cocaine', 'meth', 'sex', 'weed', 'hookers', 'alcohol', '💉', '💊', 'pills', 'blowjob', 'porn', 'sherm', 'pcp']
    # shuffle(drugs)
    # print(drugs)
    if any(x in json['message'].lower() for x in drugs):
        return json['message']
    else: 
        return False


def main():
    twitter = authenticate_twitter()
    while True:
        vens = get_venmos(1000)
        for ven in vens:
            if check_for_drugs(ven):
                tweet(twitter, ven)
                print("Tweeted " + summarize(ven) + "\n Sleeping for an hour")
                time.sleep(3600)

if __name__ == '__main__':
  main()
