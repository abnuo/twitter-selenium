import sys
import os
import pickle
import twitter_selenium

if not os.path.isfile("session.pkl"):
  username = input("Enter username or email: ")
  password = input("Enter password: ")
  session = twitter_selenium.TwitterSession(username,password)
  f = open("session.pkl","wb")
  pickle.dump(session.cookies,f)
  f.close()
else:
  cookies = pickle.load("session.pkl")
  session = twitter_selenium.TwitterSession(cookies=cookies)

try:
  text = sys.argv[1]
except:
  exit("No text was supplied.")

print(f"Tweeting -> {text}")
session.tweet(text)
