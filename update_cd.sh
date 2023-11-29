#!/bin/sh
# Downloads chromedriver based on your current chrome version, unzips, deletes zip file


# Get current chrome version
# separate version from other output (cut...-f3)
# separate first 3 fields (segments) of the version number (cut...-f1-3)
# Pass version number into xargs/curl call
CHROME_VERSION=$(/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version | cut -d ' ' -f3 | cut -d '.' -f1-3 | xargs -I {} curl https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{})

ZIP_FILE_NAME=chromedriver_mac64.zip

# Insert CHROME_VERSION into download URL:
curl -o ./$ZIP_FILE_NAME "https://chromedriver.storage.googleapis.com/$CHROME_VERSION/chromedriver_mac64.zip"

# Unzip. -o flag means overwrite
unzip -o $ZIP_FILE_NAME

rm $ZIP_FILE_NAME

# Clean / remove quarantine for Apple in order to open it
xattr -d com.apple.quarantine chromedriver
