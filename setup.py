from setuptools import setup

setup(
   name="twitter-selenium",
   version="3.2",
   description="Tweeting with selenium",
   packages=["twitter_selenium"],
   install_requires=["selenium","BeautifulSoup4"],
   scripts=[
            "scripts/tweet.py",
           ]
)
