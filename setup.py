from setuptools import setup

setup(
   name="twitter-selenium",
   version="1.3",
   description="Tweeting with selenium",
   packages=["twitter_selenium"],
   install_requires=["selenium"],
   scripts=[
            "scripts/tweet.py",
           ]
)
