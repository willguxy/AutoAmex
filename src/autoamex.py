#!/usr/bin/env python
import sys
import time
from datetime import datetime
import logging
from helper import (
    load_config,
    close_feedback,
    click_on_offers,
    amex_log_in,
    amex_log_out,
    get_driver,
    collect_offer_names,
)

AMEX_URL = "https://global.americanexpress.com/offers/eligible"


def login_test(credentials, browser="PhantomJS"):
    log_file_name = datetime.strftime(datetime.now(), "%Y-%m-%d %H_%M_%S") + ".log"
    logging.basicConfig(filename="../tmp/" + log_file_name, level=logging.INFO)

    driver = get_driver(browser)

    t0 = time.time()  # Define t0 at the start of the function

    for index, login_pair in enumerate(credentials, start=1):
        logging.info("# {0} ID: {1}".format(index, login_pair[0]))

        t = time.time()  # Define t at the start of each loop iteration

        try:
            driver.get(AMEX_URL)
            time.sleep(2)
            amex_log_in(
                driver, login_pair[0], login_pair[1], "eliloUserID", "eliloPassword"
            )

        except Exception as e:
            logging.error(e)
            logging.error("Something is wrong with login")
            continue

        time.sleep(5)
        close_feedback(driver)
        time.sleep(3)
        offer_names = collect_offer_names(driver)

        logging.info("Available offers are: {}".format(offer_names))

        click_on_offers(driver)

        try:
            amex_log_out(driver)
        except:
            pass

        logging.info("Time used: %0.1f seconds" % (time.time() - t))

    driver.quit()

    logging.info("** Summary **\nTotal time used: %0.1f seconds" % (time.time() - t0))


def main(argv):
    browser = argv[0] if len(argv) >= 1 else "Chrome"
    login_test(load_config("../conf/config.csv"), browser=browser)


if __name__ == "__main__":
    main(sys.argv[1:])
