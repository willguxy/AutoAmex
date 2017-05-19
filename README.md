# How does it work?
- Clone this repo to your local directory
- Add your own config file under the `conf` folder. Name it as `config.csv`
- The `config.csv` should follow `your_amex_log_in_id`,`your_password` each line. Add however many lines as you want
- Run `python autoamex.py chrome` or `python autoamex.py phantomjs` if you choose to set up your local environment
- Otherwise, just run `docker-start.sh` on Linux or Mac.

# Important Note
You are supposed to have one online account per card. This program doesn't work with multiple cards under the same log-in. It lacks reliablility if we go that way -- once it fails for some cards but succeed for others, you would need to go through a lot of hassle to get those offer reappear under your account.

# Docker compatiblility
- You need to first set up your Docker environment on your local machine
- I used exisiting public image on Docker hub, but it could go obsolete. I'll update when I build and upload my own
- Linux users, just run `./docker-start.sh`
- (I would need to figure something out for Windows users)
- The folder is mounted, so the log files would appear in your local dir as well
- Note the time stamp of those log files would be UTC instead

# AutoTwitter
- OffersBot has stopped updating their twitter account. You'd now need to parse the RSS feed from their website
- I haven't found any free RSS-to-Twiter tools online. TwitterFeed used to be the one, but it's gone now
- Alternative to the approach provided here, you can pay some fee and use other services, or build your own cloud machine that does this job
- Here `parseOffersBotRss.py` lets you get the lastest hashtags and store locally in a file called `hashtags.txt`. `AutoTwitter.py` is the other part which finds this text file in the same folder, and run some Selenium job to publish these hashtags. I added some arbitrary non-sense in front just in case this behavior triggers Twitter spam detector
- `AutoTwitter.py` is also self-contained in that you can pass command line argument to it, and it will pusblish whatever you pass in
- Everything else stays the same. I haven't tested the balace checker so this one might not work very well now.

# Other stuff
- AutoAmexAllOffers: retrieves all added offers across all accounts and lay them down in a csv file
