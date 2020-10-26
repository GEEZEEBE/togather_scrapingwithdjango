import bs4, time, selenium, requests, json, schedule
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pymongo import MongoClient

driver = webdriver.Chrome(executable_path='/home/rapa/Documents/Develops/chromedriver')
db_url='mongodb://127.0.0.1:27017'

def jobprocess():
    now = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    Insert_name = '황문섭'
    driver.get('https://www.work.go.kr/empInfo/empInfoSrch/list/dtlEmpSrchList.do?careerTo=&keywordJobCd=&occupation=133100%2C133101%2C133200%2C134101%2C134102&rot2WorkYn=&templateInfo=&payGbn=&resultCnt=10&keywordJobCont=&cert=&cloDateStdt=&moreCon=more&minPay=&codeDepth2Info=11000&isChkLocCall=&sortFieldInfo=DATE&major=&resrDutyExcYn=&sortField=DATE&staArea=&sortOrderBy=DESC&keyword=&termSearchGbn=all&benefitSrchAndOr=O&disableEmpHopeGbn=&webIsOut=&actServExcYn=&keywordStaAreaNm=&maxPay=&emailApplyYn=&listCookieInfo=DTL&pageCode=&codeDepth1Info=11000&keywordEtcYn=&publDutyExcYn=&keywordJobCdSeqNo=&exJobsCd=&templateDepthNmInfo=&computerPreferential=&regDateStdt=&employGbn=&empTpGbcd=1&region=&resultCntInfo=10&siteClcd=all&cloDateEndt=&sortOrderByInfo=DESC&currntPageNo=1&indArea=&careerTypes=N&searchOn=Y&subEmpHopeYn=&academicGbn=04&foriegn=&templateDepthNoInfo=&mealOfferClcd=&station=&moerButtonYn=&holidayGbn=&enterPriseGbn=all&academicGbnoEdu=&cloTermSearchGbn=all&keywordWantedTitle=&stationNm=&benefitGbn=&keywordFlag=&essCertChk=&isEmptyHeader=&depth2SelCode=&_csrf=5c5ab007-f9f9-4c7c-88fe-f811bf6c31f3&keywordBusiNm=&preferentialGbn=all&rot3WorkYn=&pfMatterPreferential=&regDateEndt=&staAreaLineInfo1=11000&staAreaLineInfo2=1&pageIndex=1&termContractMmcnt=&careerFrom=&laborHrShortYn=#viewSPL')
    for i in range(1, 10):
        C_date = driver.find_element_by_xpath(f'//*[@id="list{i}"]/td[4]/div/p[3]').text
        C_name = driver.find_element_by_xpath(f'//*[@id="list{i}"]/td[2]/a').text
        element = driver.find_element_by_xpath(f"//tr[@id='list{i}']//div[@class='cp-info-in']/*")
        element.click()
        
        time.sleep(5)
        
        driver.implicitly_wait(10)

        driver.switch_to.window(driver.window_handles[-1])

        driver.implicitly_wait(10)

            job = client['jobdb']
            try:
                jobs = driver.find_elements_by_xpath('//*[@id="contents"]/div/div/div')
                I_name = driver.find_element_by_xpath('//*[@id="contents"]/div[4]/div[1]/p[2]').text
                for job in jobs:
                    # 세부 데이터 수집
                        price = job.find_element_by_xpath("//ul/li[1]/div/strong").text
                data={'Insert_name':Insert_name, 'company_name':C_name,'create_date':now, 'desc':I_name, 'payment':price,'work_time':C_date}
                infor = job.datalist.insert_one(data)
            except:
                pass

        time.sleep(5)

        driver.close()

        print(driver.window_handles)

        driver.switch_to.window(driver.window_handles[0])

jobprocess()

