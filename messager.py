import praw
import config
import time
import os
import random
import re
import requests

def bot_login():
    print ("Logging in...")
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
    
    data = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")
    current_price = data.json()['bpi']['USD']['rate_float']
    
    with open("need_to_message.txt", "r") as b:
        need_to_message = b.read()
        need_to_message = need_to_message.split("\n")
        
    for i in range(len(need_to_message)):
        splitted = need_to_message[i].split(" ")
        username = splitted[0]
        price = intsplitted[1]
        if (current_price - 100 < float(price) < current_price + 100):
            r.redditor(username).message("Bitcoin Price Reminder", "You asked for a reminder when bitcoin hits the price of $" + price + " USD, well it is currently $" + current_price + "USD")
            print("Sent a message to /u/" + username)
            with open("need_to_message.txt", "w") as b:
                lines = b.readlines()
                for line in lines:
                    if line != need_to_message[i]:
                        b.write(line)
            
            


bot_login()
while True:
    run_bot()