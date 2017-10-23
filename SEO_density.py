import os
import pandas
import re
from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from nltk.stem.wordnet import WordNetLemmatizer


def parse_page(filename,page):

    soup = BeautifulSoup(urlopen(filename), 'html.parser')
    lmtzr = WordNetLemmatizer()
    
    keyword = soup.find('input',{'id':'lst-ib'}).get('value').lower()
    keyword_token = list(set([lmtzr.lemmatize(token) for token in keyword.split(' ')]))

    combined_result = []

    search_results = soup.find_all('div', {'class': 'g'})
    position = 0
    for search_result in search_results:
        
        ## Position of the search result in this page
        position += 1

        ## Title flag and keyword density in title
        title = search_result.find('div',{'class':'rc'}).find('h3',{'class':'r'}).get_text()
        title_token = re.sub('[^a-zA-Z0-9\'\.\n]+', ' ', title.lower()).split()
        title_token = [lmtzr.lemmatize(token) for token in title_token]

        title_flag_count = list(filter(lambda token:token in title_token, keyword_token))
        title_flag = 1 if len(title_flag_count) == len(keyword_token) else 0
        title_density_count = sum([keyword_token.count(token) for token in title_token])
        title_density = round(title_density_count / len(title_token),4)

        ## URL flag and keyword density in URL
        url = search_result.find('div',{'class':'rc'}).find('h3',{'class':'r'}).find('a').get('href')

        url_path_token = re.sub('[^a-zA-Z0-9\']+', ' ', urlparse(url).path).lower().split()
        url_path_token = [lmtzr.lemmatize(token) for token in url_path_token]
        url_netloc_token = re.sub('[^a-zA-Z0-9\']+', ' ', urlparse(url).netloc).lower().split()
        url_netloc_token = [lmtzr.lemmatize(token) for token in url_netloc_token]
        url_query_token = re.sub('[^a-zA-Z0-9\']+', ' ', urlparse(url).query).lower().split()
        url_query_token = [lmtzr.lemmatize(token) for token in url_query_token]
        url_flag_count = list(filter(lambda token:token in url_path_token+url_netloc_token+url_query_token,keyword_token))
        url_flag = 1 if len(url_flag_count) == len(keyword_token) else 0

        url_density_count = sum([keyword_token.count(token) for token in url_path_token+url_netloc_token+url_query_token])
        url_density = round(url_density_count / (len(url_path_token)+len(url_netloc_token)+len(url_query_token)) ,4)
        
        
        ## Meta description and keyword density in meta description
        meta = search_result.find('div',{'class':'rc'}).find('div',{'class':'s'}).find('span',{'class':'st'})
        meta_description = re.sub('[^a-zA-Z0-9\n\.\']+', ' ',meta.get_text().strip().lower())
        meta_token = [lmtzr.lemmatize(token) for token in meta_description.split()]
        meta_em =  ' '.join([x.get_text() for x in meta.find_all('em')]).split()
        meta_em_token = [lmtzr.lemmatize(token) for token in meta_em]
        
        meta_flag_count = list(filter(lambda token:token in meta_token,keyword_token))
        meta_flag = 1 if len(meta_flag_count) == len(keyword_token) else 0
        meta_density = round(len(meta_em_token) / len(meta_token), 4)

        ## Append the result to list
        combined_result.append([position,page,title,url,meta_description,title_flag,title_density,url_flag,url_density,meta_flag,meta_density])

    return combined_result
        
            
## The filepath where you store your downloaded HTML pages,please change accordingly
filepath = '/Users/apple/Google Drive/Study/NUS/SEM 7/BT4212/Assignment/Assignment 3/SEOtask_final_v2/Example'
all_files = os.listdir(filepath)
output = []
for index, page in enumerate(all_files):
    ## to skip the temp file generated on Mac
    if (page == '.DS_Store') or (".html" not in page):
        continue
    filename = 'file://127.0.0.1' + filepath + '/' + page
    result = parse_page(filename,page)
    output.extend(result)

df = pandas.DataFrame(output, columns =['Position','Filename','Title','URL','Meta','TitleFlag','TitleDensity','URLFlag','URLDensity','MetaFlag','MetaDensity'])
df.to_csv('output.csv',header = True, index = False,encoding = 'utf-8')

print('Output successfully generated!')

        
            
            
    
