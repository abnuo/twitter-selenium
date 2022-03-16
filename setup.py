from setuptools import setup

setup(
   name="twitter-selenium",
   version="1.1",
   description="Tweeting with selenium",
   packages=["twitter_selenium"],  #same as name
   install_requires=["selenium"], #external packages as dependencies
   scripts=[
            "scripts/tweet.py",
           ]
)
