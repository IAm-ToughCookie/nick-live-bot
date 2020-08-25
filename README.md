# nick-live-bot
A bot that reminds Nick that he is live. 

## 💡 Idea:
My friend Nick always forgets to tweet when he goes live, so I jokingly said I'd make a bot that will do it for him. He dared me to do it, and two days later, here we are. 

## 📖 Project:
Simple python script that checks the twitch-kraken-API for the status of the stream every 10 seconds while he is offline if the status changes to online it will fire a message to the twitter-API to send a tweet. The tweet only goes out once for every time he goes online. 

## 🐍 Script:
The scripts runtime start with getting the initial state of the stream (either true for online or false for offline). 
After getting the initial script ran it checks for the status if the stream is on, it will send the tweet with the game and link fetched from the twitch-api and set a variable to true so the script knows a tweet has been send. 
It will check every 5400s (90min) if the stream is still online. If not, it will set the online- and tweet_send-variable to false and basically reset the cycle. 
From there on out it will check every 10 seconds if the stream is online again.

## 🌍 Hosting:
I have never hosted a python script on production before, so I don't know if I did it correctly.
I hosted the script on AWS-EC2. 🤷‍♂️
It's running, so I suppose that's worth something?

## 🔑 Keys and Secrets:
All API-Keys and Secrets are located in a config.py-file that gets imported into main script so they are never exposed, I think.  