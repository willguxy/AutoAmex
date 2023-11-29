import csv, time, string
from random import choice
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from undetected_chromedriver import Chrome, ChromeOptions

def GenPasswd2(length=8, chars=string.ascii_letters + string.digits):
  return ''.join([choice(chars) for i in range(length)])


def genRandomText():
  return GenPasswd2(8,string.digits) + GenPasswd2(15,string.ascii_letters)


def collectOfferNames(driver):
  offer_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Add to Card') \
    or contains(text(), 'Save Promo Code')]/../../..")
  tmpnames = [n.text.encode('ascii', 'ignore').decode('utf-8', 'ignore') for n in offer_elements if n.text]
  tmpnames = [n.split('\n')[1] if '\n' in n else n for n in tmpnames]
  offernames = ', '.join(sorted(tmpnames))
  return offernames


def getDriver(browser):
  options = ChromeOptions()
  options.add_argument("--incognito")
  options.add_argument("--window-size=1440,900")
  if browser.lower() == 'firefox':
    driver = webdriver.Firefox()
  elif browser.lower() == 'chrome':
    try:
      driver = Chrome(options=options)
    except urllib.error.URLError as e:
      if "[SSL: UNSAFE_LEGACY_RENEGOTIATION_DISABLED] unsafe legacy renegotiation disabled (_ssl.c:1006)" in str(e):
        print("Error: Unsafe legacy renegotiation disabled. Please update your SSL settings.")
        return None
    except Exception as e:
      print("Error: An unexpected error occurred while initializing the Chrome driver.")
      return None
  elif browser.lower() == 'chrome_linux':
    driver = Chrome(options=options)
  elif browser.lower() in ('phantomjs', 'headless'):
    driver = Chrome(options=options)
  else:
    print("WARNING: browser selection not valid, use Chrome as default")
    driver = Chrome(options=options)
  return driver


def loadConfig(filename):
  res = []
  with open(filename, 'r') as f:
    reader = csv.reader(f)
    for row in reader: res.append(row)
  return res


def closeFeedback(driver):
  try:
    driver.find_element(By.CLASS_NAME, "srCloseBtn").click()
  except: pass
  try:
    driver.find_element(By.CLASS_NAME, "fsrCloseBtn").click()
  except: pass
  try:
    driver.find_element(By.CLASS_NAME, "dls-icon-close").click()
  except: pass


def clickOnOffersOnPage(driver):
  for t in range(3):
    if not collectOfferNames(driver): return
    for e in driver.find_elements(By.XPATH, '//*[@title="Add to Card"]') + \
            driver.find_elements(By.XPATH, '//*[@title="Save Promo Code"]'):
      try:
        driver.execute_script("arguments[0].click();", e)
      except Exception as e:
        pass
      time.sleep(2)
    if t != 2:
      driver.refresh()
      time.sleep(1)


def amexLogIn(driver, usr, pwd, emailFieldID='lilo_userName', passFieldID='lilo_password'):
  WebDriverWait(driver, 10).until(lambda driver:
    driver.find_element(By.ID, emailFieldID)).clear()
  WebDriverWait(driver, 10).until(lambda driver:
    driver.find_element(By.ID, emailFieldID)).send_keys(usr)
  WebDriverWait(driver, 10).until(lambda driver:
    driver.find_element(By.ID, passFieldID)).clear()
  WebDriverWait(driver, 10).until(lambda driver:
    driver.find_element(By.ID, passFieldID)).send_keys(pwd)
  for i in range(5):
    try:
      login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'loginSubmit')))
      login_button.click()
      break
    except:
      if i < 4:  # if it's not the last attempt
        time.sleep(5)  # wait for 2 seconds before next attempt
      else:
        pass  # if all attempts failed, pass the exception
  time.sleep(10)


def amexLogOut(driver):
  while driver.find_element(By.XPATH, '//*[contains(text(), "Log Out")]'):
    try: driver.find_element(By.XPATH, '//*[contains(text(), "Log Out")]').click()
    except: pass
    time.sleep(1)


def twitterLogIn(driver, usr, pwd):
  signInLinkID = "signin-link"
  loginBtnClass = "submit"
  emailField = "session[username_or_email]"
  pwdField = "session[password]"
  WebDriverWait(driver, 10).until(lambda driver:
    driver.find_element(By.ID, signInLinkID)).click()
  WebDriverWait(driver, 10).until(lambda driver:
    driver.find_element(By.NAME,emailField)).send_keys(usr)
  WebDriverWait(driver, 10).until(lambda driver:
    driver.find_element(By.NAME,pwdField)).send_keys(pwd)
  WebDriverWait(driver, 10).until(lambda driver:
    driver.find_element(By.CLASS_NAME, loginBtnClass)).click()


def twitterLogOut(driver):
  userDropdownID = "user-dropdown-toggle"
  signOutBtn = "js-signout-button"
  WebDriverWait(driver, 10).until(lambda driver:
    driver.find_element(By.ID, userDropdownID)).click()
  WebDriverWait(driver, 10).until(lambda driver:
    driver.find_element(By.CLASS_NAME, signOutBtn)).click()


def getBalance(driver):
  try:
    e = driver.find_element(By.XPATH, '//*[contains(text(), "Total Balance")]')
    return e.find_element(By.XPATH, '../..').text.split('\n')[1]
  except:
    return "Error"

def clickOnOffers(driver):
    clickThroughCards(driver)

def clickThroughCards(driver):
    # Create a list to store the names of the visited cards
    visited_cards = []

    # Click each card button
    while True:
        # Refresh the buttons before clicking them
        # Wait and click the card switcher toggle button
        switcher_toggle_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".flex.btn.axp-account-switcher__accountSwitcher__togglerButton___1H_zk.account-switcher-toggler.css-15ld01r"))
        )
        switcher_toggle_button.click()
        # Wait for the card list to be visible
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "switcher_product_rows"))
        )
        all_card_buttons = driver.find_elements(By.CSS_SELECTOR, "#switcher_product_rows button")
        card_buttons = [button for button in all_card_buttons if 'ending in' in button.accessible_name and button.accessible_name not in visited_cards]

        # If there are no more cards to visit, break the loop
        if not card_buttons:
            break

        # Click the first unvisited card
        button = card_buttons[0]
        # Add the card to the visited cards list
        visited_cards.append(button.accessible_name)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(button))
        button.click()
        time.sleep(1)  # Adding a delay to allow for any page transitions
        # click the offers on this page
        clickOnOffersOnPage(driver)



