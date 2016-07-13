from selenium import webdriver
from datetime import datetime
import sys
import time
from helper import loadConfig, twitterLogIn, twitterLogOut

website = "https://twitter.com/download?logged_out=1&lang=en"


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

	# use phantom JS/Firefox/Chrome
	# driver = webdriver.PhantomJS()
	# driver = webdriver.Firefox()
	driver = webdriver.Chrome('./chromedriver')
	driver.maximize_window()
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

		if status != 'challenge':
			# logout
			try:
				twitterLogOut(driver)
			except:
				print "Error: Cannot find logout button [%s]" % username[idx]
				if outputlog:
					sys.stdout = orig_stdout
					logfile.close()
				driver.quit()
			time.sleep(2)

		print "--------------------------------------------------------------"
	
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


