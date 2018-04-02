from twitter import Api
from tweet_window import *

import tweet_window as tw
import os
import time
import argparse
import sys
import twitter
import csv
import json

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
        self.num_of_msg = 0
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
        
        self.search_follow_list = None if self.search_follow == "" else self.search_follow.split(',')    
        self.search_track_list = None if self.search_track == "" else self.search_track.split(',')
    
    def run(self):
        # # api.GetStreamFilter will return a generator that yields one status
        # # message (i.e., Tweet) at a time as a JSON dictionary.
        try:
            stream =self.api.GetStreamFilter(track=self.search_track_list, 
                languages=self.languages, locations=self.search_location, 
                follow=self.search_follow_list)
                             
            with open(self.file_save_path, 'a', encoding="utf-8") as f:
                # f_writer = csv.writer(f)
                # data = twitter.Status.NewFromJsonDict(tweet)
                # # TODO: problem: streaming stops when we add more field such as data.retweet_count, data.favorite_count etc
                # row = [data.created_at, data.id, data.user.screen_name, data.user.time_zone, data.user.location, data.text]               
                # f_writer.writerow(row)
                
                for line in stream:
                    f.write(str(line))
                    # TODO: seems like this if condition doesn't work
                    # need to find a way to communicate between tweet_mine and tweet_window
                    if tw.mine_status is not True:
                        break
                        
        except Exception as e:
            print("ERROR: " + repr(e))
        
        
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
    # sys.exit(0)
    tm = TweetMine(config_args=args)
    tm.run()
    sys.exit(0)
