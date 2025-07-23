from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import numpy as np


# 1. CHROME 브라우저 실행
path = 'chromedriver.exe'
service = webdriver.chrome.service.Service(path)
driver = webdriver.Chrome(service = service)

# 식당 정보 얻을 리스트 형성
red_ribbon_data={
    '식당 이름': [],
    '식당 주소' : [],
    '레드리본 개수': [],
    '메뉴 태그': []
}

# 2. 레드리본 검색 url 접근 & 홍대 성수 이태원 키워드 리스트에 저장

keyword_list =['홍대', '성수', '이태원']
driver.get('https://www.bluer.co.kr/search?tabMode=single&searchMode=feature&location=&ribbonType=&feature=107')
time.sleep(5)

for keyword in keyword_list:

    # 검색어 입력 및 검색
    search_box = driver.find_element(By.XPATH,'//*[@id="form-search-header"]/div[2]/div/div[1]/div/input')
    search_box.send_keys(keyword)
    search_box.send_keys(Keys.RETURN)

    time.sleep(3)


    # 총 몇 개의 데이터가 있는지 찾기
    data_num_string = driver.find_element(By.CSS_SELECTOR,'#restaurant-filter-bottom > div > div.list-restaurant-content.active > div.list-cnt').text
    data_num_arr = [x for x in data_num_string]
    result_num=''
    for i in data_num_arr:
        if i.isdigit():
            result_num+=i
    result_num = int(result_num)
    pages = result_num//32 +1

    # 다음창으로 넘어가는 버튼 주소 : button
    button = driver.find_element(By.XPATH,'//*[@id="page-selection"]/ul/li[5]/a/img')
    body = driver.find_element(By.TAG_NAME,'body')

    for page in range(pages):

        # 화면에 보이는 식당 태그들 담기
        rest_contents = driver.find_elements(By.CSS_SELECTOR, '#list-restaurant >li .thumb-restaurant')

        for content in rest_contents:
            # 식당 이름, 메뉴 태그, 주소 패스를 저장
            title_path = content.find_element(By.CSS_SELECTOR, 'div.header-title > div:nth-child(2) > h3')
            address_path = content.find_element(By.CSS_SELECTOR,'div.info > div:nth-child(1) > div')
            tag_path = content.find_elements(By.CSS_SELECTOR,'header > div.header-status > ol > li')

            # 태그 여러개일 것을 가정해 list에 담아서 저장
            tags=[]
            for tag in tag_path:
                tags.append(tag.text)

            # 리본 개수 없을 것을 가정해 try-except 구문으로 작성
            # 리본 개수가 있으면 갯수 data 딕셔너리에 저장, 없으면(예외발생하면) 0 저장
            try :
                ribbon_path = content.find_elements(By.CSS_SELECTOR,'div:nth-child(1) > ul.ribbons.pull-left > li')
            except:
                red_ribbon_data['레드리본 개수'].append(0)
            else:
                red_ribbon_data['레드리본 개수'].append(len(ribbon_path))

            red_ribbon_data['식당 이름'].append(title_path.text)
            red_ribbon_data['식당 주소'].append(address_path.text)
            red_ribbon_data['메뉴 태그'].append(tags)
        
        # 마지막 페이지면 반복문 나가기
        if page == (pages-1):
            break

        # 페이지 아래로 내리기
        for _ in range(14):
            body.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)

        # 버튼 누르기
        button.click()
        time.sleep(1)
    for _ in range(14):
        body.send_keys(Keys.PAGE_UP)
    button_x = driver.find_element(By.XPATH,'//*[@id="form-search-header"]/div[2]/div/div[1]/div/img[2]')
    button_x.click()
    time.sleep(1)


red_df = pd.DataFrame(red_ribbon_data)

driver.close()