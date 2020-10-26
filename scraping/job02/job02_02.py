from bs4 import BeautifulSoup
from pymongo import MongoClient

import schedule
import time
import datetime
import requests
    
def putdata():
    url = "http://www.saramin.co.kr/zf_user/search?search_area=main&search_done=y&search_optional_item=n&searchType=default_mysearch&searchword=%EB%93%9C%EB%A1%A0"
    db_url = 'mongodb://192.168.0.134:27017/'
    # db_url = 'mongodb://192.168.219.136:27017/'
    
    res=requests.get(url)
    soup = BeautifulSoup(res.content, features='lxml')
    # links = soup.find_all('div', attrs={"class":"item_recruit"})
    links = soup.find_all('div', attrs={"class":"item_recruit"})
    with MongoClient(db_url) as client:
        job2_DB = client['job2_DB']
        for link in links:
            insert_name = "GYEONGSU"
            scraping_site = "SARAMIN"
            title = link.span.get_text()
            company_name = link.div.next_sibling.next_sibling.span.get_text().strip()
            job_url = "http://www.saramin.co.kr" + link.a["href"]
            apply_startdate = ""
            apply_enddate = link.div.div.next_sibling.next_sibling.span.get_text().strip()
            create_date = ""
            desc = ""
            payment = ""
            career = ""
            work_time = ""
            academic = ""
            location = ""
            data = {'insert_name':insert_name, 'scraping_site':scraping_site, 'title':title, "company_name":company_name, 'job_url':job_url, "apply_startdate":apply_startdate, "apply_enddate":apply_enddate, "create_date":create_date, "desc":desc, "payment":payment, "career":career, "work_time":work_time, "academic":academic, "location":location}
            job2_DB.job02_02.insert_one(data)
    now = datetime.datetime.now()
    # print(data)
    print(now, "job02_02_working..")

if __name__ == "__main__":
    schedule.every(24).hours.do(putdata)
    while True:
        schedule.run_pending()
        time.sleep(1)

