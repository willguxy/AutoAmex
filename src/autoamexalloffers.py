#!/usr/bin/env python
import sys, time, re, logging
import pandas as pd
from datetime import datetime, timedelta
from helper import loadConfig, closeFeedback, amexLogIn, amexLogOut, getDriver
logger = logging.getLogger(__name__)
logging.basicConfig()
amex_url = 'https://global.americanexpress.com/offers/enrolled'

def get_date(x):
  if x.endswith('days'):
    day_offset = int(re.match(r'expires in (\d+) days', x).group(1))
    d = datetime.today() + timedelta(day_offset)
    return d.strftime('%m/%d/%Y')
  elif x.endswith('today'):
    return datetime.today().strftime('%m/%d/%Y')
  elif x.endswith('tomorrow'):
    d = datetime.today() + timedelta(1)
    return d.strftime('%m/%d/%Y')
  else:
    m = re.match(r'expires\n(.*)', x)
    if m: return m.group(1)
    else:
      logger.warning('{} cannot be processed'.format(x))
      return datetime.today().strftime('%m/%d/%Y')


def getAddedOffers(cred, browser = "Chrome"):
  offer_map = {}
  offer_key_desc = {}
  username = [x[0] for x in cred]
  driver = getDriver(browser)
  for login_pair in cred:
    try:
      driver.get(amex_url)
      amexLogIn(driver, login_pair[0], login_pair[1], 'eliloUserID', 'eliloPassword')
    except:
      print("login error")
      continue
    time.sleep(1)
    while not driver.find_elements_by_class_name("offer-expires"): time.sleep(1)
    closeFeedback(driver)
    offer_expires = [o.text.encode('utf-8').lower() 
      for o in driver.find_elements_by_class_name("offer-expires")]
    offer_expires = [get_date(o) for o in offer_expires]
    offer_info = [offer.text.encode('ascii', errors='ignore').encode('utf-8')
      for offer in driver.find_elements_by_class_name("offer-info")]
    offer_info = [o.replace(', get', ' and get').replace(',', '') for o in offer_info]
    # filter out things don't start with 'Spend'
    offer_expires = [offer_expires[i] for i in range(len(offer_expires)) 
      if offer_info[i].startswith('Spend')]
    offer_info = [o for o in offer_info if o.startswith('Spend')]
    offer_info = [o.split('\n') for o in offer_info]
    offer_desc = [o[0] for o in offer_info]
    offer_info = [','.join([re.findall(r'Spend \$(\d+)', o[0])[0], o[1]]) for o in offer_info]
    offer_key = [','.join(x) for x in zip(offer_expires, offer_info)]
    for k in offer_key:
      if k in offer_map: offer_map[k].append(login_pair[0])
      else: offer_map[k] = [login_pair[0]]
    for i in range(len(offer_key)):
      if offer_key[i] in offer_key_desc: offer_key_desc[offer_key[i]].update([offer_desc[i]])
      else: offer_key_desc[offer_key[i]] = set([offer_desc[i]])
    while not driver.find_elements_by_id('eliloUserID'):
      try: amexLogOut(driver)
      except: pass
  driver.quit()
  offer_key_desc = {k: ' OR '.join(v) for k, v in offer_key_desc.iteritems()}

  offer_df = {k: ['+' if x in v else '' for x in username] for k, v in offer_map.iteritems()}
  offer_df = pd.DataFrame(offer_df)
  cols = offer_df.columns.tolist()
  cols.sort(key=lambda x: (datetime.strptime(x.split(',')[0].strip(), '%m/%d/%Y'), 
    x.split(',')[2].strip()))
  offer_df = offer_df[cols]
  offer_df.index = username
  info_rows = pd.DataFrame([[offer_key_desc[x], x.split(',')[0].strip()] for x in cols]).T
  info_rows.index = ['_description', '_expiration']
  colnames = [x.split(',')[2].strip() for x in cols]
  info_rows.columns = offer_df.columns = colnames
  res = pd.concat([info_rows, offer_df])

  file_name = 'offers_' + datetime.strftime(datetime.now(), '%Y-%m-%d_%H-%M-%S') + '.csv'
  res.to_csv('../tmp/' + file_name, sep=',', encoding='utf-8')


def main(argv):
  browser = argv[0] if len(argv) >= 1 else 'Chrome'
  getAddedOffers(loadConfig("../conf/config.csv"), browser=browser)

if __name__ == '__main__':
  main(sys.argv[1:])


