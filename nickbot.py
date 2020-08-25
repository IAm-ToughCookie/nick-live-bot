import requests
import time
import tweepy
import config

# DEBUG ONLY
set_online = False  # if set to true will set URL to BobRoss instead of Nick's stream! 

if set_online == True:
    URL = "https://api.twitch.tv/kraken/streams/105458682" # BobRoss-Stream
else:
    URL = "https://api.twitch.tv/kraken/streams/441080048" # Nick-Stream

def tweet(msg):
    auth = tweepy.OAuthHandler(config.API_KEY, config.API_SECRET)

    auth.set_access_token( config.ACCESS_TOKEN, config.ACCESS_SECRET)

    api = tweepy.API(auth)

    tweet = msg

    status = api.update_status(status=tweet)

def get_initial_state(url, client_id, accept):
    r = requests.get(url, headers={"Client-ID": client_id, "Accept": accept})
    resp = r.json()
    
    if resp.get('stream') is None:
        online = False
    else:
        online = True
    return online

def check_online(url, client_id, accept):
    global online

    r = requests.get(url, headers={"Client-ID": client_id, "Accept": accept})
    resp = r.json()
    
    if resp.get('stream') is not None:
        online = True
        game = resp.get('stream').get('game')
        stream_url = resp.get('stream').get('channel').get('url')
        tweet_send = False
        if tweet_send == False:
            tweet(f'.@LiL_Nickyy_ is now online playing {game}, join at {stream_url}')
            print("tweet send")
            tweet_send = True
        else:
            print('Stream is still online, no new tweet!')
    else:
        online = False
        tweet_send = False
        print('Stream offline')
        
online = get_initial_state(URL, config.CLIENT_ID, config.ACCEPT)

if online == False:
    while online == False:
        print(online)
        print('Stream offline: ')
        check_online(URL, config.CLIENT_ID, config.ACCEPT)
        time.sleep(10)
else:
    while online == True:
        print(online)
        print(f'Stream online: ')
        check_online(URL, config.CLIENT_ID, config.ACCEPT)
        time.sleep(5400)