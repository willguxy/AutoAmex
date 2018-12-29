# Docker
- Now auto_amex has a `Dockerfile`. Suppose you have docker set up on your machine
- You can use `make build` to build a docker image
- Use `make run` to run the process with phantomjs

# Chromedriver
- `chromedriver` has been removed form this repo
- If you need to use legacy mode, please download your own chromedriver and put it under `src`

# Add your configuration
- Add your own config file under the `conf` folder. Name it as `config.csv`
- The `config.csv` should follow `your_login,your_password` each line. Add however many lines as you want. you don't headers for the csv.

# Running the program
- Use docker and make, or
- Run on host machine `python autoamex.py chrome` or `python autoamex.py phantomjs` 
> ( if you have multi cards under one account, and want to process all of them use `python autoamex.py chrome m`)
- Need to install modules for python using `requirements.txt`
- install `chromedriver` or `phantomjs` depend on how you want to run it (recommend `chrome` for first-time users, so that you can see how it works)
- Note that `chromedriver` needs to be under `src` and `phantomjs` needs to be under `$PATH`

# Important Note
- one card per each online account
- this program doesn't work with multiple cards under the same account
- nor does it use multi-tab tricks (it's not robust and only causes more surprises)

# Docker for Windows users (probably incomplete since I never ran docker on Windows)
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

# AutoTwitter (probably not working properly)
- OffersBot has stopped updating their twitter account. You'd now need to parse the RSS feed from their website
- I haven't found any free RSS-to-Twiter tools online. TwitterFeed used to be the one, but it's gone now
- Alternative to the approach provided here, you can pay some fee and use other services, or build your own cloud machine that does this job
- Here `parseOffersBotRss.py` lets you get the lastest hashtags and store locally in a file called `hashtags.txt`. `AutoTwitter.py` is the other part which finds this text file in the same folder, and run some Selenium job to publish these hashtags. I added some arbitrary non-sense in front just in case this behavior triggers Twitter spam detector
- `AutoTwitter.py` is also self-contained in that you can pass command line argument to it, and it will pusblish whatever you pass in
- Everything else stays the same. I haven't tested the balace checker so this one might not work very well now.

# Other stuff (not working either)
- AutoAmexAllOffers: retrieves all added offers across all accounts and lay them down in a csv file
