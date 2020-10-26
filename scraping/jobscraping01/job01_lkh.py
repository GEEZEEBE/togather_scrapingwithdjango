from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests, datetime, time, schedule, os
from selenium.webdriver.chrome.options import Options

def job():
    try:
        # 드라이버 불러오기
        strfile = os.path.dirname(os.path.realpath(__file__))
        strfile = strfile + "/chromedriver_86_4240"

        options = Options()
        options.headless = True
        driver = webdriver.Chrome(executable_path=strfile, options=options)
        driver.implicitly_wait(3)

        # driver = webdriver.Chrome(executable_path='/home/rapa/Documents/job_scraping/chromedriver') # rapa computer
        #driver = webdriver.Chrome(executable_path='chromedriver') # private computer

        #'mongodb://3.35.166.10:58215/' # goorm mongodb ip, local에서 실행하고 goorm mongoDB에 데이터 쌓기
        # 'mongodb://127.0.0.1:27017/' # ip는 계속 바뀐다. 그러므로 항상 ip주소를 재확인, local ip

        # 크롬드라이버로 워크넷 채용정보 상세검색 사이트 열기
        driver.get(url='https://www.work.go.kr/empInfo/empInfoSrch/list/dtlEmpSrchList.do?careerTo=&keywordJobCd=&occupation=&rot2WorkYn=&templateInfo=&payGbn=&resultCnt=10&keywordJobCont=&cert=&cloDateStdt=&moreCon=&minPay=&codeDepth2Info=11000&isChkLocCall=&sortFieldInfo=DATE&major=&resrDutyExcYn=&sortField=DATE&staArea=&sortOrderBy=DESC&keyword=&termSearchGbn=all&benefitSrchAndOr=O&disableEmpHopeGbn=&webIsOut=&actServExcYn=&keywordStaAreaNm=&maxPay=&emailApplyYn=&listCookieInfo=DTL&pageCode=&codeDepth1Info=11000&keywordEtcYn=&publDutyExcYn=&keywordJobCdSeqNo=&exJobsCd=&templateDepthNmInfo=&computerPreferential=&regDateStdt=&employGbn=&empTpGbcd=1&region=&resultCntInfo=10&siteClcd=all&cloDateEndt=&sortOrderByInfo=DESC&currntPageNo=1&indArea=&careerTypes=N&searchOn=Y&subEmpHopeYn=&academicGbn=05%2C00&foriegn=&templateDepthNoInfo=&mealOfferClcd=&station=&moerButtonYn=&holidayGbn=&enterPriseGbn=all&academicGbnoEdu=&cloTermSearchGbn=all&keywordWantedTitle=&stationNm=&benefitGbn=&keywordFlag=&essCertChk=&isEmptyHeader=&depth2SelCode=&_csrf=ee54f119-e6de-4acd-9fb1-c872332e8e84&keywordBusiNm=&preferentialGbn=all&rot3WorkYn=&pfMatterPreferential=&regDateEndt=&staAreaLineInfo1=11000&staAreaLineInfo2=1&pageIndex=1&termContractMmcnt=&careerFrom=&laborHrShortYn=#viewSPL')
        #driver.maximize_window() # window 창 최대화
        keywords = ['python', '빅데이터', '드론']
        for keyword in keywords:
            driver.find_element(By.ID, 'srcKeyword').send_keys(keyword+Keys.ENTER) # 키워드 검색창 선택 후 키워드 입력, 엔터
            for listtitle in range(1,11):
                try:
                    res = driver.page_source # selenium으로 창 띄웠을 때 페이지 소스를 가져오기 위함 
                    soup = BeautifulSoup(res, 'lxml')
                    # 워크넷 list 목록
                    company_name = driver.find_element_by_xpath(f'//*[@id="list{listtitle}"]/td[2]/a').text 
                    title = driver.find_element_by_xpath(f'//*[@id="list{listtitle}"]/td[3]/div/div/a').text
                    payment = driver.find_element_by_xpath(f'//*[@id="list{listtitle}"]/td[4]/div/p[1]').text
                    dates = driver.find_element_by_xpath(f'//*[@id="list{listtitle}"]/td[5]/div/p[2]').text
                    apply_startdate = dates[:12]
                    apply_enddate = dates[12:]
                    apply_startdate = apply_startdate.replace('\n','')
                    desc = driver.find_element_by_xpath(f'//*[@id="jobContLine{listtitle}"]').text
                    career = driver.find_element_by_xpath(f'//*[@id="list{listtitle}"]/td[3]/div/p[2]/em[1]').text
                    work_time = driver.find_element_by_xpath(f'//*[@id="list{listtitle}"]/td[4]/div/p[3]').text
                    location = driver.find_element_by_xpath(f'//*[@id="list{listtitle}"]/td[3]/div/p[2]/em[3]').text

                    t_xpath = '//*[@id="list{}"]/td[3]/div/div/a'.format(listtitle)
                    driver.find_element_by_xpath(t_xpath).click() # 클릭으로 오픈
                    time.sleep(5) # 윈도우 창이 열릴 때 까지 기다려야 됨

                    driver.switch_to.window(driver.window_handles[1]) # 새로 열린 윈도우 창으로 포커스 전환
                    # 새창을 활성화 하였으므로 다시 한번 입력
                    res = driver.page_source
                    soup = BeautifulSoup(res, 'lxml')
                    # detail view
                    link=soup.find('a',attrs={'class':'a-link'}).get_text() # 채용정보 상세모집요강 홈페이지
                    link = link.replace('\n','',1000).replace('\t','',1000) # replace \n의 갯수 한도를 의미, \n이 1000개 이하인건 다 지워라
                    
                    with MongoClient('mongodb://127.0.0.1:27017/') as client:
                        jobdb = client['jobdb'] # jobdb라는 데이터 베이스 생성 => mongodb에서 show dbs로 확인 가능
                        dic = {'Insert_name':"LKH", 'scraping_site':"worknet", 'title':title, 'company_name':company_name, 'link':link, 'payment':payment, 'apply_startdate':apply_startdate, 'apply_enddate':apply_enddate, 'link':link, 'desc':desc, 'career':career, 'work_time':work_time, 'location':location } # 스크랩핑한 데이터와 DB를 맵핑 시키기. Key값은 DB의 Column이고, Value값은 스크랩핑한 데이터
                        jobdb.datalist.insert_one(dic) # jobdb 데이터 베이스에 datalist라는 collection을 생성하고 위에 생성된 dict 타입의 데이터를 하나씩 입력
                        
                    driver.close() # 포커싱 되어 있는 윈도우 창 닫기
                    time.sleep(5) # 닫을려는 윈도우 창이 닫힐 때 까지 기다림
                    driver.switch_to.window(driver.window_handles[0]) # 기존 윈도우 창으로 포커스 전환(포커스는 해당 창 활성화를 의미)

                except:
                    pass

                clear_1 = driver.find_element(By.ID, 'srcKeyword') # 키워드 검색창 선택
                clear_1.clear() # 키워드 삭제

            print("I'm working...")
    except:
        pass


if __name__ == "__main__":
    schedule.every(1).hours.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)
