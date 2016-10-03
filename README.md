# AutoAmex / AutoTwitter / Balance checker / All offers
- automatically adding available amex offers under your account
- you are responsible for creating a config.csv file under the same directory
- for further automation on Mac, you can use Automator to create a repeated calender event
- (update July 13th 2016) AutoTwitter that checks if your twitter account is still alive
- additional functionalities: summarize all balance information in the log file; summarize all available offers in a `csv` file with neat formatting

# Disclaimer
- your private data is NOT secured if you just put it in a csv file
- and this script is exclusive for automation use of amex offers
- educational usage only, any other use is prohibited
- your private login information can be jeopardized
- the author of this script will not be responsible for such losses

# You will need the following tools/packages
- Python 2.7+
- Selenium compatible with Python 2.7+
- [optional] phantom JS (may need to be installed separately)

# To further automate this script on Mac OS
- create a shell script in your Mac Automator
- create a calender event which triggers the above script
- modify the event accordingly, repeat daily
- and make sure your Mac is on during that time

# file description
- `autoamex.py` allows you to automatically add Amex offers in all of your accounts. Each card under a seperate account. Need "config.csv" to load up your login information
- `autoamexalloffers.py` allows you to automatically retrieve all available offer under your accounts. Each card under a seperate account. Need "config.csv" to load up your login information (currently very lengthy output. this will be further optizimed in furture version)
- `autoamexbalance.py` allows you to retrieve your payment due, current balance and pending transaction totals. Each card under a seperate account. Need "major.csv" to load up your login information. "major" means all of your major accounts, excluding autorized user logins please
- `autotwitter.py` helps check if your twitter account is still alive. For people who automate their #AmexOffers tweeting, it's possible that from time to time, the twitter accounts get classified as spam and get suspended. Running this problem would tell you if any of your twitter accounts has died. (No need to argue with Twitter in this case. Just create some new ones.)

# Simple installation for experienced users
- install python 2
- install selenium
- [optional] install phantom JS so that you can run this program in the background
- automate some of the jobs by setting up your job scheduler, e.g. cron on Unix or Automator on Mac OS

# step-by-step installation tutorial on Mac OS for beginners
- Download and install Anaconda here: https://www.continuum.io/downloads (newer version of Mac OS has built-in python, but may not be the lastest version)
- Make sure the bin folder of anaconda is under your $PATH environment variable. if you run `echo $PATH` in your terminal, you should see `/Users/yourname/anaconda/bin` in your `$PATH`.
- update your conda by running "conda update conda" and "conda update anaconda"
- I would recommend using homebrew to manage your packages on Mac: http://brew.sh/ (just copy and paste that one line of Ruby code in your terminal)
- by default, homebrew stores executables under `/usr/local/bin`
- update homebrew by `brew update` and then `brew upgrade`
- (optional) use homebrew to install phantom JS. just run `brew install phantomjs`
- to install selenium, type in the terminal `pip install selenium`. some flags can be added, such as -U if you would like to update, or --no-cache, which means not to store caches
- now you are good to go. Make sure the enviroment variable is well set, so all packages can be found without hassle. If you see some error when running the code like `can't find XYZ module`, most likely you need to modify the `$PATH` variable
- I would run it in the terminal directly. For debug purpose, you can use your preferred editor to edit the code. PyCharm seems to use its own `PATH` by default, so you would have to tweak that around to make PyCharm work
