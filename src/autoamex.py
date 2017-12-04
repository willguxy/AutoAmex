#!/usr/bin/env python
import sys, time
from selenium import webdriver
from datetime import datetime
from helper import loadConfig, closeFeedback, clickOnOffers, amexLogIn, \
  amexLogOut, getDriver, collectOfferNames

amex_url = 'https://global.americanexpress.com/offers/eligible'

def loginTest(cred, browser = "PhantomJS"):
  logfilename = datetime.strftime(datetime.now(), '%Y-%m-%d %H_%M_%S') + '.log'
  with open('../tmp/' + logfilename, 'w+') as f:
    sys.stdout = f 
    driver = getDriver(browser)
    i, t0  = 1, time.time()
    for login_pair in cred:
      t = time.time()
      print("# {0} ID: {1}".format(i, login_pair[0]))
      try:
        driver.get(amex_url)
        amexLogIn(driver, login_pair[0], login_pair[1], 'eliloUserID', 'eliloPassword')
      except:
        print("Something is wrong with login")
        continue
      closeFeedback(driver) 
      offer_names = collectOfferNames(driver)
      print("Available offers are: {}".format(offer_names))
      if offer_names: clickOnOffers(driver)
      try: amexLogOut(driver)
      except: pass
      time.sleep(1)
      print("Time used: %0.1f seconds\n" % (time.time() - t))
      i += 1
    driver.quit()
    print("** Summary **\nTotal time used: %0.1f seconds" % (time.time() - t0))

def main(argv):
  browser = argv[0] if len(argv) >= 1 else 'Chrome'
  loginTest(loadConfig("../conf/config.csv"), browser=browser)

if __name__ == '__main__':
  main(sys.argv[1:])


