#!/usr/bin/env python
import sys, time
from selenium import webdriver
from selenium.webdriver.common.by import By

from datetime import datetime
from helper import (
    loadConfig,
    closeFeedback,
    clickOnOffers,
    amexLogIn,
    amexLogOut,
    getDriver,
    collectOfferNames,
)

amex_url = "https://global.americanexpress.com/offers/eligible"

# This function is defined to test the login functionality of a website.
# The function takes two arguments - 'cred' and 'browser'.
# 'cred' contains login credentials in pairs, one pair for each login.
# 'browser' specifies which browser should be used; if it is not specified, 'PhantomJS' is used as default.


def loginTest(cred, browser="PhantomJS"):
    # A log file name is created, which includes current date and time to make it unique.
    logfilename = datetime.strftime(datetime.now(), "%Y-%m-%d %H_%M_%S") + ".log"

    # The log file is opened in write plus mode, and system standard output is set to this file.
    with open("../tmp/" + logfilename, "w+") as f:
        sys.stdout = f

        # The driver is initialized using the specified browser
        driver = getDriver(browser)

        i, t0 = 1, time.time()

        # Loop through each login_pair provided in cred
        for login_pair in cred:
            t = time.time()

            # Print ID for each login
            print("# {0} ID: {1}".format(i, login_pair[0]))
            i += 1

            try:
                # Open the Amex URL, wait for 2 seconds, and then try to login with the provided credentials.
                driver.get(amex_url)
                time.sleep(2)
                amexLogIn(
                    driver, login_pair[0], login_pair[1], "eliloUserID", "eliloPassword"
                )

            except Exception as e:
                # If there is an exception while logging in, print the error message and skip the current login_pair
                print(e)
                print("Something is wrong with login\n")
                continue

            # Wait for 5 seconds, close the feedback pop-up, wait for 3 seconds and then retrieve offer names
            time.sleep(5)
            closeFeedback(driver)
            time.sleep(3)
            offer_names = collectOfferNames(driver)

            # Print the available offers for this login_pair
            print("Available offers are: {}".format(offer_names))

            # If there are any offers available, click on each offer.
            # if offer_names:
            clickOnOffers(driver)

            try:
                # Logout the user from Amex website.
                amexLogOut(driver)

            except:
                pass

            # Compute and print the time taken to complete this login pair.
            print("Time used: %0.1f seconds\n" % (time.time() - t))

        # Close the driver
        driver.quit()

        # Compute and print the total time taken to test all the login pairs.
        print("** Summary **\nTotal time used: %0.1f seconds" % (time.time() - t0))


def main(argv):
    browser = argv[0] if len(argv) >= 1 else "Chrome"
    loginTest(loadConfig("../conf/config.csv"), browser=browser)


if __name__ == "__main__":
    main(sys.argv[1:])
