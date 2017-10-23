from selenium import webdriver


def initialise_selenium_chrome(google_binary_dir=None, headless=False):
    if not google_binary_dir:
        google_binary_dir = "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary"

    options = webdriver.ChromeOptions()
    options.binary_location = google_binary_dir

    if headless:
        options.add_argument('headless')

    chrome_driver_binary = "/usr/local/bin/chromedriver"
    driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options)
    return driver

