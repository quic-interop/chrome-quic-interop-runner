#!/usr/bin/env python3

import argparse
import os
import time

from urllib.parse import urlparse

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

DOWNLOADS = "/downloads/"


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--certhash", help="server certificate hash")
    return parser.parse_args()


requests = os.environ["REQUESTS"].split(" ")

f = open("/save.html", "w")
f.write('<html><head><meta charset="UTF-8"></head><body>')
for url in requests:
    f.write('<a href="' + url + '" target="_blank" download>click me</a>')
f.write("</body></html>")
f.close()


server = urlparse(requests[0]).netloc
print("Got server " + server)


options = webdriver.ChromeOptions()
options.gpu = False
options.binary_location = "/usr/bin/google-chrome-beta"
options.add_argument("--no-sandbox")
options.add_argument("--enable-quic")
options.add_argument("--quic-version=80")
options.add_argument("--origin-to-force-quic-on=" + server)
options.add_argument("--log-net-log=/logs/chrome.json")
options.add_argument("--net-log-capture-mode=IncludeSensitive")
options.add_argument("--ignore-certificate-errors-spki-list=" + get_args().certhash)
options.add_argument("--headless=new")
options.add_experimental_option(
    "prefs",
    {
        "download.default_directory": DOWNLOADS,
        "download.prompt_for_download": False,
    },
)


service = Service(
    executable_path="/usr/bin/chromedriver"
)


driver = webdriver.Chrome(service=service, options=options)
driver.get("file:///save.html")
for el in driver.find_elements(By.TAG_NAME, "a"):
    print("Downloading link " + el.get_attribute("href"))
    el.click()


# While downloading, Chrome saves files to <filename>.crdownload.
# Once the download completes, they are moved to <filename>.
def check_files() -> bool:
    files = os.listdir(DOWNLOADS)
    if len(files) < len(requests):
        return False
    return len([f for f in files if ".crdownload" in f]) == 0


while not check_files():
    time.sleep(0.01)

driver.close()
