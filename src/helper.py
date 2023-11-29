import csv
import time
import string
from random import choice
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from undetected_chromedriver import Chrome, ChromeOptions

def generate_password(length=8, chars=string.ascii_letters + string.digits):
  return ''.join([choice(chars) for _ in range(length)])

def generate_random_text():
  return generate_password(8, string.digits) + generate_password(15, string.ascii_letters)

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

def amex_log_out(driver):
  while driver.find_element(By.XPATH, '//*[contains(text(), "Log Out")]'):
    try: driver.find_element(By.XPATH, '//*[contains(text(), "Log Out")]').click()
    except: pass
    time.sleep(1)

def get_balance(driver):
  try:
    e = driver.find_element(By.XPATH, '//*[contains(text(), "Total Balance")]')
    return e.find_element(By.XPATH, '../..').text.split('\n')[1]
  except:
    return "Error"

def click_on_offers(driver):
    click_through_cards(driver)

def click_through_cards(driver):
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
        visited_cards.append(button.accessible_name)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(button))
        button.click()
        time.sleep(1)
        click_on_offers_on_page(driver)



