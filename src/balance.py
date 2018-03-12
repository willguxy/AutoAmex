#!/usr/bin/env python
import sys, time
from selenium import webdriver
from datetime import datetime
from helper import loadConfig, closeFeedback, amexLogIn, \
  amexLogOut, getDriver, getBalance

amex_url = 'https://global.americanexpress.com/dashboard'

def loginTest(cred, browser="PhantomJS"):
  logfilename = 'balance_' + datetime.strftime(datetime.now(), '%Y-%m-%d %H_%M_%S') + '.log'
  with open('../tmp/' + logfilename, 'w+') as f:
    sys.stdout = f 
    driver = getDriver(browser)
    i, t0  = 1, time.time()
    for login_pair in cred:
      try:
        driver.get(amex_url)
        amexLogIn(driver, login_pair[0], login_pair[1], 'eliloUserID', 'eliloPassword')
      except:
        print("# {0} ID: {1} Something is wrong with login".format(i, login_pair[0]))
        continue
      time.sleep(2)
      closeFeedback(driver)
      bal = getBalance(driver)
      print("# {0} ID: {1} Balance: {2}".format(i, login_pair[0], bal))
      i += 1
      while not driver.find_elements_by_id('eliloUserID'):
        try: amexLogOut(driver)
        except: pass
    driver.quit()
    print("** Summary **\nTotal time used: %0.1f seconds" % (time.time() - t0))

def main(argv):
  browser = argv[0] if len(argv) >= 1 else 'Chrome'
  loginTest(loadConfig("../conf/major.csv"), browser=browser)

if __name__ == '__main__':
  main(sys.argv[1:])


