from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests, datetime, schedule, time

def scrapping_jobkorea(keyword='인공지능'):
    url = f'http://www.jobkorea.co.kr/Search/?stext={keyword}&tabType=recruit&Page_No=1'
    res = requests.get(url)
    if res.status_code == 200:
        soup = BeautifulSoup(res.content, 'lxml')
        links = soup.find_all('a', class_='title dev_view')
        companies = soup.find_all('a', class_='name dev_view')
        data = []
        for link, company in zip(links, companies):
            title = link.get_text()
            title = title.strip('\r\n').strip()
            link = 'http://www.jobkorea.co.kr' + link.get('href')
            company_name = company.get_text()
            # dic = {"title": title, "link": link, "company":company_name, "create_date": datetime.datetime.now()}
            dic = {'Insert_name':'jhc', 'scraping_site':'jobkorea', 'title': title, 'company_name':company_name, 
                    'job_url':link, "create_date": datetime.datetime.now()}
            data.append(dic)

        with MongoClient('mongodb://127.0.0.1:27017/')  as client:
            mydb = client.jobdb
            res = mydb.datalist.insert_many(data)

def call_scrapping_jobkorea():
    t = time.localtime()
    print(f'{t.tm_year}.{t.tm_mon}.{t.tm_mday}-{t.tm_hour}:{t.tm_min}:{t.tm_sec} start - junhee', end="")
    scrapping_jobkorea()
    print('- complete')

if __name__ == "__main__":
    schedule.every(1).seconds.do(call_scrapping_jobkorea)
    print("start test scheduler")
    while True:
        schedule.run_pending()