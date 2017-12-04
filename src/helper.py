# helper files for amex automation

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import csv
import time
from random import choice
import string

# TODO: Add these websites to actions
# Only working on the new GUI
offer_page = "https://global.americanexpress.com/offers/eligible"
added_page = "https://global.americanexpress.com/offers/enrolled"

def GenPasswd2(length=8, chars=string.letters + string.digits):
  return ''.join([choice(chars) for i in range(length)])

def genRandomText():
  return GenPasswd2(8,string.digits) + GenPasswd2(15,string.ascii_letters)

def collectOfferNames(driver):
  tmpoffernames = driver.find_elements_by_xpath("//*[contains(text(), 'Add to Card') \
    or contains(text(), 'Save Promo Code')]/../../..")
  tmpnames = [n.text.encode('utf-8') for n in tmpoffernames]
  tmpoffernames = [tmpoffernames[i] for i in range(len(tmpoffernames)) if tmpnames[i] != '']
  tmpnames = [n.text.encode('utf-8') for n in tmpoffernames]
  tmpnames = filter(None, tmpnames)
  tmpnames = [n.split('\n')[1] if '\n' in n else n for n in tmpnames]
  offernames = ', '.join(tmpnames)
  return offernames


def getDriver(browser):
  chrome_options = webdriver.ChromeOptions()
  chrome_options.add_argument("--incognito")
  chrome_options.add_argument("--window-size=1440,900")
  if browser.lower() == 'firefox':
    driver = webdriver.Firefox()
  elif browser.lower() == 'chrome':
    driver = webdriver.Chrome('./chromedriver', chrome_options=chrome_options)
  elif browser.lower() == 'chrome_linux':
    driver = webdriver.Chrome('./chromedriver_linux64', chrome_options=chrome_options)
  elif browser.lower() in ('phantomjs', 'headless'):
    driver = webdriver.PhantomJS()
  else:
    print "WARNING: browser selection not valid, use PhantomJS as default"
    driver = webdriver.PhantomJS()
  return driver


def loadConfig(filename):
  res = []
  with open(filename, 'rb') as f:
    reader = csv.reader(f)
    for row in reader: res.append(row)
  return res


def closeFeedback(driver):
  try:
    driver.find_element_by_class_name("srCloseBtn").click()
  except:
    try:
      driver.find_element_by_class_name("fsrCloseBtn").click()
    except:
      pass


def clickOnViewMore(driver):
  driver.execute_script("window.scrollBy(0, 2250);") #scroll down
  # click on view more if available
  try:
    driver.find_element_by_xpath("//*[contains(text(), 'View More')]").click()
  except:
    for i in range(3):
      try:
        driver.find_element_by_xpath("//*[contains(text(), 'View All')]")[1].click()
        time.sleep(2)
        return
      except:
        driver.execute_script("window.scrollBy(0, -250);") # scroll up
        pass
  time.sleep(2)


# click on Added to Card
def clickOnAddedToCard(driver):
  driver.execute_script("window.scrollBy(0, 2250);") # scroll down
  flag = True
  while flag:
    try:
      driver.find_element_by_xpath("//*[contains(text(), 'Added to Card')]").click()
      time.sleep(1)
      flag = False
    except:
      driver.execute_script("window.scrollBy(0, -150);")
      time.sleep(1)
      continue


def clickOnOffers(driver):
  for t in range(3):
    if collectOfferNames(driver) == '': return
    for e in driver.find_elements_by_xpath('//*[@title="Add to Card"]') + \
            driver.find_elements_by_xpath('//*[@title="Save Promo Code"]'):
      try: e.click()
      except: pass
      time.sleep(1)
    if t != 2:
      driver.refresh() # refresh the page
      time.sleep(1)


def clickOnLoadMore(driver):
  driver.execute_script("window.scrollBy(0, 2250);") # scroll down
  # click on 'load more'
  try:
    driver.find_element_by_xpath("//*[contains(text(), 'Load More')]").click()
  except:
    for i in range(3):
      try:
        driver.find_elements_by_xpath("//*[contains(text(), 'View All')]")[5].click()
        time.sleep(2)
        return
      except:
        driver.execute_script("window.scrollBy(0, -250);") # scroll up
        pass
  time.sleep(2)


def amexLogIn(driver, usr, pwd, emailFieldID='lilo_userName', passFieldID='lilo_password'):
  WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id(emailFieldID)).clear()
  WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id(emailFieldID)).send_keys(usr)
  WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id(passFieldID)).clear()
  WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id(passFieldID)).send_keys(pwd)
  for e in driver.find_elements_by_xpath('//*[@type="submit"]'):
    try: e.click()
    except: pass
  time.sleep(3)


def amexLogOut(driver):
  for e in driver.find_elements_by_xpath('//*[@tabindex="0" and @accesskey="4"]'):
    try: e.click()
    except: pass


def twitterLogIn(driver, usr, pwd):
  signInLinkID = "signin-link"
  loginBtnClass = "submit"
  emailField = "session[username_or_email]"
  pwdField = "session[password]"
  WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id(signInLinkID)).click()
  WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_name(emailField)).send_keys(usr)
  WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_name(pwdField)).send_keys(pwd)
  WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_class_name(loginBtnClass)).click()


def twitterLogOut(driver):
  userDropdownID = "user-dropdown-toggle"
  signOutBtn = "js-signout-button"
  WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id(userDropdownID)).click()
  WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_class_name(signOutBtn)).click()





