import sys
import os
import pickle
import sysconfig
import twitter_selenium

sessionfile = sysconfig.get_paths()["purelib"]+"/twitter_selenium/session.pkl"

if not os.path.isfile(sessionfile):
  username = input("Enter username or email: ")
  password = input("Enter password: ")
  session = twitter_selenium.TwitterSession(username,password)
  f = open(sessionfile,"wb")
  pickle.dump(session.cookies,f)
  f.close()
else:
  cookies = pickle.load(sessionfile)
  session = twitter_selenium.TwitterSession(cookies=cookies)

try:
  text = sys.argv[1]
except:
  exit("No text was supplied.")

print(f"Tweeting -> {text}")
session.tweet(text)
