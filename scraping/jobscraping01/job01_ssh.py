import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import time
from urllib.parse import quote

def getInfo():
    header = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
    url_true='http://www.jobkorea.co.kr/recruit/joblist?menucode=cotype1&cotype=1,2,3,4,5?Page='
    i = 1
    with MongoClient("mongodb://192.168.0.159:27017") as my_client:        
        while True:
            print(i)
            res = requests.get(url=(url_true+str(i)),headers=header)
            print(res.url)
            soup = BeautifulSoup(res.content,'html5lib')

            if soup == None :
                break

            cpnames = soup.select(selector='#dev-gi-list > div > div.tplList.tplJobList > table > tbody > tr')

        
            for cpname in cpnames:
                company_name = (cpname.select('td.tplCo > a')[0].get_text())
                title = (cpname.select('td.tplTit > div > strong > a')[0].get_text())
                
                job_url = 'http://www.jobkorea.co.kr/'+(cpname.select('td.tplTit > div > strong > a')[0]['href'])
                res_company = requests.get(url=job_url,headers=header)
                soup_tmp = BeautifulSoup(res_company.content,'html5lib')
                try :
                    strong_add = soup_tmp.select("#mapDtl")
                    location = strong_add[0].text
                except Exception :
                    location = "홈페이지 지원"      
                print(company_name,title,location,job_url)
                time.sleep(0.4)
                my_client.jobdb.datalist.insert_one({"company_name":company_name,"title":title,"location":location,"job_url":job_url})

            i = i+1
            