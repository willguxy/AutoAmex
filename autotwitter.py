from selenium import webdriver
from datetime import datetime
import sys
import time
from helper import loadConfig, twitterLogIn, twitterLogOut

website = "https://twitter.com/download?logged_out=1&lang=en"


def skipAddPhoneNumber(driver):
	try:
		driver.find_element_by_class_name("modal-btn js-promptDismiss modal-close js-close").click()
		# document.getElementsByClassName("modal-btn js-promptDismiss modal-close js-close")[0].click()
	except:
		pass


def clickOnNotifications(driver):
	driver.find_element_by_class_name("people notifications").click()


def getDriver():
	# use phantom JS/Firefox/Chrome
	# driver = webdriver.PhantomJS()
	# driver = webdriver.Firefox()
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument("--incognito")
	driver = webdriver.Chrome(executable_path='./chromedriver', chrome_options=chrome_options)
	# driver.maximize_window()
	driver.set_window_size(1440,900)
	driver.set_window_position(0,0)
	return driver


def loginTest(username, password, outputlog = True):
	# re-route output
	orig_stdout = sys.stdout
	logfile = None
	if outputlog:
		# use current time as log file
		logfilename = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
		logfilename = "twitter_" + logfilename.replace(':', '_') + ".log"
		logfile = open(logfilename, 'w+')
		sys.stdout = logfile
	# input error handle
	if username == [] or password == [] or len(username) != len(password):
		print "username array does not have the same length as password array..."
		# close log file
		if outputlog:
			sys.stdout = orig_stdout
			logfile.close()
		return

	driver = getDriver()
	begintime  = time.time()

	# loop through all username/password combinations
	for idx in range(len(username)):
		print "--------------------------------------------------------------"
		print "#%s ID:%s" % (idx+1, username[idx])
		# just in case network connection is broken 
		try:
			driver.get(website)
		except:
			print "website is not available..."
			# close log file
			if outputlog:
				sys.stdout = orig_stdout
				logfile.close()
			driver.quit()
			return

		time.sleep(2)

		# login
		try:
			twitterLogIn(driver, username[idx], password[idx])
		except:
			print "username/password combination is incorrect..."
			print "--------------------------------------------------------------"
			continue # end current loop

		time.sleep(2)
		skipAddPhoneNumber(driver)
		time.sleep(1)

		# main program
		status = 'unknown'
		try:
			driver.find_element_by_id("challenge_response")
			status = 'challenge'
		except:
			pass

		try:
			driver.find_element_by_id("global-new-tweet-button")
			status = 'OK'
		except:
			pass

		try:
			driver.find_element_by_id("account-suspended")
			status = 'suspended'
		except:
			pass

		print "Status: %s" % status
		time.sleep(1)

		driver.get("https://twitter.com/i/notifications")  # load notification page
		time.sleep(1)

		if status != 'challenge':
			# logout
			try:
				twitterLogOut(driver)
			except:
				print "Error: Cannot find logout button [%s]" % username[idx]
				time.sleep(10)
				if outputlog:
					sys.stdout = orig_stdout
					logfile.close()
				driver.quit()
		print "--------------------------------------------------------------"

		driver.refresh()
		time.sleep(2)
		try:
			twitterLogOut(driver)
		except:
			pass
	
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
	driver.quit() # close browser

def main():
	username, password = loadConfig("twitter_config.csv")
	loginTest(username, password, outputlog = True)

if __name__ == '__main__':
	main()


