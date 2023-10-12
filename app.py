from bs4 import BeautifulSoup 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.support.ui import WebDriverWait as wait
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import regex as re
import json 
from tenacity import retry, stop_after_attempt, wait_fixed

def high_level():
    atom=wait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='DatasetResult__title-container']/a")))
    return atom    
    
i=0
for y in range(15):
    it=y*10
    print(it)   
    val=f'https://data.cms.gov/search?offset={it}'
    
    @retry(stop=stop_after_attempt(4), wait=wait_fixed(15))
    def high_level():
        driver.get(val)
        atoz=wait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='DatasetResult__title-container']/a")))
        return atoz       
    atom=high_level()
       
    for x in atom:
        dictcontent={}
        print(f"loop{i}") 
        i+=1
        ctom=x.text
        dictcontent[ctom]={}
        dictcontent[ctom]['site'] = x.get_property('href')
        dictcontent[ctom]['CMSPage'] = it
        val2=x.get_property('href')
        print("val2")
        print(val2)
        time.sleep(15)
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

        @retry(stop=stop_after_attempt(4), wait=wait_fixed(15))
        def low_level():
            driver.get(val2)
            btomz = wait(driver, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "DatasetHero__meta")))
            print(btomz)
            return btomz
        btom=low_level()
        
        for index, y in enumerate(btom):
            if index==0:
                free=re.search('.*\\n(.*)',y.text,re.IGNORECASE)
                dictcontent[x.text]['Data update frequency']= free.group(1)
            if index==1:
                free=re.search('.*\\n(.*)',y.text,re.IGNORECASE)
                dictcontent[x.text]['Latest data available']= free.group(1)
        print(dictcontent)                


        with open("D:\CMS_data_update\cmsdata.txt", "a") as convert_file: 
            convert_file.write(json.dumps(dictcontent))
    

#f = open("D:\CMS_data_update\cmsdata2.txt", "w")
#f.close()
