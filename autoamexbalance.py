from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime
import sys
import time
from helper import loadConfig


def getBalance(username, password, outputlog = True):

	# re-route output
	orig_stdout = sys.stdout
	logfile = None
	if outputlog:
		# use current time as log file
		logfilename = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
		logfilename = "balance " + logfilename.replace(':', '_') + ".log"
		logfile = open(logfilename, 'w+')
		sys.stdout = logfile

	# use phantom JS / Firefox
	driver = webdriver.PhantomJS()
	# driver = webdriver.Firefox()
	# driver = webdriver.Chrome('./chromedriver')

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
			time.sleep(2)
		except:
			pass

		balance = ''
		try:
			balance = driver.find_element_by_id("ah-outstanding-balance").text.encode('utf-8')
		except:
			try:
				balance = driver.find_element_by_id("ah-outstanding-balance-value").text.encode('utf-8')
			except:
				pass

		due = ''
		try:
			due = driver.find_element_by_id("ah-whole").text.encode('utf-8') + driver.find_element_by_id("ah-decimal").text.encode('utf-8')
		except:
			try:
				due = driver.find_element_by_class_name("ah-whole").text.encode('utf-8') + driver.find_element_by_class_name("ah-decimal").text.encode('utf-8')
			except:
				pass

		pending = ''
		try:
			driver.find_element_by_id("ah-pending-charges").click()
			time.sleep(2)
			pending = driver.find_element_by_id("ah-total-pending-amount").text.encode('utf-8')
		except:
			try:
				driver.find_element_by_id("ah-pending-transactions").click()
			except:
				pass

		print ""
		print "Total due:", due
		print "Total outstanding balance:", balance
		if pending == '':
			print "No pending transactions..."
		else:
			print "Total pending balance:", pending

		# logout
		WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id(logoutBtnID)).click()
		time.sleep(2)

		eachendtime = time.time()
		print ""
		print "Time used: %0.2f seconds" % (eachendtime - eachbegintime)
		print "--------------------------------------------------------------"

	
	offernames = list(set(offernames))
	endtime = time.time()
	# print summary
	print "--------------------------------------------------------------"
	print "** Summary **"
	print "Total time used: %0.2f seconds" % (endtime - begintime)
	print "--------------------------------------------------------------"

	# close log file
	if outputlog:
		sys.stdout = orig_stdout
		logfile.close()

	# close browser
	driver.quit()

def main():
	username, password = loadConfig("major.csv")
	getBalance(username, password, outputlog = True)

if __name__ == '__main__':
	main()


