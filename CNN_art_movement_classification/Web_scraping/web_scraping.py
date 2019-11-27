import requests
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from time import sleep
import urllib
import os
from fake_useragent import UserAgent

class Scraper:
    
    
    def __init__(self, driver_path:str):
        
        """
        Init function that opens the driver given the path of chromedriver. Creates a fake user agent and initializes the driver.
        """
        
        options = Options()
        user_agent = UserAgent().random
        options.add_argument(f'user-agent={user_agent}')
        driver = webdriver.Chrome(executable_path=driver_path, options=options)
        self.driver = driver
        content = self.driver.page_source
        self.soup = BeautifulSoup(content, "lxml")
        
                  
    def scroll_down(self, scroll_time:float=0.5):
        
        """
        Function to scroll down the page of a website
        """
        
        if not isinstance(scroll_time, float):
            raise ValueError("Scroll_time, the time between a scroll and another, must be a float.")
        
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        scroll_time = scroll_time
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_time) 
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height


    def get_url(self, url:str, scroll:bool=False):
        
        """
        Function that takes a URL - str - and connects to it. Default option for scrolling the website is True.
        """
        
#         content = self.driver.page_source
#         soup = BeautifulSoup(content, "lxml")
        if not isinstance(scroll, bool):
            raise ValueError("Scroll option must b boolean: False / True")
        try:
            self.driver.get(url)
            if scroll == True:
                self.scroll_down() # also scrolling down automatically
            else:
                pass
        except:
            raise ValueError("Invalid URL.")
    
   
    def find_hrefs(self, url:str, scroll:bool=False, subset_links:str=""):
        
        """
        Function that connects to an URL, scrolls optionally and returns all hrefs whose strings contain the pattern subset_links
        url=str, the URL of the website. 
        scroll=bool, true/false if the page needs to be scrolled down. (default=False)
        subset_links=str, only href that contain subset_links will be return. (default='')
        """
        
        if not isinstance(subset_links, str):
            raise ValueError("Subset links must be a string representing the pattern of hrefs to get.")
        if not isinstance(scroll, bool):
            raise ValueError("Scroll option must b boolean: False / True")
        if not isinstance(subset_links, str):
            raise
            
        self.get_url(url, scroll=scroll)
        hrefs = self.driver.find_elements_by_xpath("//*[@href]")
        if subset_links == "":
            hrefs_subset=[hrefs[i].get_attribute("href") for i in range(len(hrefs))]
        else:
            hrefs_subset=[hrefs[i].get_attribute("href") for i in range(len(hrefs)) if subset_links in hrefs[i].get_attribute("href")]
        # making sure that the hrefs are not duplicated and sorted
        final_href=sorted(list(set(hrefs_subset)))
        return final_href
    
    @staticmethod
    def find_classes(url:str, tag:str, class_name:str):
        
        if not isinstance(url, str):
            raise ValueError("url must be a string")
        
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "lxml")
        output = []
        try:
            result = soup.find_all(tag, class_=class_name)
            output = [elem.get_text() for elem in result]
        except: 
            pass
        
        return output
        
        
    
    def download_all_images(self, folder_name='images'):
        
        cwd = os.getcwd()
        try:
            os.mkdir('{0}/{1}'.format(cwd, folder_name))
        except:
            pass
        
        os.chdir('{0}/{1}'.format(cwd, folder_name))

        images=self.driver.find_elements_by_tag_name('img')
            
        for i in range(len(images)):
            src_attr = images[i].get_attribute('src')
            if src_attr == None:
                pass
            else:
                try:
                    image_url = src_attr.split('/')[-1]
                    print(image_url)
                    
                   
                    if 'jpg' not in image_url or 'png' not in image_url:
                        pass
                    else:
                        img_data = requests.get(src_attr).content
                        with open("{0}".format(image_url), 'wb', encoding="utf-8") as handle:
                            handle.write(img_data)
                        handle.close()
                except:
                    pass
        os.chdir(cwd)