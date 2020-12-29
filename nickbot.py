import requests
import time
import tweepy
import config
import random
from datetime import datetime
import pytz

# DEBUG ONLY
debug = True # Set Debug [DEFAULT: False]
set_online = False  # if set to true will set URL to BobRoss instead of Nick's stream! 

# SETUP TIMEZONE


if set_online == True:
    URL = "https://api.twitch.tv/kraken/streams/105458682" # BobRoss-Stream
else:
    URL = "https://api.twitch.tv/kraken/streams/441080048" # Nick-Stream


def get_time():
    utc_now = pytz.utc.localize(datetime.now())
    cest_now = utc_now.astimezone(pytz.timezone("Europe/Vienna"))
    cest_now_str = cest_now.strftime("%d. %b, %H:%M:%S")
    return cest_now_str

def tweet(msg):
    auth = tweepy.OAuthHandler(config.API_KEY, config.API_SECRET)

    auth.set_access_token( config.ACCESS_TOKEN, config.ACCESS_SECRET)

    api = tweepy.API(auth)

    tweet = msg

    status = api.update_status(status=tweet)

def get_initial_state(url, client_id, accept):
    try:
        r = requests.get(url, headers={"Client-ID": client_id, "Accept": accept})
        resp = r.json()
    except ValueError:
        print(f"Request failed at initial state: {r.status_code} - {r.reason}")
        online = False
        return online

    if resp.get('stream') is None:
        online = False
    else:
        online = True
    return online

def check_online(url, client_id, accept):
    global online
    global tweet_send

    try:
        r = requests.get(url, headers={"Client-ID": client_id, "Accept": accept})
        resp = r.json()
    except ValueError: 
        print(f"Request failed at initial state: {r.status_code} - {r.reason}")
        online = False
        tweet_send = False
        print(f'-'*20 + ' No tweet - Stream offline')
    
    if resp.get('stream') is not None:
        online = True
        now = datetime.now()
        now_str = now.strftime("%d.%m. %H:%M:%S")
        game = resp.get('stream').get('game')
        stream_url = resp.get('stream').get('channel').get('url')
        
        if tweet_send == False:
            tweet_msg_list = [
                '.@LiL_Nickyy_ is now online playing ' + game + ' join at ' + stream_url,
                'My father @LiL_Nickyy_ is now playing ' + game + ' on Twitch! Join here: ' + stream_url,
                'Guess who\'s back! @LiL_Nickyy_ is back, back again. Playing ' + game + ' !  ' + stream_url,
                'It be online like that! @LiL_Nickyy_ playing  ' + game + ' at ' + stream_url,
                'Hey it\'s ya boy, @LiL_Nickyy_ playing that  ' + game + ' at ' + stream_url,
                'It\'s ' + get_time() + ' perfect time to watch @LiL_Nickyy_ play some ' + game + ' at ' + stream_url,
                '[' + get_time() + '] Go and watch some @LiL_Nickyy_ play ' + game + ' you filthy casual!  ' + stream_url,
                'It is now: ' + get_time() + ' . Stay hydrated. Practicse self love and watch @LiL_Nickyy_ play ' + game + ' at ' + stream_url
            ]
            fallback_tweet = '[' + get_time()+ '] @LiL_Nickyy_ is online. Playing  ' + game + '  at  ' + stream_url
            try:
                if debug is True:
                    print(f'{game}')
                    print(tweet_msg_list[random.randrange(0,len(tweet_msg_list))])
                else:
                    tweet(tweet_msg_list[random.randrange(0,len(tweet_msg_list))])
                    print(f'-'*20 + ' Tweet send')
                    tweet_send = True
            except tweepy.error.TweepError:
                tweet(fallback_tweet)
                print(f'-'*20 + ' Fallback-tweet send')
                tweet_send = True
        else:
            print(f'-'*20 + ' No tweet - Stream still online')
    else:
        online = False
        tweet_send = False
        print(f'-'*20 + ' No tweet - Stream offline')
        
online = get_initial_state(URL, config.CLIENT_ID, config.ACCEPT)
tweet_send = False


def start_online_loop():
    while online == True:
        print(f'[{get_time()}] Online Status: {online}')
        check_online(URL, config.CLIENT_ID, config.ACCEPT)
        time.sleep(5400)

    start_offline_loop()

def start_offline_loop():
    while online == False:
        print(f'[{get_time()}] Online Status: {online}')
        check_online(URL, config.CLIENT_ID, config.ACCEPT)
        time.sleep(10)

    start_online_loop()


if online == False:
    print('Offline loop started... ')
    start_offline_loop()
else:
    print('Online loop started...')
    start_online_loop()