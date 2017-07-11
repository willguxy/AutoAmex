#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime
import sys
import time
from helper import loadConfig, twitterLogIn, twitterLogOut, getDriver

website = "https://twitter.com/download?logged_out=1&lang=en"


def skipAddPhoneNumber(driver):
  try:
    driver.find_element_by_class_name("js-promptDismiss").click()
    # driver.find_element_by_class_name("modal-btn js-promptDismiss modal-close js-close").click()
    # document.getElementsByClassName("modal-btn js-promptDismiss modal-close js-close")[0].click()
  except:
    try:
      driver.find_element_by_class_name("Icon Icon--close Icon--medium").click()
    except:
      pass


def clickOnNotifications(driver):
  driver.find_element_by_class_name("people notifications").click()


def clickOnBanner(driver):
  try:
    driver.find_element_by_class_name("EdgeButton EdgeButton--primary js-promptAction").click()
  except:
    pass


def sendTweet(driver, text):
  driver.find_element_by_id("global-new-tweet-button").click()
  time.sleep(1)
  WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id("tweet-box-global")).send_keys(text)
  driver.find_elements_by_class_name("Icon--tweet")[2].click()
  print("Send tweet OK [%s]" % text)
  time.sleep(1)


def loginTest(username, password, outputlog = True, tweet = None):
  # re-route output
  orig_stdout = sys.stdout
  logfile = None
  if outputlog:
    # use current time as log file
    logfilename = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
    logfilename = "twitter_" + logfilename.replace(':', '_') + ".log"
    logfile = open('../tmp/' + logfilename, 'w+')
    sys.stdout = logfile
  # input error handle
  if username == [] or password == [] or len(username) != len(password):
    print "username array does not have the same length as password array..."
    # close log file
    if outputlog:
      sys.stdout = orig_stdout
      logfile.close()
    return

  begintime  = time.time()

  # loop through all username/password combinations
  for idx in range(len(username)):
    driver = getDriver('chrome')
    print "--------------------------------------------------------------"
    print "#%s ID:%s" % (idx+1, username[idx])
    # just in case network connection is broken 
    try:
      driver.get(website)
    except:
      print "website is not available..."
      # close log file
      if outputlog:
        sys.stdout = orig_stdout
        logfile.close()
      driver.quit()
      return

    time.sleep(2)

    # login
    try:
      twitterLogIn(driver, username[idx], password[idx])
    except:
      print "username/password combination is incorrect..."
      print "--------------------------------------------------------------"
      continue # end current loop

    time.sleep(2)
    skipAddPhoneNumber(driver)
    clickOnBanner(driver)
    time.sleep(1)

    # main program
    status = 'unknown'
    try:
      driver.find_element_by_id("challenge_response")
      status = 'challenge'
    except:
      pass

    try:
      driver.find_element_by_id("global-new-tweet-button")
      status = 'OK'
    except:
      pass

    try:
      driver.find_element_by_id("account-suspended")
      status = 'suspended'
    except:
      pass

    print "Status: %s" % status
    if status in ('challenge', 'suspended'):
      print "have to skip this one..."
      driver.quit() # close browser
      continue
    time.sleep(1)

    if not tweet is None:
      try:
        sendTweet(driver, tweet)
        time.sleep(1)
      except:
        print "can't send tweet"
        pass
    driver.get("https://twitter.com/i/notifications")  # load notification page
    time.sleep(1)

    if status != 'challenge':
      # logout
      try:
        twitterLogOut(driver)
      except:
        print "Error: Cannot find logout button [%s]" % username[idx]
        time.sleep(10)
        if outputlog:
          sys.stdout = orig_stdout
          logfile.close()
        driver.quit()
    print "--------------------------------------------------------------"

    driver.refresh()
    time.sleep(2)
    try:
      twitterLogOut(driver)
    except:
      pass

    driver.quit() # close browser
  
  endtime = time.time()
  # print summary
  print "--------------------------------------------------------------"
  print "** Summary **"
  print "Total time used: %0.2f seconds" % (endtime - begintime)
  print "--------------------------------------------------------------"

  # close log file
  if outputlog:
    sys.stdout = orig_stdout
    logfile.close()


def main(argv):
  username, password = loadConfig("../conf/twitter_config.csv")
  # username = username[40:]
  # password = password[40:]
  text = None
  if len(argv) >= 1:
    text = ' '.join(argv)
  else:
    with open('hashtags.txt') as f:
      text = f.readline()
  loginTest(username, password, outputlog = True, tweet = text)

if __name__ == '__main__':
  main(sys.argv[1:])


