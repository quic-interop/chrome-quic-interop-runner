#!/bin/bash

set -e

CHROME_VERSION="$(dpkg-query -W -f='${source:Upstream-Version}' google-chrome-beta)"

echo "Installing ChromeDriver $CHROME_VERSION"

wget -q "https://chromedriver.storage.googleapis.com/$CHROME_VERSION/chromedriver_linux64.zip"

unzip chromedriver_linux64.zip

mv chromedriver /usr/bin
chmod +x /usr/bin/chromedriver

rm chromedriver_linux64.zip
