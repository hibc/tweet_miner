from twitter import Api
from twitter import error
from tweet_window import *

import tweet_window as tw
import os
import time
import argparse
import sys
# import json

'''
follow:
    A list of user IDs to track. [Optional]
track:
    A list of expressions to track. [Optional]
locations:
    A list of Longitude,Latitude pairs (as strings) specifying
    bounding boxes for the tweets' origin. [Optional]
delimited:
    Specifies a message length. [Optional]
stall_warnings:
    Set to True to have Twitter deliver stall warnings. [Optional]
languages:
    A list of Languages.
    Will only return Tweets that have been detected as being
    written in the specified languages. [Optional]
'''
    
class TweetMine():
    def __init__(self, config_args=None):
        self.numer_of_msg = 0
        self.api = None
        self.consumer_key = config_args.consumer_key
        self.consumer_secret = config_args.consumer_secret
        self.access_token = config_args.access_token
        self.access_secret = config_args.access_secret

        self.search_location = config_args.locations
        self.search_language = config_args.languages
        self.search_track = config_args.track
        self.search_follow = config_args.follow

        self.file_save_path = config_args.file_path
        self.languages = []
        self.search_track_list = []
        self.search_follow_list = []

        self.set_twitter_config_API()
        self.set_search_config()
    
    def set_twitter_config_API(self):
        
        try:
            self.api = Api(consumer_key=self.consumer_key, consumer_secret=self.consumer_secret,
            access_token_key=self.access_token, access_token_secret=self.access_secret)
        except Exception as e:
            print(e)

    def set_search_config(self):
        
        if self.search_language is None or self.search_language == '':
            self.languages = ['en']
        else:
            self.languages=[self.search_language]
        
        self.search_follow_list = None if self.search_follows == "" else self.search_follows.split(',')    
        self.search_track_list = None if self.search_track == "" else self.search_track.split(',')
    
    def run(self):
        num_of_tweets = 0
        # # api.GetStreamFilter will return a generator that yields one status
        # # message (i.e., Tweet) at a time as a JSON dictionary.
        try:
            for tweet in self.api.GetStreamFilter(track=self.search_track_list, 
                languages=self.languages, locations=self.search_location, 
                follow=self.search_follow_list):
                num_of_tweets += 1

                # it might be good to write to a file
                # instead keep tweets int a memory
                with open(self.file_save_path, 'a') as f:
                    f.write(str(tweet))

                if tw.mine_status != True:
                    break
                    
        except Exception as e:
            print("ERROR: " + repr(e))
        
        print("Mining has stopped..")
        print('Total number of tweet: {0}'.format(num_of_tweets))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='arguments for Tweet Mining')
    parser.add_argument('--consumer_key', type=str)
    parser.add_argument('--consumer_secret', type=str)
    parser.add_argument('--access_token', type=str)
    parser.add_argument('--access_secret', type=str)
    
    parser.add_argument('--locations', type=str, default=None)
    parser.add_argument('--languages', type=str, default=None)
    parser.add_argument('--follow', type=str, default=None)
    parser.add_argument('--track', type=str)

    parser.add_argument('--file_path', type=str)
    args = parser.parse_args()

    print("\nconsumer_key: {0}\nconsumer_secret: {1}\naccess_token: {2}\naccess_secret: {3}\n".format(args.consumer_key, args.consumer_secret, args.access_token, args.access_secret))
    print("location: {0}\nlaunguages: {1}\nfollow: {2}\ntrack: {3}\n".format(args.locations, args.languages, args.follow, args.track))
    print("file_path: {0}\n".format(args.file_path))
    # sys.exit(0)
    tm = TweetMine(config_args=args)
    tm.run()
