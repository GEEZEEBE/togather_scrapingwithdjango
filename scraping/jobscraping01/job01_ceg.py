from pymongo import MongoClient
import time
import schedule
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from datetime import datetime

# 추가 
import os
from selenium.webdriver.chrome.options import Options

def insertDB(data):
        with MongoClient('mongodb://192.168.0.159:27017/') as client:
                myworkdb = client['jobdb']
                myworkdb.datalist.insert_one(data)

def Scrap():
        # webdriver  추가 
        strfile = os.path.dirname(os.path.realpath(__file__))
        strfile = strfile + "/chromedriver_86_4240"

        options = Options()
        options.headless = True
        # driver = webdriver.Chrome(executable_path=strfile, options=options)
        # driver.implicitly_wait(3)
        # 추가 end 
        
        with webdriver.Chrome(executable_path=strfile, options=options) as driver:
                driver.implicitly_wait(3)
                url = "http://www.saramin.co.kr/zf_user/search?searchType=search&loc_mcd=101000%2C102000&company_cd=0%2C1%2C2%2C3%2C4%2C5%2C6%2C7%2C9%2C10&searchword=AI&panel_type=&search_optional_item=y&search_done=y&panel_count=y"

                driver.get(url=url)
            
                try:
                        company_names = driver.find_elements_by_css_selector("div.area_corp > strong")
                except Exception as e:
                        company_names = ""
                        
                try:
                        titles = driver.find_elements_by_css_selector(" div.area_job > h2 > a")
                except Exception as e:
                        titles = ""
                        
                try:
                        due_dates = driver.find_elements_by_css_selector("div.area_job > div.job_date > span")
                except Exception as e:
                        due_dates = ""
                        
                try:
                        locations = driver.find_elements_by_css_selector("div.job_condition > span:nth-child(1) > a:nth-child(2)")
                except Exception as e:
                        locations = ""
                
                try:
                        careers = driver.find_elements_by_css_selector("div.job_condition > span:nth-child(2)")
                except Exception as e:
                        careers = ""
                
                try:
                        r_date = datetime.now()
                        r_date_s = r_date.split(",")
                        print(r_date_s)
                except Exception as e:
                        r_date = ""
                   
                try:        
                        links = driver.find_elements_by_css_selector(" div.area_corp > strong > a")
                except Exception as e:
                        links = ""
                        
                insert_name = "최유진"
                scraping_site ="https://www.saramin.co.kr/"
                
                # list 
                company_nameList = [n.text for n in company_names]
                titleList = [t.get_attribute('title') for t in titles]
                due_dateList = [d.text for d in due_dates]
                locationList = [l.text for l in locations]
                careerList = [c.text for c in careers]
                linkList = [l.get_attribute('href') for l in links]
                insert_nameList =[]
                create_dateList = []
                scraping_siteList =[]
                for i in range(40):
                        create_dateList.append(r_date)
                        insert_nameList.append(insert_name)
                        scraping_siteList.append(scraping_site)
                
        
                keys = ["insert_name", "scraping_site", "company_name", "title", "location", "career", "job_url"]
                for values in zip(insert_nameList, scraping_siteList, company_nameList, titleList, locationList, careerList, linkList):
                        data = {}
                        for k, v in zip(keys, values):
                                data[k] = v
                        print(data)
                        insertDB(data)
        
                driver.quit()
                
if __name__ == "__main__":
        Scrap()                
      
