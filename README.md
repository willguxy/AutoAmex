# AutoAmex
- automatically adding available amex offers under your account
- you are responsible for creating a config.csv file under the same directory
- for further automation on Mac, you can use Automator to create a repeated calender event

# Disclaimer
- your private data is NOT secured if you just put it in a csv file
- and this script is exclusive for automation use of amex offers
- educational usage only, any other use is prohibited
- your private login information can be jeopardized
- the author of this script will not be responsible for such losses

# You will need the following tools/packages
- Python 2.7+
- Selenium compatible with Python 2.7+
- phantom JS (may need to be installed separately)

# To further automate this script on Mac OS
- create a shell script in your Mac Automator
- create a calender event which triggers the above script
- modify the event accordingly, repeat daily
- and make sure your Mac is on during that time

# file description
- autoamex.py allows you to automatically add Amex offers in all of your accounts. Each card under a seperate account. Need "config.csv" to load up your login information
- autoamexalloffers.py allows you to automatically retrieve all available offer under your accounts. Each card under a seperate account. Need "config.csv" to load up your login information (currently very lengthy output. this will be further optizimed in furture version)
- autoamexbalance.py allows you to retrieve your payment due, current balance and pending transaction totals. Each card under a seperate account. Need "major.csv" to load up your login information. "major" means all of your major accounts, excluding autorized user logins please
