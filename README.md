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

# Docker for Windows users
- Check there installation guide for Windows 10 at https://docs.docker.com/docker-for-windows/
- If you are using older versions, please use Docker Toolbox https://docs.docker.com/toolbox/overview/
- It would install both Git and VirtualBox to your computer as well
- Start Docker and make sure it's running on your machine (should be able see the whale icon on lower right corner)
- You should be able to see a terminal popped up (MINGW64). This would be Linux-like instead of `cmd.exe` looking.
- Your host disk is automatically mounted. This means any changes will be reflected on both sides.
- The starting directory is *your personal folder* on Windows
- Find your downloaded `AutoAmex` repo. You can use Git or just download and unzip it
- Remember to create your own `config.csv` file before proceeding
- Go to the repo folder and run `./docker-start.sh`
- Setting jobs on Windows is left out for now. You would need to do your own research to find out how it's done with Docker on Windows

# AutoTwitter
- OffersBot has stopped updating their twitter account. You'd now need to parse the RSS feed from their website
- I haven't found any free RSS-to-Twiter tools online. TwitterFeed used to be the one, but it's gone now
- Alternative to the approach provided here, you can pay some fee and use other services, or build your own cloud machine that does this job
- Here `parseOffersBotRss.py` lets you get the lastest hashtags and store locally in a file called `hashtags.txt`. `AutoTwitter.py` is the other part which finds this text file in the same folder, and run some Selenium job to publish these hashtags. I added some arbitrary non-sense in front just in case this behavior triggers Twitter spam detector
- `AutoTwitter.py` is also self-contained in that you can pass command line argument to it, and it will pusblish whatever you pass in
- Everything else stays the same. I haven't tested the balace checker so this one might not work very well now.

# Other stuff
- AutoAmexAllOffers: retrieves all added offers across all accounts and lay them down in a csv file
