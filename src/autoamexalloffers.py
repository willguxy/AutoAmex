#!/usr/bin/env python

from selenium import webdriver
from datetime import datetime
import sys
import time
from datetime import datetime as dt
from helper import loadConfig, closeFeedback, clickOnAddedToCard, clickOnLoadMore, amexLogIn, amexLogOut, getDriver

amexWebsite = "https://online.americanexpress.com/myca/logon/us/action/LogonHandler?request_type=LogonHandler&Face=en_US&inav=iNavLnkLog"


def getAddedOffers(username, password, outputlog = True, browser = "Chrome"):
  # re-route output
  orig_stdout = sys.stdout
  logfile = None
  if outputlog:
    # use current time as log file
    logfilename = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
    logfilename = "offers " + logfilename.replace(':', '_') + ".csv"
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

  # use phantom JS / Firefox
  # driver = webdriver.PhantomJS()
  # driver = webdriver.Firefox()
  driver = getDriver(browser) 
  majorOfferDescMap = dict()
  majorOfferDateMap = dict()
  majorDateOfferPair = set()
  userOffersList = []

  # loop through all username/password combinations
  for idx in range(len(username)):
    eachbegintime = time.time()
    try:
      driver.get(amexWebsite)
    except:
      print "website is not available..."
      # close log file
      if outputlog:
        sys.stdout = orig_stdout
        logfile.close()
      return
    # fill and submit login form
    try:
      amexLogIn(driver, username[idx], password[idx])
    except:
      print "username/password combination is incorrect..."
      continue
    time.sleep(2)
    closeFeedback(driver)
    clickOnAddedToCard(driver)
    clickOnLoadMore(driver)

    # main program
    offers = driver.find_elements_by_class_name("ah-card-offer")
    offerstext = [offer.text.encode('utf-8') for offer in offers]
    offersplit = [text.split('\n') for text in offerstext]
    offerDescMap = dict()
    offerDateMap = dict()
    dateOfferPair = set()
    offersSet = set()
    # discard expired offers
    for sp in offersplit:
      expiration = dt.strptime(sp[3], '%m/%d/%Y')
      if expiration > dt.now():
        offerDescMap[sp[0]] = sp[1]
        offerDateMap[sp[0]] = sp[3]
        dateOfferPair.add((expiration, sp[0]))
        offersSet.add(sp[0])
    majorOfferDescMap.update(offerDescMap)
    majorOfferDateMap.update(offerDateMap)
    majorDateOfferPair.update(dateOfferPair)
    # accomadate new AMEX GUI
    if len(offers) == 0:
      offers = driver.find_elements_by_xpath("//*[contains(text(), 'Spend ') or contains(text(), 'Get ')]")
      offerstext = [n.text.encode('utf-8') for n in offers]
      offerstext = filter(None, offerstext)
      #offersplit = [text.split('\n') for text in offerstext]
      #offerexpires = driver.find_elements_by_class_name("offer-expires")
      #offerdates = [e.text.encode('utf-8').split('\n')[1] for e in offerexpires]
      tmpnames = [offerstext.split('\n')[1] for n in offerstext]
      for n in tmpnames:
        offersSet.add(n)
      #tmpdesc = [n.text.encode('utf-8').split('\n')[0] for n in offers]
      #for i in len(tmpnames):
      #  expiration = dt.strptime(offerexpires[i], '%m/%d/%Y')
      #  if expiration > dt.now():
      #    offerDescMap[tmpnames[i]] = tmpdesc[i]
      #    offerDateMap[tmpnames[i]] = offerexpires[i]
      #    dateOfferPair.add((expiration, tmpnames[i]))
      #    offersSet.add(tmpnames[i])
    userOffersList.append(offersSet)

    time.sleep(1)
    # logout
    try:
      amexLogOut(driver)
    except:
      pass
    time.sleep(1)

  majorDateOfferList = list(majorDateOfferPair)
  majorDateOfferList.sort(key=lambda tup:tup[0])
  # write 1st line
  for dateOffer in majorDateOfferList:
    offer = dateOffer[1].replace(',', '.')
    sys.stdout.write(','+offer)
  sys.stdout.write('\n')
  # write 2nd line
  for dateOffer in majorDateOfferList:
    desc = majorOfferDescMap[dateOffer[1]].replace(',', ' and')
    sys.stdout.write(','+desc)
  sys.stdout.write('\n')
  # write 3rd line
  for dateOffer in majorDateOfferList:
    date = majorOfferDateMap[dateOffer[1]]
    sys.stdout.write(','+date)
  sys.stdout.write('\n')
  # write the rest
  for i in range(len(username)):
    sys.stdout.write(username[i])
    for dateOffer in majorDateOfferList:
      if dateOffer[1] in userOffersList[i]:
        sys.stdout.write(',+')
      else:
        sys.stdout.write(',')
    sys.stdout.write('\n')

  # close log file
  if outputlog:
    sys.stdout = orig_stdout
    logfile.close()

  # close browser
  driver.quit()


def main():
  username, password = loadConfig("../conf/config.csv")
  getAddedOffers(username, password, outputlog = True)

if __name__ == '__main__':
  main()


