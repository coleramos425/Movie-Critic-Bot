# -*- coding: utf-8 -*-
import config
import os
import random
import markovify
import tweepy
import json

# -- SETUP TWITTEER API --

auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)

api = tweepy.API(auth)

# -- RANDOMLY PICK MOVIE --

# 7 movie choices
spiderTags = {
    0: ("bill", "Kill Bill: Vol 1."),
    1: ("django", "Django Unchained"),
    2: ("dog", "Reservoir Dogs"),
    3: ("eight", "The Hateful Eight"),
    4: ("hollywood", "Once Upon a Time… In Hollywood"),
    5: ("inglor", "Inglorious B*sterds"),
    6: ("pulp", "Pulp Fiction")
}

randIndx = random.randint(0,6) #pick a random movie to review
abrevTitle = spiderTags[randIndx][0]
fullTitle = spiderTags[randIndx][1]

# scrape movie reviews for selected movie, generate json
os.chdir(os.getcwd() + '/moviedata')
print(os.getcwd())
# call my spider I created. This lives inside the moviedata folder!
os.system("scrapy crawl " + abrevTitle +" -O results.json")
    
# -- SCRAPE REVIEWS INTO TXT --
print(os.getcwd())
f = open(os.getcwd()+'/results.json', "r")
jStr = f.read()
listOfD = json.loads(jStr)

# generate a list of reviews
reviews = []
for d in listOfD:
    reviews.append(d['review_text'].strip())
f.close()

# make .txt to sent to Markovify
txtfile = open("corpus.txt", "w")
for element in reviews:
    txtfile.write(element + "\n")
txtfile.close()

# -- READ INTO MARKOVIFY --

with open("corpus.txt") as f:
    text = f.read()

text_model = markovify.NewlineText(text) # build the model

maxSize = 280 - (len(fullTitle)+4)
origReview = text_model.make_short_sentence(maxSize)
tweet = "[" + fullTitle + "]: " + origReview
print(tweet)


# -- SEND ORIGINAL REVIEW TO TWITTER --

api.update_status(tweet)
print("I just posted a tweet!")