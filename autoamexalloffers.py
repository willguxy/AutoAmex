from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime
import sys
import time
import csv

def loadConfig(filename):
	'''
		load your config.csv file
		the file should contain username, password in each line
		make sure the file is under the same directory
	'''

	username = []
	password = []

	try:
		f = open(filename, 'rb')
		reader = csv.reader(f)
		for row in reader:
			username.append(row[0])
			password.append(row[1])
		f.close()
	except:
		print "file read failed..."
		return username, password

	return username, password


def getAddedOffers(username, password, outputlog = True):

	# re-route output
	orig_stdout = sys.stdout
	logfile = None
	if outputlog:
		# use current time as log file
		logfilename = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
		logfilename = "offers " + logfilename.replace(':', '_') + ".csv"
		logfile = open(logfilename, 'w+')
		sys.stdout = logfile

	# use phantom JS / Firefox
	# driver = webdriver.PhantomJS()
	driver = webdriver.Firefox()
	driver.maximize_window()

	# some parameters
	emailFieldID = "lilo_userName"
	passFieldID = "lilo_password"
	loginBtnID= "lilo_formSubmit"
	logoutBtnID = "iNavLogOutButton"
	viewMoreBtn = "ah-view-more-button"

	# input error handle
	if username == [] or password == [] or len(username) != len(password):
		print "username array does not have the same length as passwrod array..."
		# close log file
		if outputlog:
			sys.stdout = orig_stdout
			logfile.close()
		return

	offernames = []
	# offersum = 0
	# begintime  = time.time()

	allinfos = []
	masterinfo = []

	# loop through all username/password combinations
	for idx in range(len(username)):

		eachbegintime = time.time()

		# print "--------------------------------------------------------------"
		# print "#", idx+1, "ID:", username[idx]
		# just in case network connection is broken 
		try:
			driver.get("https://online.americanexpress.com/myca/logon/us/action/LogonHandler?request_type=LogonHandler&Face=en_US&inav=iNavLnkLog")
		except:
			print "website is not available..."
			# close log file
			if outputlog:
				sys.stdout = orig_stdout
				logfile.close()
			return

		# fill and submit login form
		try:
			WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id(emailFieldID)).clear()
			WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id(emailFieldID)).send_keys(username[idx])
			WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id(passFieldID)).clear()
			WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id(passFieldID)).send_keys(password[idx])
			WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id(loginBtnID)).click()
		except:
			print "username/password combination is incorrect..."
			continue

		time.sleep(2)

		# print "Waiting for page to fully load..."
		# for i in range(5):
		# 	time.sleep(1)
		# 	print "->",
		# print "Page has fully loaded..."
		# print ""

		# just in case the feedback banner appears
		try:
			driver.find_element_by_class_name("srCloseBtn").click()		
		except:
			try:
				driver.find_element_by_class_name("fsrCloseBtn").click()
			except:
				pass
		time.sleep(1)

		# scroll down
		driver.execute_script("window.scrollBy(0, 1250);")

		# click on Added to Card
		flag = True
		while flag:
			try:
				# driver.find_element_by_class_name("ah-addedCard").click()
				driver.find_element_by_xpath("//*[contains(text(), 'Added to Card')]").click()
				time.sleep(1)
				flag = False
			except:
				driver.execute_script("window.scrollBy(0, -150);")
				time.sleep(1)
				continue

		# # click on 'Added to Card'
		# added_to_card = driver.find_elements_by_xpath("//*[contains(text(), 'Added to Card')]")
		# for atc in added_to_card:
		# 	try:
		# 		atc.click()
		# 	except:
		# 		pass
		# 		time.sleep(2)
		
		# scroll down
		driver.execute_script("window.scrollBy(0, 1250);")

		# click on 'load more'
		try:
			driver.find_element_by_xpath("//*[contains(text(), 'Load More')]").click()
		except:
			pass
		time.sleep(2)
		
		# old version + new version
		infos = driver.find_elements_by_class_name("ah-added-card-offer-info") + \
			driver.find_elements_by_class_name("ah-offer-info")
		dates = driver.find_elements_by_class_name("ah-added-card-offer-expiration-date") + \
			driver.find_elements_by_class_name("ah-card-offer-expiration-date")
		icons = driver.find_elements_by_class_name("ah-card-offer-icon")

		# double + sign as separator
		offerinfos = [info.text.encode('utf-8') for info in infos]
		offerdates = [date.text.encode('utf-8') for date in dates]
		allinfos.append([offerdates[i]+'++'+offerinfos[i].replace('\n','++') for i in range(len(offerinfos))])
		# sort by date instead of names
		masterinfo = sorted(set(masterinfo+[offerdates[i]+'++'+offerinfos[i].replace('\n','++') for i in range(len(offerinfos))]))

		# # new version dosen't have offer type
		# types = []
		# offertypes = []
		# if len(icons) != 0:
		# 	types = [driver.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) \
		# 		{ items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', icon)['class'].encode('utf-8') for icon in icons]
		# 	offertypes = [type[27:-5] for type in types]

		# # print out all offers including (type), info and expiration date
		# i = 1
		# if len(offerinfos) == len(offerdates):

		# 	for i in range(len(offerinfos)):

		# 		if len(offertypes) == 0:
		# 			print i, offerinfos[i], offerdates[i]
		# 		else:
		# 			print i, offertypes[i], offerinfos[i], offerdates[i]
		# 		print ""
		# 		i += 1

		time.sleep(1)
		
		# logout
		try:
			WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id(logoutBtnID)).click()
		except:
			pass
		time.sleep(1)

		# eachendtime = time.time()
		# print "You have logged out..."
		# print "Time used: %0.2f seconds" % (eachendtime - eachbegintime)
		# print "--------------------------------------------------------------"

	
	# offernames = list(set(offernames))
	# endtime = time.time()
	# print summary
	# print "--------------------------------------------------------------"
	# print "** Summary **"
	# print "Total time used: %0.2f seconds" % (endtime - begintime)
	# print "--------------------------------------------------------------"

	for i in range(3):
		# replace comma in the any of the 
		for info in masterinfo:
			sys.stdout.write(','+info.split('++')[i].replace(',',''))
		sys.stdout.write('\n')

	for i in range(len(username)):
		sys.stdout.write(username[i])
		for info in masterinfo:
			if info in allinfos[i]:
				sys.stdout.write(','+'+')
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

	username, password = loadConfig("config.csv")
	getAddedOffers(username, password, outputlog = True)

if __name__ == '__main__':
	main()


