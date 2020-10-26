# 모듈 불러오기
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By 

from pymongo import MongoClient
import sys
import time
import os


def ConnectDB():
    """
    pymongo 연결하기
    리턴값 : MongoCLient 객체
    """
    # str_server = "mongodb://192.168.219.110:27017/"
    str_server = "mongodb://127.0.0.1:27017/"

    client = MongoClient(str_server)
    return client

def InsertDB( client, dbname, tbname, dataList ):
    """
    WORKGOKR 테이블에 데이터를 추가한다.
    client : MongoClient 객체
    dataList : WORKGOKR 정보를 담고 있는 리스트 변수 ( company_name, title, payment, work_time )
    """
    # DB 선택하기
    db = client[dbname]

    # dict 데이터 객체 생성하기
    data = dict()
    data['company_name'] = dataList[0]
    data['title'] = dataList[1]
    data['payment'] = dataList[2]
    data['work_time'] = dataList[3]

    db[tbname].insert_one(data)

def ShowDB( client, dbname, tbname ):
    """
    WORKGOKR 테이블의 내용을 출력한다.
    client : MongoClient 객체
    """

    # DB 선택하기
    db = client[dbname]

    # cursor 얻기
    cursor = db[tbname].find()

    nCount = 1
    for row in cursor:
        print("%d" %nCount)
        print("회사 이름 : %s" %row['company_name'])
        print("직업 소개 : %s" %row['title'])
        print("급여 : %s" %row['payment'])
        print("근무시간 : %s" %row['work_time'])
        print("-"*20)
        nCount = nCount + 1

# work.go.kr 읽엉오기
def ReadWorkGoKr():
    # 옵션 주기
    # options = webdriver.ChromeOptions()
    # options.add_argument("--no-sandbox")
    # options.add_argument('--disable-dev-shm-usage')
    # options.add_argument('--headless')
    

    # 드라이버 불러오기
    strfile = os.path.dirname(os.path.realpath(__file__))
    strfile = strfile + "/chromedriver_86_4240"

    options = Options()
    options.headless = True
    driver = webdriver.Chrome(executable_path=strfile, options=options)
    driver.implicitly_wait(3)

    # 드라이버 get 메서드 호출하기
    driver.get("https://www.work.go.kr/empInfo/empInfoSrch/list/dtlEmpSrchList.do?moreCon=more")

    # 회사명 (company name)
    cp_list = [ elem.text for elem in driver.find_elements_by_xpath("//a[@class='cp_name']") ]

    # 직업 소개
    job_list = [ elem.text for elem in driver.find_elements_by_xpath("//div[@class='cp-info-in']") ]

    # 급여
    price_list = [ elem.text for elem in driver.find_elements_by_xpath("//table/tbody/tr/td[4]/div/p[1]") ]

    # 근무시간
    time_list = [ elem.text for elem in driver.find_elements_by_xpath("//table/tbody/tr/td[4]/div/p[3]") ]

    # 결과 리스트
    item_list = list(zip(cp_list, job_list, price_list, time_list))

    # DB 저장하기
    client = ConnectDB()
    for item in item_list:
        InsertDB(client, 'jobdb', 'datalist', item)
    client.close()

    # ShowDB(client,  'jobdb', 'datalist')
    
    # 종료하기
    driver.quit()

# main 함수 호출하기
if __name__ == "__main__":
    ReadWorkGoKr()

