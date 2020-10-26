import pymongo
from pymongo import MongoClient
import time
import schedule

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait

client=MongoClient()

client= MongoClient('localhost',27017)

# DB 이름
db=client['job2_DB']

# DB 이름 coll
coll=db['job02_03']

options = Options()
options.headless = True
browser = webdriver.Chrome(executable_path="/home/bjh/Downloads/chromedriver", options=options)
browser.get("https://www.work.go.kr/empInfo/empInfoSrch/list/dtlEmpSrchList.do?keyword=%EC%A0%84%EC%9E%90%EA%B3%B5%ED%95%99%EA%B3%BC")

time.sleep(3)

aa=list()
comp=list()
payl=list()
title01=list()


for i in range(1,11):
    title=browser.find_elements_by_css_selector(f'#list{i} > td:nth-child(3) > div > div > a')
    for i in title:
        title01.append(i.text)

for i in range(1,11):
    data=browser.find_elements_by_css_selector(f'#jobContLine{i}')
    for i in data:
        aa.append(i.text)
        

for i in range(1,11):
    company=browser.find_elements_by_css_selector(f'#list{i} > td:nth-child(2) > a')
    for i in company:
        comp.append(i.text)
        
for i in range(1,11):
    pay=browser.find_elements_by_css_selector(f'#list{i} > td:nth-child(4) > div')
    for i in pay:
        payl.append(i.text)


coll=db.job02_03
key = ['company_name','desc','payment','title']
for value in zip(comp, aa, payl,title01):
    data={}
    for k,v in zip(key,value):
        data[k]=v
    print(data)
    coll.insert_one(data)
result=coll.find()



# schedule.every().day.at("10:30").do(job)
# while True:
#     schedule.run_pending()
#     time.sleep(1)



