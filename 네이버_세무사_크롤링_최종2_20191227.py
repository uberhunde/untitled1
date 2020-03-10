#######################
###### 1. 환경 세팅 ######
#######################

# 라이브러리 호출
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time
import csv

# 객체 정의
class TaxAccountant:
    def __init__(self, business_name, road_addr, phone_num, business_cate, sido, sigungu, upmyondong):
        self.business_name = business_name
        self.road_addr = road_addr
        self.phone_num = phone_num
        self.business_cate = business_cate
        self.sido = sido
        self.sigungu = sigungu
        self.upmyondong = upmyondong

    def getBusinessName(self):
        return self.business_name

    def getRoadAddr(self):
        return self.road_addr

    def getPhoneNum(self):
        return self.phone_num

    def getBusinessCate(self):
        return self.business_cate

    def getSido(self):
        return self.sido

    def getSigungu(self):
        return self.sigungu

    def getUpmyondong(self):
        return self.upmyondong


# 구글크롬 드라이버 실행 및 네이버지도(v4) 접속
driver = webdriver.Chrome('C:\chromedriver.exe')
driver.get('https://v4.map.naver.com/')

# 네이버지도 새로운 버전 팝업 닫기
try:
    driver.find_element_by_xpath('//*[@id="dday_popup"]/div[2]/button').click()
except:
    time.sleep(0.1)

## 검색창에 '세무사'입력 및 검색, 지역
# 검색창 '세무사' 입력
elem_srch = driver.find_element_by_id('search-input')
elem_srch.send_keys('세무사')

# 검색버튼 클릭
srch_xpath = '//*[@id="header"]/div[1]/fieldset/button'
driver.find_element_by_xpath(srch_xpath).click()

# 좌측부분 '지역별' 레이어 클릭하여 내리기(하기 코드 실행 후 위치 확인 요망)
area_guide = driver.find_element_by_class_name('select_area')
area_guide.find_element_by_xpath('//*[@id="panel"]/div[2]/div[1]/div[2]/div[1]/div[4]/div[1]/a[1]/span').click()

# 데이터 내릴 list 생성(tax accountant)
ta = []

## 0. 크롬 브라우저상에서 각자 맡은 지역의 시도 > 시군구 > 동읍면 차례로 클릭 후 하기 코드를 실행

####################################
############ 2.수작업 부분 ############
###### (1) 시도 > 시군구 > 읍면동 선택 ######
###### (2) 다음페이지 수작업 클릭 ######
###### (3) 하기 코드 수행 후 (1)로  ######
####################################

## 1. 업체 정보 추출
bs = BeautifulSoup(driver.page_source,'html.parser')
li_list = bs.select('ul.lst_site > li')
dd = driver.find_element_by_xpath('//*[@id="panel"]/div[2]/div[1]/div[2]/div[2]/div/div/strong')
print(str(dd.text) + '번째 페이지, 크롤링 대상은 ' + str(len(li_list)) + '군데 입니다')
for i in range(int(len(li_list))):
    try:
        # 주소
        lot_num = driver.find_element_by_xpath('//*[@id="panel"]/div[2]/div[1]/div[2]/div[2]/ul/li[' + str(i+1) + ']/div[1]/dl/dd[1]/a')
        # 지번상세 열기
        lot_num.click()
        time.sleep(0.05)
        # 행정동 수집
        admin = driver.find_element_by_class_name('info_road').text.lstrip('지번주소 ')
        # 지번상세 닫기
        driver.find_element_by_xpath('//*[@id="naver_map"]/div[1]/div[9]/div[3]/div/div/div[3]/a').click()
    except NoSuchElementException:
        admin = None
    try:
#        print(li_list[i].find('a').text)  # 상호
        business_name = li_list[i].find('a').text  # 상호
    except:
        business_name = None
        time.sleep(0.1)
    try:
#        print(li_list[i].find('dd').text.rstrip(' 지번'))  # 도로명주소
        road_addr = li_list[i].find('dd').text.rstrip(' 지번')  # 도로명주소
    except:
        road_addr = None
        time.sleep(0.1)
    try:
#        print(li_list[i].find('dd', class_='tel').text.lstrip())  # 전화번호
        phone_num = li_list[i].find('dd', class_='tel').text.lstrip()  # 전화번호
    except:
        phone_num = None
        time.sleep(0.1)
    try:
        #        print(li_list[i].find('dd', class_='cate').text)  # 산업분류
        business_cate = li_list[i].find('dd', class_='cate').text  # 사업분류
    except:
        business_cate = None
        time.sleep(0.1)
    try:
        sido = admin.split(' ')[0]
        sigungu = admin.split(' ')[1]
        upmyondong = admin.split(' ')[2]
 #       print(admin.split(' ')[0])  # 시도
 #       print(admin.split(' ')[1])  # 시군구
 #       print(admin.split(' ')[2])  # 읍면동
    except:
        time.sleep(0.1)
    ta.append(TaxAccountant(business_name, road_addr, phone_num, business_cate, sido, sigungu, upmyondong))
    time.sleep(0.1)
    print(i+1)

# 지역별 더보기 레이어 닫기
try:
    sel_area_close = driver.find_element_by_xpath('//*[@id="panel"]/div[2]/div[1]/div[2]/div[1]/div[3]/div[1]/a[2]/span')
    sel_area_close.click()
except:
    time.sleep(0.05)

###################################
############ 3. csv 추출 ############
### 상기 코드 반복 실행 완수 후 실행 ###
###################################

## 수집결과 csv 출력
# 기본 디렉토리에 저장 - 확인: ~\PycharmProjects\untitled1 [파이참으로 실행시 저장디렉토리]
f = open('output2.csv', 'w', newline= '')
csv_writer = csv.writer(f)
for i in range(0,len(ta)):
    csv_writer.writerow([ta[i].getBusinessName(),ta[i].getRoadAddr(),ta[i].getPhoneNum(),ta[i].getBusinessCate(),ta[i].getSido(),ta[i].getSigungu(),ta[i].getUpmyondong()])
f.close()