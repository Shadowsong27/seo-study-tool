from urllib import request
from bs4 import BeautifulSoup
from common import initialise_selenium_chrome

# url = "https://www.semrush.com/analytics/backlinks/overview/http%3A%2F%2Facjc.moe.edu.sg:domain"
#
# driver.get(url)
# inner_html = driver.execute_script("return document.body.innerHTML")
# print(inner_html)

# content = request.urlopen(req).read().decode("utf-8")
# soup = BeautifulSoup(content, "lxml")
# print(soup)


class Controller:

    def __init__(self):
        self.driver = initialise_selenium_chrome()

    def run(self, keyword):
        """
        output a csv file contained all top 100 websites data related to the given
        keyword
        :return:
        """
        # open google, find top 100 sites html and parse
        # store in JSON
        # open semrush iterate through the top 100 websites
        # get data and append in JSON
        # convert to pandas dataframe and output as csv
        pass