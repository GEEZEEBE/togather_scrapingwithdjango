from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import schedule,time
from pymongo import MongoClient
#for goorm.io
from selenium.webdriver.chrome.options import Options
import datetime
d_path = '/home/cho/Documents/Develop/web_config/driver/chromedriver_linux'
# Create your views here.




# -------------------------------------------------- selenium ---------------------------------------------------------------
def login(id_1,password,driver):
    click = driver.find_element_by_css_selector('#header > div.top-area > div > div.util > a:nth-child(1)')
    click.click()
    id_info = driver.find_element_by_css_selector('#custId1')
    pw_info = driver.find_element_by_css_selector('#pwd1')
    button = driver.find_element_by_css_selector('#loginArea > div.login-form.login-idv > div.login-area > button')

    id_info.send_keys(id_1)
    pw_info.send_keys(password)
    button.click()

    

def close_tab(driver,url1):
    #time.sleep(1)
    if len(driver.window_handles) > 2 :

        for i in range(0,len(driver.window_handles)-1):
            driver.switch_to.window(driver.window_handles[-1])
            driver.close()  

        last_tab = driver.window_handles[-1]
        driver.switch_to.window(window_name=last_tab)
    else :  # 새 탭이 로딩이 완전히 되지않아서 데이터를 못 읽어오는 것을 방지 하기위한 조건문 
        i =0
        while driver.current_url != url1: # 현재 driver 의 링크와 구직정보를 제공하는 링크가 동일하지 않은경우 대기
            time.sleep(0.4)
            i+=1
            if i>5 :
                break
        last_tab = driver.window_handles[-1]            # 가장 최신단의 탭정보를 얻어옴
        driver.switch_to.window(window_name=last_tab)   # 최신단의 탭으로 이동
        last_tab = driver.window_handles[-1]            # 만약을 대비하기 위한 탭 이동코드
        driver.switch_to.window(window_name=last_tab)
        
        if driver.current_url != url1 :                 # 만약 위의 과정을 거쳐도 url 이 같지 않은경우 강제로 이동시킴
            driver.get(url=url1)


def collectJobInfo(d_path):    
    with  MongoClient("mongodb://127.0.0.1:27017") as my_client: 
        url = 'https://www.work.go.kr/seekWantedMain.do'
        my_client.my_db.job_info.drop()
     
        # for goorm.io setting selenium 
        # options = Options()
        # options.add_argument("--headless")
        # options.add_argument("--no-sandbox")

        # driver = webdriver.Chrome(options=options)          # for goorm.io 
        driver = webdriver.Chrome(executable_path=d_path) # for linux 

        driver.implicitly_wait(3) # 암묵적으로 웹 자원을 (최대) 3초 기다리기
    
        # 로그인 후 worknet 에 입력된 맞춤채용정보를 저장한 검색 페이지로 이동
        # 이때 seqNo 를 바꿔 지정된 검색 옵션을 선택할 수 있다. 현재는 2번을 사용중
        driver.get(url="https://www.work.go.kr/empInfo/empInfoSrch/list/dtlEmpSrchList.do?region=&empTpGbcd=1%7C2&keyword=%EB%93%9C%EB%A1%A0+%EA%B0%9C%EB%B0%9C")

        # 페이지 정보 얻어오기 
        pageNo = int(driver.find_element_by_css_selector('#mForm > div.nav_wrp > div').text[2])
        
        # 페이지 수만큼 반복 실행
        for i in range(1,pageNo+1):
            # 데이터 수집시작
            driver.get(url=f"https://www.work.go.kr/empInfo/empInfoSrch/list/dtlEmpSrchList.do?region=&&pageIndex={i}&empTpGbcd=1%7C2&keyword=%EB%93%9C%EB%A1%A0+%EA%B0%9C%EB%B0%9C")
            table = driver.find_element_by_css_selector("#mForm > div.table-wrap > table > tbody")
            lists = table.find_elements_by_css_selector("tr")
            for td in lists :
                #새창으로 이동하기 위한 링크클릭
                
                title = td.find_element_by_css_selector('td:nth-child(3) > div > div > a').text
                company = td.find_element_by_css_selector('td:nth-child(2) > a').text
                link = td.find_element_by_css_selector('td:nth-child(3) > div > div > a').get_attribute('href')                
                d_day_tag = (td.find_elements_by_css_selector(' td:nth-child(5) > div > p'))
                d_day = str(d_day_tag[-1].text).split('\n')
                pay = str(td.find_element_by_css_selector('td:nth-child(4) > div > p:nth-child(1)').text)
                career =  str(td.find_element_by_css_selector('td:nth-child(3) > div > p:nth-child(3) > em:nth-child(1)').text)
                academic =  str(td.find_element_by_css_selector('td:nth-child(3) > div > p:nth-child(3) > em:nth-child(2)').text)
                career += ' | '+academic
                address =  str(td.find_element_by_css_selector('td:nth-child(3) > div > p:nth-child(3) > em:nth-child(3)').text)
                work = td.find_element_by_css_selector('td:nth-child(3) > div > div > p').text
                #print(list1)    
                # 새로 열렸던 창을 닫고 기존의 검색창으로 복귀 
            
                #my_client.job02_DB.job02_08.insert_one({'site':'worknet','title':title,'company':company,'link':link,'day_start':d_day[0],'day_end':d_day[1],'create_date':datetime.datetime.now(), 'career':career,'pay':pay,'desc':work})
                if len(d_day) > 1 :
                    print({'site':'worknet','title':title,'company':company,'link':link,'day_start':d_day[0],'day_end':d_day[1],'create_date':datetime.datetime.now(),'desc':work,'pay':pay,'career':career,'location':address})
                else :
                    print({'site':'worknet','title':title,'company':company,'link':link,'day_start':d_day[0],'day_end':'지정안됨','create_date':datetime.datetime.now(),'desc':work,'pay':pay,'career':career,'location':address})
                    

        time.sleep(2)
        driver.quit()

if __name__ == "__main__":
    
    collectJobInfo(d_path)