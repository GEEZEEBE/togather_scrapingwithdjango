from selenium import webdriver
from selenium.webdriver.common.keys import Keys as keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs 
from pymongo import MongoClient
import datetime, os
from selenium.webdriver.chrome.options import Options


def worknet():
    insert_name = 'Hojong'
    scraping_site = 'worknet'
    key_words = ["python", "web", "AI",'빅데이터','인공지능']
    options = Options() 
    options.add_argument('--start-maximized') 
    options.add_argument('--headless') #chrome hidden 

    for key_word in key_words:
        strfile = os.path.dirname(os.path.realpath(__file__))
        strfile = strfile + "/chromedriver_86_4240"

        options = Options()
        options.headless = True
        driver = webdriver.Chrome(executable_path=strfile, options=options)
        driver.implicitly_wait(3)

        # driver = webdriver.Chrome(executable_path="../chromedriver", chrome_options=options)
        driver.get(url='https://www.work.go.kr/seekWantedMain.do')
        # driver.implicitly_wait(0.5)

        driver.find_element_by_xpath("//*[@id='gnb']/ul/li[1]/a").click() # 채용정보버튼
        driver.find_element_by_xpath('//*[@id="srcKeyword"]').send_keys(key_word) # 검색어 입력
        driver.find_element_by_xpath('//*[@id="main_contents"]/div[1]/div/div[2]/div/button').click() # 검색버튼
        
        a = driver.find_element_by_xpath('//*[@id="careerTypeN"]') # 경력 checkbox
        driver.execute_script("arguments[0].click();", a)
        b = driver.find_element_by_xpath('//*[@id="b_academicGbn05"]') # 학력 checkbox
        driver.execute_script("arguments[0].click();", b)
        c = driver.find_element_by_xpath('//*[@id="employGbnParam10"]') # 고용형태 checkbox
        driver.execute_script("arguments[0].click();", c)
        d = driver.find_element_by_xpath('//*[@id="srcFrm"]/div[3]/div[4]/button') # 검색버튼
        driver.execute_script("arguments[0].click();", d)

        res = driver.page_source
        soup = bs(res, features='lxml')
        trs = soup.select('table.board-list tbody tr')

        for tr in trs:
            ## company_name title desc location
            company_name = tr.select_one('a.cp_name').text.strip()
            title = tr.select_one('div.cp-info-in a').text.strip()
            desc = tr.select_one('p.mt10').text.strip().split(':')[1]
            location = tr.select('em')[2].text.strip()
            
            ## apply_enddate
            if len(tr.select('div.cp-info p')[8].text.split()) == 2:
                apply_enddate = "채용시까지"
            else:
                start_y_m_d = tr.select('div.cp-info p')[8].text.split()[0].split('/')
                end_y_m_d = tr.select('div.cp-info p')[8].text.split()[2].split('/')
                apply_startdate = "20" + start_y_m_d[0] + start_y_m_d[1] + start_y_m_d[2]
                apply_enddate = "20" + end_y_m_d[0] + end_y_m_d[1] + end_y_m_d[2]

            ## payment
            temp = tr.select('div.cp-info p')[3].text.split()
            if len(temp) == 6:
                payment = temp[0] + ":" + temp[1] + "~" + temp[4]
            elif len(temp) == 4:
                payment = temp[0] + ":" + temp[1] + temp[3]
            else:
                payment = "회사내규에 따름"
            
            driver.quit()

            with MongoClient("mongodb://127.0.0.1:27017") as client:
                db = client.jobdb 
                data = {"key_word":key_word,
                        "scraping_site":scraping_site,
                        "insert_name":insert_name, 
                        "company_name":company_name, 
                        "title":title, 
                        "desc": desc, 
                        "location": location, 
                        "apply_enddate":apply_enddate, 
                        "payment":payment
                        
                        }
                db.datalist.insert(data)
        
        
#     now = datetime.datetime.now()
#     print(now)
# worknet()
