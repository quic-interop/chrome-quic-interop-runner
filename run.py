#!/usr/bin/env python3

import argparse
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--certhash", help="server certificate hash")
    return parser.parse_args()


f = open("/save.html", "w")
f.write('<html><head><meta charset="UTF-8"></head><body>')
for url in os.environ["REQUESTS"].split(" "):
    print(url)
    f.write('<a href="' + url + '" download>click me</a>')
f.write("</body></html>")
f.close()


options = webdriver.ChromeOptions()
options.gpu = False
options.headless = True
options.binary_location = "/usr/bin/google-chrome-unstable"
options.add_argument("--no-sandbox")
options.add_argument("--enable-quic")
options.add_argument("--quic-version=h3-29")
options.add_argument("--origin-to-force-quic-on=server:443")
options.add_argument("--log-net-log=/logs/chrome.json")
options.add_argument("--net-log-capture-mode=IncludeSensitive")
options.add_argument("--ignore-certificate-errors-spki-list=" + get_args().certhash)
options.add_experimental_option(
    "prefs",
    {
        "download.default_directory": "/downloads/",
        "download.prompt_for_download": False,
    },
)

driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver", options=options)
driver.get("file:///save.html")
for el in driver.find_elements_by_tag_name("a"):
    el.click()

# TODO: check that /downloads doesn't contain a .crdownload file
time.sleep(5)
driver.close()
