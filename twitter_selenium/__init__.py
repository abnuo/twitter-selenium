from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import os
import sysconfig
import pickle
drivers = {"firefox": webdriver.Firefox, "chrome": webdriver.Chrome}

def FixPath(path):
  if not path.startswith("/") or not path.startswith("C:\\"):
    return os.getcwd() + "\\" + path
  else:
    return path

def LoadSessionFile(sessionfile=sysconfig.get_paths()["purelib"]+"/twitter_selenium/session.pkl",driver="firefox",path=None,options=None):
  if not os.path.isfile(sessionfile):
    username = input("Enter username or email: ")
    password = input("Enter password: ")
    securityquestion = input("Enter security question (will be used if needed): ")
    session = TwitterSession(username,password,securityquestion,driver=driver,path=path,options=options)
    f = open(sessionfile,"wb")
    pickle.dump(session.cookies,f)
    f.close()
  else:
    f = open(sessionfile,"rb")
    cookies = pickle.load(f)
    session = TwitterSession(cookies=cookies,driver=driver,path=path,options=options)
  return session

class TwitterSession:
  def __init__(self,username=None,password=None,securityquestion=None,cookies=None,driver="firefox",options=None,path=None):
    if not path == None:
      self.driver = drivers[driver](options=options,executable_path=path)
    else:
      self.driver = drivers[driver](options=options)
    self.wait = WebDriverWait(self.driver, 50)
    if cookies == None:
      self.login(username,password,securityquestion)
    else:
      self.home()
      for i in cookies:
        self.driver.add_cookie(i)
      self.cookies = self.driver.get_cookies()
      self.home()
  def login(self,username,password,securityquestion=""):
    self.driver.get("https://twitter.com/i/flow/login")
    elem = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[autocomplete=username]")))
    elem.click()
    elem.send_keys(username)
    elem.send_keys(Keys.RETURN)
    elem = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[name=password]")))
    elem.send_keys(password)
    elem.send_keys(Keys.RETURN)
    try:
      WebDriverWait(self.driver, 5).until(EC.title_contains("Home / Twitter"))
    except:
      elem = self.driver.switch_to.active_element
      elem.send_keys(securityquestion)
    self.cookies = self.driver.get_cookies()
  def close(self):
    self.driver.close()
  def home(self):
    self.driver.get("https://twitter.com/home")
  def tweet(self,text,media=None):
    self.home()
    tweetinput = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".notranslate.public-DraftEditor-content")))
    tweetbutton = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid=tweetButtonInline]")))#//span[text()='Tweet']")))
    mediainput = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid=fileInput]")))
    tweetinput.click()
    tweetinput.send_keys(text)
    if not media == None:
      for i in media:
        path = FixPath(i)
        mediainput.send_keys(path)
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@aria-valuenow='0']")))
    try:
      tweetbutton.click()
    except:
      self.driver.execute_script("arguments[0].click();", tweetbutton)
    return self.wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(@class, 'css-4rbku5 css-18t94o4 css-901oao r-1kihuf0 r-jwli3a r-1loqt21 r-37j5jr r-a023e6 r-b88u0q r-rjixqe r-1b7u577 r-bcqeeo r-3s2u2q r-qvutc0')]"))).get_attribute("href")
  def like(self,id):
    self.driver.get(f"https://twitter.com/i/status/{id}")
    likebutton = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label=Like]")))
    likebutton.click()
  def retweet(self,id):
    self.driver.get(f"https://twitter.com/i/status/{id}")
    rtbutton = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label=Retweet]")))
    rtbutton.click()
  def unlike(self,id):
    self.driver.get(f"https://twitter.com/i/status/{id}")
    likebutton = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label=Liked]")))
    likebutton.click()
  def unretweet(self,id):
    self.driver.get(f"https://twitter.com/i/status/{id}")
    rtbutton = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label=Retweeted]")))
    rtbutton.click()
  def follow(self,username):
    self.driver.get(f"https://twitter.com/{username}")
    likebutton = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f"[aria-label='Follow @{username}' i]")))
    likebutton.click()
  def unfollow(self,username):
    self.driver.get(f"https://twitter.com/{username}")
    likebutton = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f"[aria-label='Following @{username}' i]")))
    likebutton.click()
  def gettweet(self,id):
    self.driver.get(f"https://twitter.com/i/status/{id}")
    description = None
    while True:
      description = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "meta[property='og:description']")))
      if not description.get_attribute("content") == "":
        break
    return description.get_attribute("content")[1:-1]
