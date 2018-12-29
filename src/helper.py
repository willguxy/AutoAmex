import csv
import time
import string
from random import choice
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


def GenPasswd2(length=8, chars=string.ascii_letters + string.digits):
    return ''.join([choice(chars) for i in range(length)])


def genRandomText():
    return GenPasswd2(8, string.digits) + GenPasswd2(15, string.ascii_letters)


def collectOfferNames(driver):
    offer_elements = driver.find_elements_by_xpath("//*[contains(text(), 'Add to Card') \
    or contains(text(), 'Save Promo Code')]/../../..")
    tmpnames = [n.text.encode('ascii', 'ignore').decode(
        'utf-8', 'ignore') for n in offer_elements if n.text]
    tmpnames = [n.split('\n')[1] if '\n' in n else n for n in tmpnames]
    offernames = ', '.join(sorted(tmpnames))
    return offernames


def collectCards(driver):

    # open card slist
    card_button_element = driver.find_element_by_xpath(
        "//span[@class='card-stack-container']/span[@class='card-stack']/button")
    card_button_element.click()
    time.sleep(1)

    if driver.find_element_by_xpath(
            '//*[@title="View All"]'):
        driver.find_element_by_xpath(
            '//*[@title="View All"]').click()

    # read card names
    card_list = driver.find_element_by_id('accounts')

    cards_name_elements = card_list.find_elements_by_class_name(
        'heading-2')

    card_names = []
    for i in cards_name_elements:
        card_names.append(i.text)

    # close cards list
    driver.execute_script("arguments[0].click();", card_button_element)

    return card_names


def changeCard(driver, cardName):
    card_button_element = driver.find_element_by_xpath(
        "//span[@class='card-stack-container']/span[@class='card-stack']/button")
    card_button_element.click()
    time.sleep(2)

    card_list = driver.find_element_by_id('accounts')
    card_list_element = card_list.find_element_by_xpath("//section/header/section/div/div/div/p[contains(text(),'" +
                                                        cardName + "')]")
    card_list_element.click()
    print("clicked " + cardName)


def getDriver(browser):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--window-size=1440,900")
    if browser.lower() == 'firefox':
        driver = webdriver.Firefox()
    elif browser.lower() == 'chrome':
        driver = webdriver.Chrome(
            './chromedriver', chrome_options=chrome_options)
    elif browser.lower() == 'chrome_linux':
        driver = webdriver.Chrome(
            './chromedriver_linux64', chrome_options=chrome_options)
    elif browser.lower() in ('phantomjs', 'headless'):
        driver = webdriver.PhantomJS()
    else:
        print("WARNING: browser selection not valid, use PhantomJS as default")
        driver = webdriver.PhantomJS()
    return driver


def loadConfig(filename):
    res = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            res.append(row)
    return res


def closeFeedback(driver):
    try:
        driver.find_element_by_class_name("srCloseBtn").click()
    except:
        pass
    try:
        driver.find_element_by_class_name("fsrCloseBtn").click()
    except:
        pass
    try:
        driver.find_element_by_class_name("dls-icon-close").click()
    except:
        pass


def clickOnOffers(driver):
    for t in range(3):
        if not collectOfferNames(driver):
            return
        for e in driver.find_elements_by_xpath('//*[@title="Add to Card"]') + \
                driver.find_elements_by_xpath('//*[@title="Save Promo Code"]'):
            try:
                e.click()
            except:
                pass
            time.sleep(1)
        if t != 2:
            driver.refresh()
            time.sleep(1)


def amexLogIn(driver, usr, pwd, emailFieldID='lilo_userName', passFieldID='lilo_password'):
    WebDriverWait(driver, 10).until(lambda driver:
                                    driver.find_element_by_id(emailFieldID)).clear()
    WebDriverWait(driver, 10).until(lambda driver:
                                    driver.find_element_by_id(emailFieldID)).send_keys(usr)
    WebDriverWait(driver, 10).until(lambda driver:
                                    driver.find_element_by_id(passFieldID)).clear()
    WebDriverWait(driver, 10).until(lambda driver:
                                    driver.find_element_by_id(passFieldID)).send_keys(pwd)
    for e in driver.find_elements_by_xpath('//*[@type="submit"]'):
        try:
            e.click()
        except:
            pass
    time.sleep(1)


def amexLogOut(driver):
    while driver.find_element_by_xpath('//*[contains(text(), "Log Out")]'):
        try:
            driver.find_element_by_xpath(
                '//*[contains(text(), "Log Out")]').click()
        except:
            pass
        time.sleep(1)


def twitterLogIn(driver, usr, pwd):
    signInLinkID = "signin-link"
    loginBtnClass = "submit"
    emailField = "session[username_or_email]"
    pwdField = "session[password]"
    WebDriverWait(driver, 10).until(lambda driver:
                                    driver.find_element_by_id(signInLinkID)).click()
    WebDriverWait(driver, 10).until(lambda driver:
                                    driver.find_element_by_name(emailField)).send_keys(usr)
    WebDriverWait(driver, 10).until(lambda driver:
                                    driver.find_element_by_name(pwdField)).send_keys(pwd)
    WebDriverWait(driver, 10).until(lambda driver:
                                    driver.find_element_by_class_name(loginBtnClass)).click()


def twitterLogOut(driver):
    userDropdownID = "user-dropdown-toggle"
    signOutBtn = "js-signout-button"
    WebDriverWait(driver, 10).until(lambda driver:
                                    driver.find_element_by_id(userDropdownID)).click()
    WebDriverWait(driver, 10).until(lambda driver:
                                    driver.find_element_by_class_name(signOutBtn)).click()


def getBalance(driver):
    try:
        e = driver.find_element_by_xpath(
            '//*[contains(text(), "Total Balance")]')
        return e.find_element_by_xpath('../..').text.split('\n')[1]
    except:
        return "Error"
