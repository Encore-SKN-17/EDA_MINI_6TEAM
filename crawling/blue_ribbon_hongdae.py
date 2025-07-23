from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import numpy as np

def get_blue_ribbon_data(blue_ribbon_data, driver):

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
            blue_ribbon_data['블루리본 개수'].append(0)
        else:
            blue_ribbon_data['블루리본 개수'].append(len(ribbon_path))

        blue_ribbon_data['식당 이름'].append(title_path.text)
        blue_ribbon_data['식당 주소'].append(address_path.text)
        blue_ribbon_data['메뉴 태그'].append(tags)

        
    return blue_ribbon_data

def scroll(body):
    body.send_keys(Keys.END)
    body.send_keys(Keys.PAGE_UP)
    time.sleep(2)

def save_datas(blue_ribbon_data,body, path,num):
    for _ in range(num):
        blue_ribbon_data = get_blue_ribbon_data(blue_ribbon_data,driver)

        # 페이지 아래로 내리기
        scroll(body)

        # 전에 있는 창으로 넘어가는 버튼 주소 : button
        try:
            button = driver.find_element(By.CSS_SELECTOR,path)
            button.click()
        except:
            break
    
        time.sleep(2)
    return blue_ribbon_data

button_path_list =['#page-selection > ul > li.prev > a','#page-selection > ul > li.next > a']

# 1. CHROME 브라우저 실행
path = 'chromedriver.exe'
service = webdriver.chrome.service.Service(path)
driver = webdriver.Chrome(service = service)

# 식당 정보 얻을 리스트 형성
blue_ribbon_data={
    '식당 이름': [],
    '식당 주소' : [],
    '블루리본 개수': [],
    '메뉴 태그': []
}

# 2. 특정 url 접근
driver.get('https://bluer.co.kr/search?&foodType=&foodTypeDetail=&feature=&location=&locationDetail=&area=&areaDetail=&ribbonType=&priceRangeMin=0&priceRangeMax=1000&week=&hourMin=0&hourMax=48&isSearchName=false')
keyword ='홍대'
time.sleep(3)

# 홍대 입력 및 검색
search_box = driver.find_element(By.XPATH,'//*[@id="form-search-header"]/div[2]/div/div[1]/div/input')
search_box.send_keys(keyword)
search_box.send_keys(Keys.RETURN)
time.sleep(3)


# 화면 스크롤
body = driver.find_element(By.TAG_NAME,'body')
scroll(body)

# 맨 마지막 화면으로 이동
button = driver.find_element(By.CSS_SELECTOR,'#page-selection > ul > li.last > a')
button.click()
time.sleep(2)

# 1~7,14번 ,15번째 창 정보 저장
blue_ribbon_data = save_datas(blue_ribbon_data,body,button_path_list[0],9)
print(blue_ribbon_data)

scroll(body)
button = driver.find_element(By.CSS_SELECTOR,'#page-selection > ul > li.next > a')
button.click()
time.sleep(2)

blue_ribbon_data = save_datas(blue_ribbon_data, body, button_path_list[1],6)

blue_hongdae_df = pd.DataFrame(blue_ribbon_data)

driver.close()