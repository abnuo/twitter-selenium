import sys
import os
import pickle
import twitter_selenium

if not os.path.isfile("session.pkl"):
  username = input("Enter username or email: ")
  password = input("Enter password: ")
  session = twitter_selenium.TwitterSession(username,password)
  pickle.dump(session.cookies,"session.pkl")
else:
  cookies = pickle.load("session.pkl")
  session = twitter_selenium.TwitterSession(cookies=cookies)

text = sys.argv[1]
print(f"Tweeting -> {text}")
session.tweet(text)
