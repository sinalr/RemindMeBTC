import praw
import config
import time
import os
import random
import re
import requests

def bot_login():
    print ("Loggin in...")
    global r
    r = praw.Reddit(username = config.username,
            password = config.password,
            client_id = config.client_id,
            client_secret = config.client_secret,
            user_agent = config.user_agent)
    print ("Logged in!")
    
def run_bot():
    global r
    global comments_dealt_with
    for subreddit in config.subreddits:
        print ("Obtaining 25 comments in " + subreddit)
        for comment in r.subreddit(subreddit).comments(limit=25):
            if ("RemindMeBTC!" in comment.body and comment.id not in comments_dealt_with and comment.author != r.user.me()):
                print ("String with \"RemindMeBTC!\" found in comment " + comment.id)
                thecomment = comment.
                try:
                    if "RemindMeBTC!" in thecomment:
                      thecomment = thecomment.split(" ")
                      price = thecomment[1]
                      comment.reply("Alright, I'll send you a message when bitcoin hits " + price)
                      print("Replying!")
                      with open ("need_to_.txt", "a") as a:
                        a.write(comment.author + " " + price + "\n")
                      comments_dealt_with.append(comment.id)
                      with open ("comments_dealt_with.txt", "a") as a:
                        a.write(comment.id + "\n")
                except (AttributeError, ValueError):
                    print ("Invalid formatting, ignoring")
                    comments_dealt_with.append(comment.id)
                    with open ("comments_dealt_with.txt", "a") as a:
                        a.write(comment.id + "\n")
                    continue
                
                
def get_saved_comments():
    global comments_dealt_with
    if not os.path.isfile("comments_dealt_with.txt"):
        comments_dealt_with = []
    else:
        with open("comments_dealt_with.txt", "r") as f:
            comments_dealt_with = f.read()
            comments_dealt_with = comments_dealt_with.split("\n")
            #comments_dealt_with = filter(None, comments_dealt_with)


bot_login()
get_saved_comments()

while True:
    run_bot()