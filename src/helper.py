import csv
import time
import sys
from random import choice
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from undetected_chromedriver import Chrome, ChromeOptions
import logging

def collect_offer_names(driver):
  offer_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Add to Card') \
    or contains(text(), 'Save Promo Code')]/../../..")
  tmpnames = [n.text.encode('ascii', 'ignore').decode('utf-8', 'ignore') for n in offer_elements if n.text]
  tmpnames = [n.split('\n')[1] if '\n' in n else n for n in tmpnames]
  offernames = ', '.join(sorted(tmpnames))
  return offernames

def get_driver(browser):
  options = ChromeOptions()
  options.add_argument("--incognito")
  options.add_argument("--window-size=1440,900")
  if browser.lower() == 'firefox':
    driver = webdriver.Firefox()
  elif browser.lower() == 'chrome':
    try:
      driver = Chrome(options=options)
    except Exception as e:
      logging.error("Error: An unexpected error occurred while initializing the Chrome driver.")
      sys.exit(1)
  elif browser.lower() == 'chrome_linux':
    driver = Chrome(options=options)
  elif browser.lower() in ('phantomjs', 'headless'):
    driver = Chrome(options=options)
  else:
    logging.warning("WARNING: browser selection not valid, use Chrome as default")
    driver = Chrome(options=options)
  return driver

def load_config(filename):
  with open(filename, 'r') as f:
    reader = csv.reader(f)
    return list(reader)

def close_feedback(driver):
  feedback_classes = ["srCloseBtn", "fsrCloseBtn", "dls-icon-close"]
  for feedback_class in feedback_classes:
    try:
      driver.find_element(By.CLASS_NAME, feedback_class).click()
    except:
      pass

def click_on_offers_on_page(driver):
  # Get the offers from the page
  offers = collect_offer_names(driver)
  # Log the offers on this page
  if offers:
    logging.info("Offers on this page: %s." % offers.split('account ending')[0])
  else:
    logging.info("No offers on this page.")
  for _ in range(3):
    if not collect_offer_names(driver): return
    for e in driver.find_elements(By.XPATH, '//*[@title="Add to Card"]') + \
            driver.find_elements(By.XPATH, '//*[@title="Save Promo Code"]'):
      try:
        driver.execute_script("arguments[0].click();", e)
      except Exception as e:
        pass
      time.sleep(2)
    driver.refresh()
    time.sleep(1)

def amex_log_in(driver, usr, pwd, email_field_id='lilo_userName', pass_field_id='lilo_password'):
  WebDriverWait(driver, 10).until(lambda driver:
    driver.find_element(By.ID, email_field_id)).clear()
  WebDriverWait(driver, 10).until(lambda driver:
    driver.find_element(By.ID, email_field_id)).send_keys(usr)
  WebDriverWait(driver, 10).until(lambda driver:
    driver.find_element(By.ID, pass_field_id)).clear()
  WebDriverWait(driver, 10).until(lambda driver:
    driver.find_element(By.ID, pass_field_id)).send_keys(pwd)
  try:
    login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'loginSubmit')))
    login_button.click()
  except:
    logging.error("ERROR: Unable to log in")
    sys.exit(1)

def amex_log_out(driver):
  while driver.find_element(By.XPATH, '//*[contains(text(), "Log Out")]'):
    try: driver.find_element(By.XPATH, '//*[contains(text(), "Log Out")]').click()
    except: pass
    time.sleep(1)
  logging.info("Logged out.")

def click_on_offers(driver):
    visited_cards = []
    while True:
        switcher_toggle_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".flex.btn.axp-account-switcher__accountSwitcher__togglerButton___1H_zk.account-switcher-toggler.css-15ld01r"))
        )
        switcher_toggle_button.click()
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "switcher_product_rows"))
        )
        all_card_buttons = driver.find_elements(By.CSS_SELECTOR, "#switcher_product_rows button")
        card_buttons = [button for button in all_card_buttons if 'ending in' in button.accessible_name and button.accessible_name not in visited_cards]
        if not card_buttons:
            break
        button = card_buttons[0]
        logging.info("Clicking on card: %s" % button.accessible_name.split(' account')[0])
        visited_cards.append(button.accessible_name)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(button))
        button.click()
        time.sleep(1)
        click_on_offers_on_page(driver)



