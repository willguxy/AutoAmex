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
  tmpoffernames = driver.find_elements_by_class_name("ah-card-offer-name") + \
    driver.find_elements_by_class_name("ah-offer-name")
  tmpnames = [n.text.encode('utf-8') for n in tmpoffernames]
  tmpnames = filter(None, tmpnames)
  # in the case of new GUI or nothing on old GUI
  if len(tmpnames) == 0:
    tmpoffernames = driver.find_elements_by_xpath("//*[contains(text(), 'Spend ') or contains(text(), 'Get ')]")
    tmpnames = [n.text.encode('utf-8') for n in tmpoffernames]
    # only keep object with valid text
    tmpoffernames = [tmpoffernames[i] for i in range(len(tmpoffernames)) if tmpnames[i] != '']
    tmpoffernames = [e.find_element_by_xpath('..') for e in tmpoffernames] # get parent
    tmpnames = [n.text.encode('utf-8') for n in tmpoffernames]
    tmpnames = filter(None, tmpnames)
    tmpnames = [n.split('\n')[1] for n in tmpnames]
  # update the method to retrieve offers in old GUI when offers exist
  else:
    tmpoffernames = driver.find_elements_by_xpath("//*[contains(text(), 'Spend ') or contains(text(), 'Get ')]")
    tmpnames = [n.text.encode('utf-8') for n in tmpoffernames]
    tmpnames = filter(None, tmpnames)
  print "Found " + str(len(tmpnames)) + " offers"
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
  elif browser.lower() in ('phantomjs', 'headless'):
    driver = webdriver.PhantomJS()
  else:
    print "WARNING: browser selection not valid, use PhantomJS as default"
    driver = webdriver.PhantomJS()
  # driver.maximize_window()
  # driver.set_window_size(1440, 900)
  # driver.set_window_position(0, 0)
  return driver


def loadConfig(filename):
  ''' load your config.csv file
    the file should contain username, password in each line
    make sure the file is under the same directory '''
  username = []
  password = []
  try:
    f = open(filename, 'rb')
    reader = csv.reader(f)
    for row in reader:
      username.append(row[0])
      password.append(row[1])
    f.close()
  except:
    print "file read failed..."
  return username, password


def closeFeedback(driver):
  try:
    driver.find_element_by_class_name("srCloseBtn").click()
  except:
    try:
      driver.find_element_by_class_name("fsrCloseBtn").click()
    except:
      pass
  time.sleep(1)


def clickViewMore(driver):
  driver.execute_script("window.scrollBy(0, 1250);") #scroll down
  # click on view more if available
  try:
    driver.find_element_by_xpath("//*[contains(text(), 'View More')]").click()
  except:
    for i in range(3):
      try:
        driver.find_elements_by_xpath("//*[contains(text(), 'View All')]")[1].click()
        time.sleep(2)
        return
      except:
        driver.execute_script("window.scrollBy(0, -250);") # scroll up
        pass
  time.sleep(2)


# click on Added to Card
def clickOnAddedToCard(driver):
  driver.execute_script("window.scrollBy(0, 1250);") # scroll down
  flag = True
  while flag:
    try:
      # driver.find_element_by_class_name("ah-addedCard").click()
      driver.find_element_by_xpath("//*[contains(text(), 'Added to Card')]").click()
      time.sleep(1)
      flag = False
    except:
      driver.execute_script("window.scrollBy(0, -150);")
      time.sleep(1)
      continue


def clickOnOffers(driver):
  for t in range(3):
    if collectOfferNames(driver) == '':
      print "All offers added"
      return
    time.sleep(1)
    try:
      driver.execute_script("javascript:$('.ah-card-offer-add-to-card').each(function(i){$(this).click();});")
    except:
      pass
    try:
      driver.execute_script("javascript:$('.ah-Add-to-card').each(function(i){$(this).click();});")
    except:
      pass
    #try:
    #  driver.execute_script("javascript:$('.offer-cta').each(function(i){$(this).click();});")
    #except:
    #  pass
    try:
      [e.click() for e in driver.find_elements_by_xpath('//*[@title="Add to Card"]')]
    except:
      pass
    time.sleep(1)
    if t != 2:
      driver.refresh() # refresh the page
      time.sleep(1)
      clickViewMore(driver)


def clickOnLoadMore(driver):
  driver.execute_script("window.scrollBy(0, 1250);") # scroll down
  # click on 'load more'
  try:
    driver.find_element_by_xpath("//*[contains(text(), 'Load More')]").click()
  except:
    for i in range(3):
      try:
        driver.find_elements_by_xpath("//*[contains(text(), 'View All')]")[1].click()
        time.sleep(2)
        return
      except:
        driver.execute_script("window.scrollBy(0, -250);") # scroll up
        pass
  time.sleep(2)


def amexLogIn(driver, usr, pwd):
  emailFieldID = "lilo_userName"
  passFieldID = "lilo_password"
  loginBtnID= "lilo_formSubmit"
  viewMoreBtn = "ah-view-more-button"
  WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id(emailFieldID)).clear()
  WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id(emailFieldID)).send_keys(usr)
  WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id(passFieldID)).clear()
  WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id(passFieldID)).send_keys(pwd)
  WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id(loginBtnID)).click()
  time.sleep(3)


def amexLogOut(driver):
  logoutBtnID = "iNavLogOutButton"
  WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id(logoutBtnID)).click()


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





