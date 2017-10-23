from urllib import request, parse
from bs4 import BeautifulSoup
from common import initialise_selenium_chrome
from selenium.webdriver.common.keys import Keys
from nltk.stem.wordnet import WordNetLemmatizer

import time
import re


# url = "https://www.semrush.com/analytics/backlinks/overview/http%3A%2F%2Facjc.moe.edu.sg:domain"
#
# driver.get(url)
# inner_html = driver.execute_script("return document.body.innerHTML")
# print(inner_html)

# content = request.urlopen(req).read().decode("utf-8")
# soup = BeautifulSoup(content, "lxml")
# print(soup)


class Controller:

    def __init__(self, keyword):
        self.driver = initialise_selenium_chrome()
        self.lemmatizer = WordNetLemmatizer()
        self.keyword = keyword
        self.keyword_token = list(set([self.lemmatizer.lemmatize(token) for token in keyword.lower().split(' ')]))
        self.result = []

    def run(self):
        """
        output a csv file contained all top 100 websites data related to the given
        keyword
        :return:
        """
        # open google, find top 100 sites html and parse
        self.driver.get("http://www.google.com")

        search_bar = self.driver.find_element_by_id("lst-ib")
        search_bar.send_keys(self.keyword)
        search_bar.send_keys(Keys.ENTER)

        # get data
        position_tracker = 1

        for page_number in range(2, 3):
            search_results = self.driver.find_elements_by_class_name("g")

            for web_page in search_results:
                
                # parsing
                result_meta_element, result_title, result_url = self.parse_html(web_page)
                
                # calculation and processing
                title_flag, title_density = self.cal_title_flag_and_density(result_title)
                url_flag, url_density = self.cal_url_flag_and_density(result_url)
                meta_flag, meta_density = self.cal_meta_flag_and_density(result_meta_element)

                position = position_tracker
                position_tracker += 1

                # package
                current_data_object = {
                    "ranking": position,
                    "title": result_title,
                    "url": result_url,
                    "meta": result_meta_element.text,
                    "title_flag": title_flag,
                    "title_density": title_density,
                    "url_flag": url_flag,
                    "url_density": url_density,
                    "meta_flag": meta_flag,
                    "meta_density": meta_density
                }

                self.result.append(current_data_object)

            # navigate to next page
            a_tags = self.driver.find_elements_by_class_name("fl")
            for a_tag in a_tags:
                if a_tag.get_attribute('aria-label') == "Page {}".format(page_number):
                    a_tag.click()
                    break

            # store in JSON
            # open semrush iterate through the top 100 websites
            # get data and append in JSON
            # convert to pandas dataframe and output as csv

    @staticmethod
    def parse_html(web_page):
        title_element = web_page.find_element_by_class_name("r")
        result_title = title_element.text
        result_url = title_element.find_element_by_css_selector("a").get_attribute("href")
        # leave as element first until i figure out whats wrong with the original algo
        result_meta = web_page.find_element_by_class_name("st")
        return result_meta, result_title, result_url

    def cal_meta_flag_and_density(self, result_meta):
        meta_description = re.sub('[^a-zA-Z0-9\n.\']+', ' ', result_meta.text.strip().lower())
        meta_token = [self.lemmatizer.lemmatize(token) for token in meta_description.split()]
        meta_em = ' '.join([x.text for x in result_meta.find_elements_by_css_selector("em")]).split()
        meta_em_token = [self.lemmatizer.lemmatize(token) for token in meta_em]
        meta_flag_count = list(filter(lambda token: token in meta_token, self.keyword_token))
        meta_flag = 1 if len(meta_flag_count) == len(self.keyword_token) else 0
        meta_density = round(len(meta_em_token) / len(meta_token), 4)
        return meta_flag, meta_density

    def cal_url_flag_and_density(self, result_url):
        url_path_token = re.sub('[^a-zA-Z0-9\']+', ' ', parse.urlparse(result_url).path).lower().split()
        url_path_token = [self.lemmatizer.lemmatize(token) for token in url_path_token]
        url_netloc_token = re.sub('[^a-zA-Z0-9\']+', ' ', parse.urlparse(result_url).netloc).lower().split()
        url_netloc_token = [self.lemmatizer.lemmatize(token) for token in url_netloc_token]
        url_query_token = re.sub('[^a-zA-Z0-9\']+', ' ', parse.urlparse(result_url).query).lower().split()
        url_query_token = [self.lemmatizer.lemmatize(token) for token in url_query_token]
        url_flag_count = list(
            filter(lambda token: token in url_path_token + url_netloc_token + url_query_token, self.keyword_token))
        url_flag = 1 if len(url_flag_count) == len(self.keyword_token) else 0
        url_density_count = sum(
            [self.keyword_token.count(token) for token in url_path_token + url_netloc_token + url_query_token])
        url_density = round(
            url_density_count / (len(url_path_token) + len(url_netloc_token) + len(url_query_token)), 4)
        return url_flag, url_density

    def cal_title_flag_and_density(self, result_title):
        title_token = re.sub('[^a-zA-Z0-9\'.\n]+', ' ', result_title.lower()).split()
        title_token = [self.lemmatizer.lemmatize(token) for token in title_token]
        title_flag_count = list(filter(lambda token: token in title_token, self.keyword_token))
        title_flag = 1 if len(title_flag_count) == len(self.keyword_token) else 0
        title_density_count = sum([self.keyword_token.count(token) for token in title_token])
        title_density = round(title_density_count / len(title_token), 4)
        return title_flag, title_density


if __name__ == '__main__':
    Controller("big data startup Singapore").run()

