#!/usr/bin/env python
import sys
import time
from selenium import webdriver
from datetime import datetime
from helper import loadConfig, closeFeedback, clickOnOffers, amexLogIn, \
    amexLogOut, getDriver, collectOfferNames, collectCards, changeCard

amex_url = 'https://global.americanexpress.com/offers/eligible'


def loginTest(cred, browser="PhantomJS"):
    logfilename = datetime.strftime(
        datetime.now(), '%Y-%m-%d %H_%M_%S') + '.log'
    with open('../tmp/' + logfilename, 'w+') as f:
        sys.stdout = f
        driver = getDriver(browser)
        i, t0 = 1, time.time()
        for login_pair in cred:
            t = time.time()
            print("# {0} ID: {1}".format(i, login_pair[0]))
            i += 1
            try:
                driver.get(amex_url)
                time.sleep(2)
                amexLogIn(driver, login_pair[0], login_pair[1],
                          'eliloUserID', 'eliloPassword')
            except:
                print("Something is wrong with login\n")
                continue
            time.sleep(5)
            closeFeedback(driver)
            time.sleep(3)
            offer_names = collectOfferNames(driver)
            print("Available offers are: {}".format(offer_names))
            if offer_names:
                clickOnOffers(driver)
            while not driver.find_elements_by_id('eliloUserID'):
                try:
                    amexLogOut(driver)
                except:
                    pass
            print("Time used: %0.1f seconds\n" % (time.time() - t))
        driver.quit()
        print("** Summary **\nTotal time used: %0.1f seconds" %
              (time.time() - t0))


def loginTestMulti(cred, browser="PhantomJS"):
    logfilename = datetime.strftime(
        datetime.now(), '%Y-%m-%d %H_%M_%S') + '.log'
    with open('../tmp/' + logfilename, 'w+') as f:
        sys.stdout = f
        driver = getDriver(browser)
        i, t0 = 1, time.time()
        for login_pair in cred:
            t = time.time()
            print("# {0} ID: {1}".format(i, login_pair[0]))
            i += 1
            try:
                driver.get(amex_url)
                time.sleep(2)
                amexLogIn(
                    driver, login_pair[0], login_pair[1], 'eliloUserID', 'eliloPassword')
            except:
                print("Something is wrong with login\n")
                continue
            time.sleep(5)
            closeFeedback(driver)

            time.sleep(3)
            card_names = collectCards(driver)
            # each card
            for i in card_names:
                tmpT = time.time()
                print(i)
                changeCard(driver, i)
                time.sleep(5)
                offer_names = collectOfferNames(driver)
                print("Available offers are: {}".format(offer_names))
                if offer_names:
                    clickOnOffers(driver)
                print("Time used: %0.1f seconds\n" % (time.time() - tmpT))
            while not driver.find_elements_by_id('eliloUserID'):
                try:
                    amexLogOut(driver)
                except:
                    pass
        # driver.quit()
        print("** Summary **\nTotal time used: %0.1f seconds" %
              (time.time() - t0))


def main(argv):
    browser = argv[0] if len(argv) >= 1 else 'Chrome'
    action = argv[1] if len(argv) >= 2 else ''
    if action == '':
        loginTest(loadConfig("../conf/config.csv"), browser=browser)
    else:
        loginTestMulti(loadConfig("../conf/config.csv"), browser=browser)


if __name__ == '__main__':
    main(sys.argv[1:])
