import tweepy
import logging
import time
import random
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
from config import create_api


def fav_retweet_user(api, user_handle):
    search_query = f"{user_handle} -filter:retweets"
    logger.info(f'Retrieving tweets mentioning {user_handle}...')
    tweets = api.search(q=search_query, lang ="en")
    for tweet in tweets:
        if tweet.in_reply_to_status_id is not None or \
            tweet.user.id == api.me().id:
            # This tweet is a reply or I'm its author so, ignore it
            return
        if not tweet.favorited:
            # Mark it as Liked, since we have not done it yet
            try:
                tweet.favorite()
                logger.info(f"Liked a tweet mentioning {user_handle}")
            except Exception as e:
                logger.error("Error on fav", exc_info=True)
        if not tweet.retweeted:
            # Retweet, since we have not retweeted it yet
            try:
                tweet.retweet()
                logger.info(f"Retweeted a tweet mentioning {user_handle}")
            except Exception as e:
                logger.error("Error on fav and retweet", exc_info=True)

def retweet_tweets_with_hashtag(api, need_hashtags):
    if type(need_hashtags) is list:
        search_query = f"{need_hashtags} - filter:retweets"
        tweets = api.search(q=search_query, lang ="en", tweet_mode='extended', count=20, result_type="mixed")
        for tweet in tweets:
            logger.debug(tweet)
            hashtags = [i['text'].lower() for i in tweet.__dict__['entities']['hashtags']]
            try:
                need_hashtags = [hashtag.strip('#') for hashtag in need_hashtags]
                need_hashtags = list(need_hashtags)
                if set(hashtags) & set(need_hashtags):
                    if tweet.user.id != api.me().id:
                        api.retweet(tweet.id)
                        logger.info(f"Retweeted tweet from {tweet.user.name}")
                        time.sleep(5)
            except tweepy.TweepError:
                logger.error("Error on retweet", exc_info=True)
    else:
        logger.error("Hashtag search terms needs to be of type list", exc_info=True) 
        return
def fav_retweet(api):
    logger.info('Retrieving tweets...')
    mentions = api.mentions_timeline(tweet_mode = 'extended')
    for mention in reversed(mentions):
        if mention.in_reply_to_status_id is not None or mention.user.id == api.me().id:
            # This tweet is a reply or I'm its author so, ignore it
            return
        # 
        # if mention.in_reply_to_status_id is mention.user.id == api.me().id:
        if not mention.favorited:
            # Mark it as Liked, since we have not done it yet
            try:
                mention.favorite()
                logger.info(f"Liked tweet by {mention.user.name}")
            except Exception as e:
                logger.error("Error on fav", exc_info=True)
                
        if not mention.retweeted:
            # Retweet, since we have not retweeted it yet
            try:
                mention.retweet()
                logger.info(f"Retweeted tweet by {mention.user.name}")
            except Exception as e:
                logger.error("Error on fav and retweet", exc_info=True)

def retweet_tweets_with_ticker(api, need_ticker):
    if type(need_ticker) is list:
        search_query = f"{need_ticker} -filter:retweets"
        tweets = api.search(q=search_query, lang ="en", tweet_mode='extended')
        for tweet in tweets:
            ticker = [i['text'].lower() for i in tweet.__dict__['entities']['symbols']]
            try:
                need_ticker = [hashtag.strip('$') for hashtag in need_ticker]
                need_ticker = list(need_ticker)
                if set(ticker) & set(need_ticker):
                    if tweet.user.id != api.me().id:
                        api.retweet(tweet.id)
                        logger.info(f"Retweeted tweet from {tweet.user.name}")
                        time.sleep(5)
            except tweepy.TweepError:
                logger.error("Error on retweet", exc_info=True)
    else:
        logger.error("Hashtag search terms needs to be of type list", exc_info=True) 
        return               
def main():
    api = create_api()
    while True:
        fav_retweet(api)
        retweet_tweets_with_hashtag(api, ["#passs386"])
        # fav_retweet_user(api, "@GCBCoalition")
        # @immivoice
        
        logger.info("Waiting...")
        time.sleep(30)

if __name__ == "__main__":
    main()  
