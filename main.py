from urllib import request
from bs4 import BeautifulSoup
from common import initialise_selenium_chrome
from selenium.webdriver.common.keys import Keys
import time


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
        self.driver.get("http://www.google.com")
        """
        https://www.google.com.sg/search?dcr=0&source=hp&q=big+data+startup+Singapore&oq=big+data+startup+Singapore&num=100
        https://www.google.com.sg/search?q=big+data+startup+Singapore&rls=en&dcr=0&ei=M7jtWcT4N8blvgSX8Y2gCw&start=10&sa=N
        
        """
        search_bar = self.driver.find_element_by_id("lst-ib")
        search_bar.send_keys(keyword)
        search_bar.send_keys(Keys.ENTER)

        # get data



        # navigate to page 2
        a_tags = self.driver.find_elements_by_class_name("fl")
        for a_tag in a_tags:
            if a_tag.get_attribute('aria-label') == "Page 2":
                a_tag.click()
                break
        time.sleep(30)

        # store in JSON
        # open semrush iterate through the top 100 websites
        # get data and append in JSON
        # convert to pandas dataframe and output as csv
        pass


if __name__ == '__main__':
    Controller().run("big data startup Singapore")
