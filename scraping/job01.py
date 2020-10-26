import schedule
import time, datetime
''' 강사님 sample code
# def job():
#     print("I'm working...")

# schedule.every(5).seconds.do(job)

# reference other file
# import sample_function
# schedule.every(24).hours.do(sample_function.print_message)

# while True:
#     schedule.run_pending()
#     time.sleep(1)

# run python3 ./job01.py    # in Terminal
'''
from jobscraping01 import job01_ceg, job01_jhc, job01_jhj, job01_lkh, job01_oes, job01_pgj, job01_hms

def call_scrapping():
    t = time.localtime()
    print(f'{t.tm_year}.{t.tm_mon}.{t.tm_mday}-{t.tm_hour}:{t.tm_min}:{t.tm_sec} start - junhee', end="")
    job01_ceg.Scrap()
    job01_jhc.scrapping_jobkorea()
    job01_jhj.worknet()
    job01_lkh.job()
    job01_oes.ReadWorkGoKr()
    job01_pgj.w2m()
    job01_hms.jobprocess()
    print('- complete')

schedule.every(1).seconds.do(call_scrapping)
print("start test scheduler")
while True:
    schedule.run_pending()
    time.sleep(1)