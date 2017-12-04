#!/usr/bin/env python
import sys, time
from selenium import webdriver
from datetime import datetime
from helper import loadConfig, closeFeedback, clickOnOffers, amexLogIn, \
  amexLogOut, getDriver, collectOfferNames

amex_url = 'https://global.americanexpress.com/offers/eligible'

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
    print("username array does not have the same length as password array...")
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
    print("--------------------------------------------------------------")
    print("#", idx+1, "ID:", username[idx])
    # just in case network connection is broken
    try: driver.get(amex_url)
    except:
      print("website is not available...")
      if outputlog:
        sys.stdout = orig_stdout
        logfile.close() # close log file
      return

    # fill and submit login form
    try: amexLogIn(driver, username[idx], password[idx], 'eliloUserID', 'eliloPassword')
    except:
      print("Something is wrong with login")
      continue # end current loop

    closeFeedback(driver) # just in case the feedback banner appears

    # store offer names and click on offers
    offernames = collectOfferNames(driver)
    print("Available offers are: {}".format(offernames))
    if not offernames == '': clickOnOffers(driver)
    try:  amexLogOut(driver)
    except: pass
    time.sleep(1)

    eachendtime = time.time()
    print("Time used: %0.2f seconds" % (eachendtime - eachbegintime))
    print("--------------------------------------------------------------")

  endtime = time.time()
  # print summary
  print("--------------------------------------------------------------")
  print("** Summary **")
  print("Total time used: %0.2f seconds" % (endtime - begintime))
  print("--------------------------------------------------------------")

  # close log file
  if outputlog:
    sys.stdout = orig_stdout
    logfile.close()
  # close browser
  driver.quit()


def main(argv):
  browser = 'Chrome'
  if len(argv) >= 1:
    browser = argv[0]
  username, password = loadConfig("../conf/config.csv")
  loginTest(username, password, outputlog=True, browser=browser)

if __name__ == '__main__':
  main(sys.argv[1:])


