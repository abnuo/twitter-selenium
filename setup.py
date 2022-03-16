from setuptools import setup

setup(
   name="twitter-selenium",
   version="2.0",
   description="Tweeting with selenium",
   packages=["twitter_selenium"],
   install_requires=["selenium","BeautifulSoup4"],
   scripts=[
            "scripts/tweet.py",
           ]
)
