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


def loginTest(username, password, outputlog = True):

	# re-route output
	orig_stdout = sys.stdout
	logfile = None
	if outputlog:
		# use current time as log file
		logfilename = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
		logfilename = logfilename.replace(':', '_') + ".log"
		logfile = open(logfilename, 'w+')
		sys.stdout = logfile

	# use phantom JS
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
	offersum = 0
	begintime  = time.time()

	# loop through all username/password combinations
	for idx in range(len(username)):

		eachbegintime = time.time()

		print "--------------------------------------------------------------"
		print "#", idx+1, "ID:", username[idx]
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

		# print "Waiting for page to fully load..."
		# for i in range(5):
		# 	time.sleep(1)
		# 	print "->",
		# print "Page has fully loaded..."

		# just in case the feedback banner appears
		try:
			driver.find_element_by_class_name("srCloseBtn").click()
		except:
			pass
		time.sleep(2)

		# click on view more if available
		try:
			driver.find_element_by_class_name(viewMoreBtn).click()
		except:
			pass
		time.sleep(2)

		# click on offers
		# store offer names
		tmpoffernames = driver.find_elements_by_class_name("ah-card-offer-name") + driver.find_elements_by_class_name("ah-offer-name")
		tmpnames = [n.text.encode('utf-8') for n in tmpoffernames]
		tmpnames = filter(None, tmpnames)
		print "Available offers are:", ', '.join(tmpnames)
		offernames = offernames + tmpnames

		# offers = [] if nothing found
		# new version + old version
		offers = driver.find_elements_by_class_name("ah-card-offer-add-to-card") + driver.find_elements_by_class_name("ah-Add-to-card")
		offersum += len(offers)
		print "Total number of offers is:", len(offers)
		print "Adding offers:",

		i = 1
		for offer in offers:
			print i,
			i += 1
			trials = 0 # just in case the button freezes and the program keeps clicking it
			try:
				while True:
					trials += 1
					offer.click()
					time.sleep(1.5)
					if trials >= 5:
						break
			except:
				print "+",
				continue
		print ""

		time.sleep(2)

		# logout
		try:
			WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id(logoutBtnID)).click()
		except:
			# driver.quit()
			pass # pass would be fine, since the launch of the url is the log-in page no matter what

		time.sleep(2)

		eachendtime = time.time()
		# print "You have logged out..."
		print "Time used: %0.2f seconds" % (eachendtime - eachbegintime)
		print "--------------------------------------------------------------"

	
	offernames = list(set(offernames))
	endtime = time.time()
	# print summary
	print "--------------------------------------------------------------"
	print "** Summary **"
	print "Total time used: %0.2f seconds" % (endtime - begintime)
	print "Total number of added offers:", offersum
	print "All offer names:", ', '.join(offernames)
	print "--------------------------------------------------------------"

	# close log file
	if outputlog:
		sys.stdout = orig_stdout
		logfile.close()

	# close browser
	driver.quit()

def main():
	username, password = loadConfig("config.csv")
	loginTest(username, password, outputlog = True)

if __name__ == '__main__':
	main()


