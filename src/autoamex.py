#!/usr/bin/env python

from selenium import webdriver
from datetime import datetime
import sys
import time
from helper import loadConfig, closeFeedback, clickViewMore, clickOnOffers, amexLogIn, \
  amexLogOut, clickOnLoadMore, getDriver

amexWebsite = "https://online.americanexpress.com/myca/logon/us/action/LogonHandler?request_type=LogonHandler&Face=en_US&inav=iNavLnkLog"

def loginTest(username, password, outputlog = True, browser = "PhantomJS"):
  orig_stdout = sys.stdout # re-route output
  logfile = None
  if outputlog:
    # use current time in log file name
    logfilename = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
    logfilename = logfilename.replace(':', '_') + ".log"
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

  driver = getDriver(browser)
  begintime  = time.time()

  # loop through all username/password combinations
  for idx in range(len(username)):
    eachbegintime = time.time()
    print "--------------------------------------------------------------"
    print "#", idx+1, "ID:", username[idx]
    # just in case network connection is broken 
    try:
      driver.get(amexWebsite)
    except:
      print "website is not available..."
      if outputlog:
        sys.stdout = orig_stdout
        logfile.close() # close log file
      return

    # fill and submit login form
    try:
      amexLogIn(driver, username[idx], password[idx])
    except:
      print "Something is wrong with login"
      continue # end current loop

    closeFeedback(driver) # just in case the feedback banner appears
    clickOnLoadMore(driver) # scroll down and click load more

    # store offer names and click on offers
    tmpoffernames = driver.find_elements_by_class_name("ah-card-offer-name") + \
      driver.find_elements_by_class_name("ah-offer-name")
    tmpnames = [n.text.encode('utf-8') for n in tmpoffernames]
    tmpnames = filter(None, tmpnames)
    print "Available offers are:", ', '.join(tmpnames)
    clickOnOffers(driver)
      
    # logout
    try:
      amexLogOut(driver)
    except:
      pass # pass would be fine, since the launch of the url is the log-in page no matter what
    time.sleep(1)

    eachendtime = time.time()
    print "Time used: %0.2f seconds" % (eachendtime - eachbegintime)
    print "--------------------------------------------------------------"

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
  # close browser
  driver.quit()


def main():
  username, password = loadConfig("../conf/config.csv")
  loginTest(username, password, outputlog = True, browser = "PhantomJS")

if __name__ == '__main__':
  main()


