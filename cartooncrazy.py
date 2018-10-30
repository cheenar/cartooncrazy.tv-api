import requests
import cfscrape
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options
import os

'''
Build the session 
'''
mySession = requests.session()
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
}
mySession.headers = headers
scraper = cfscrape.create_scraper(sess=mySession)

#Build the cartoon list
cartoon_list = scraper.get("http://www.cartooncrazy.net/cartoon-list/")
cartoon_list_soup = BeautifulSoup(cartoon_list.content, "html")
cartoon_titles_a = cartoon_list_soup.findAll("ul", {"class":"multi-column-1"})[0].find_all("li");
cartoon_titles_b = cartoon_list_soup.findAll("ul", {"class":"multi-column-2"})[0].find_all("li");
cartoon_titles_c = cartoon_list_soup.findAll("ul", {"class":"multi-column-3"})[0].find_all("li");

#Build the cartoon titles list with the links to the pages
cartoon_titles = {}
for x in range(len(cartoon_titles_a)):
    title = cartoon_titles_a[x].find_all("a")[0].contents[0]
    title = title[0:len(title) - 1]
    cartoon_titles[title] = "http://www.cartooncrazy.net" + cartoon_titles_a[x].find_all("a")[0].attrs["href"]
for x in range(len(cartoon_titles_b)):
    title = cartoon_titles_b[x].find_all("a")[0].contents[0]
    title = title[0:len(title) - 1]
    cartoon_titles[title] = "http://www.cartooncrazy.net" + cartoon_titles_b[x].find_all("a")[0].attrs["href"]
for x in range(len(cartoon_titles_c)):
    title = cartoon_titles_c[x].find_all("a")[0].contents[0]
    title = title[0:len(title) - 1]
    cartoon_titles[title] = "http://www.cartooncrazy.net" + cartoon_titles_c[x].find_all("a")[0].attrs["href"]

def get_title_by_index(index):
    return cartoon_titles[list(cartoon_titles.keys())[index]]

def get_title_by_name(name):
    return cartoon_titles[name]

#scrape the page
def scrape_page(page):
    soup = BeautifulSoup(scraper.get(page).content);
    anime_image = soup.find("div", {"id":"anime-entry-img"}).find("img").attrs["src"];
    anime_desc = soup.find("div", {"id":"anime-entry"}).find_all("p")[1].text
    anime_episode_link = soup.find("div", {"id":"episode-list-entry"}).find_all("script")[1].text.split("'")[1]
    soup = BeautifulSoup(scraper.get(anime_episode_link).content)
    #soup.find_all("tr")[0].find("a").attrs["title"]
    episodes = []
    for episode in soup.find_all("tr"):
            link = episode.find("a").attrs["href"]
            title = episode.find("a").text
            episodes.append((title, 'http://www.cartooncrazy.net' + link))
    return (anime_image, anime_desc, anime_episode_link, episodes)

def episode_watch(link):
    x = scraper.get(link);
    soup = BeautifulSoup(x.content);
    link = soup.find("iframe").attrs["src"]
    return link

import json

if __name__ == "__main__":
    master_json = {}
    for title in list(cartoon_titles.keys())[10:15]:
        print(title)
        master_json[title] = {}
        page_data = scrape_page(cartoon_titles[title]);
        master_json[title]["image"] = page_data[0]
        master_json[title]["desc"] = page_data[1]
        master_json[title]["link"] = page_data[2]
        master_json[title]["episodes"] = []
        episodes = page_data[3]
        for episode in episodes:
            print(episode[0])
            _obj = {}
            _obj["title"] = episode[0]
            _obj["link"] = episode_watch(episode[1])
            master_json[title]["episodes"].append(_obj)
    x = json.dumps(master_json);
    _file = open("master.json", "w+")
    _file.write(x);
    _file.close()
        
        

"""

{
    "Kill la Kill": {
        "image": ...
        "desc": ...
        "link": ...
        "episodes": [
            {
                "title": ...
                "link": ...
            }
        ]
    }
}

"""