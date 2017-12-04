#!/usr/bin/env python
import sys, time, re
import pandas as pd
from selenium import webdriver
from datetime import datetime, timedelta
from helper import loadConfig, closeFeedback, clickOnAddedToCard, \
  clickOnLoadMore, amexLogIn, amexLogOut, getDriver

amex_url = "https://online.americanexpress.com/myca/logon/us/action/LogonHandler?request_type=LogonHandler&Face=en_US&inav=iNavLnkLog"


def get_date(x):
  if x.endswith('days'):
    day_offset = int(re.match(r'expires in (\d+) days', x).group(1))
    d = datetime.today() + timedelta(day_offset)
    return d.strftime('%m/%d/%Y')
  else:
    return re.match(r'expires\n(.*)', x).group(1)


def getAddedOffers(username, password, browser = "Chrome"):
  if username == [] or password == [] or len(username) != len(password):
    print("username array does not have the same length as password array...")
    return
  offer_map = {}

  driver = getDriver(browser)
  for idx in range(len(username)):
    try: driver.get(amex_url)
    except:
      print("website is not available...")
      #return
    try: amexLogIn(driver, username[idx], password[idx])
    except:
      print("username/password combination is incorrect...")
      continue
    time.sleep(2)
    closeFeedback(driver)
    clickOnAddedToCard(driver)
    clickOnLoadMore(driver)
    time.sleep(2)
    closeFeedback(driver)
    # get expiration dates
    offer_expires = [o.text.encode('utf-8').lower() 
      for o in driver.find_elements_by_class_name("offer-expires")]
    offer_expires = [get_date(o) for o in offer_expires]
    # get description and merchant name
    offer_info = [offer.text.encode('utf-8').replace(',', ' and')
      for offer in driver.find_elements_by_class_name("offer-info")]
    offer_info = [', '.join(text.split('\n')) for text in offer_info]
    offer_key = [', '.join(x) for x in zip(offer_expires, offer_info)]

    for k in offer_key:
      if k in offer_map: offer_map[k].append(username[idx])
      else: offer_map[k] = [username[idx]]
    time.sleep(1)
    try: amexLogOut(driver)
    except: pass
    time.sleep(1)
  driver.quit()

  offer_df = {k: ['+' if x in v else '' for x in username] for k, v in offer_map.iteritems()}
  offer_df = pd.DataFrame(offer_df)
  cols = offer_df.columns.tolist()
  cols.sort(key=lambda x: datetime.strptime(x.split(',')[0], '%m/%d/%Y'))
  offer_df = offer_df[cols]
  offer_df.index = username
  info_rows = pd.DataFrame([x.split(', ')[1::-1] for x in cols]).T
  info_rows.index = ['_description', '_expiration']
  colnames = [x.split(', ')[2] for x in cols]
  info_rows.columns = offer_df.columns = colnames
  res = pd.concat([info_rows, offer_df])

  file_name = 'offers_' + datetime.strftime(datetime.now(), '%Y-%m-%d_%H-%M-%S') + '.csv'
  res.to_csv('../tmp/' + file_name, sep=',', encoding='utf-8')


def main():
  username, password = loadConfig("../conf/config.csv")
  getAddedOffers(username, password)

if __name__ == '__main__':
  main()


