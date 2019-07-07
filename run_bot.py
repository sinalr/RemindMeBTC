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
    

def search():
    global r
    global comments_dealt_with
    for subreddit in config.subreddits:
        print ("Obtaining 25 comments in " + subreddit)
        for comment in r.subreddit(subreddit).comments(limit=25):
            if ("RemindMeBTC!" in comment.body and comment.id not in comments_dealt_with and comment.author != r.user.me()):
                print ("String with \"RemindMeBTC!\" found in comment " + comment.id)
                thecomment = comment.body
                try:
                    if "RemindMeBTC!" in thecomment:
                      thecomment = thecomment.split(" ")
                      price = thecomment[1]
                      price = price.replace("$","")
                      price = price.replace(",","")
                      testing_if_int = int(price) + 25
                      try:
                        comment.reply("Alright, I'll send you a message if bitcoin hits $" + price + " USD")
                        print("Replying!")
                        with open ("need_to_message.txt", "a") as a:
                          a.write(str(comment.author) + " " + price + "\n")
                        comments_dealt_with.append(comment.id)
                        with open ("comments_dealt_with.txt", "a") as a:
                          a.write(comment.id + "\n")
                      except (praw.exceptions.APIException):
                        print("Rip Rate Limit :(")
                        time.sleep(10)
                except (AttributeError, ValueError, IndexError):
                    print ("Invalid formatting, ignoring")
                    comment.reply("Incorrect Formating :( \n \n use 'RemindMeBTC! price'")
                    comments_dealt_with.append(comment.id)
                    with open ("comments_dealt_with.txt", "a") as a:
                        a.write(comment.id + "\n")
                        
def message():
    global r
    global comments_dealt_with
    
    data = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")
    current_price = data.json()['bpi']['USD']['rate_float']
    print("Checking if I need to message anyone")
    
    with open("need_to_message.txt", "r") as b:
        need_to_message = [line.strip() for line in b if line.strip()]
        keep_lines = []
        
    for i in range (len(need_to_message)):
        splitted = need_to_message[i].split(" ")
        username = splitted[0]
        price = splitted[1]
        if not(current_price - 25 < float(price) < current_price + 25):
            keep_lines.append(need_to_message[i])
        else:
            r.redditor(username).message("Bitcoin Price Reminder", "You asked for a reminder when bitcoin hits the price of $" + price + " USD, and it is currently $" + str(current_price) + " USD. Thanks for using the RemindMeBTC Bot! I hope you reach your moon :)")
            print("Sent a message to /u/" + username)
    with open("need_to_message.txt", "w") as b:
        for i in range(len(keep_lines)):
            b.write(keep_lines[i] + "\n")
            
                        
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
    search()
    message()
    print("Sleeping for 10 sec...")
    time.sleep(10)