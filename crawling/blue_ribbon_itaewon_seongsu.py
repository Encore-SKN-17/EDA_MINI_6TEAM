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
        print(title_path.text)
        blue_ribbon_data['식당 주소'].append(address_path.text)
        blue_ribbon_data['메뉴 태그'].append(tags)

        
    return blue_ribbon_data

# 맨 아래로 스크롤 내리기
def scroll(body):
    body.send_keys(Keys.END)
    body.send_keys(Keys.PAGE_UP)
    time.sleep(2)


def save_datas(blue_ribbon_data, path,num,driver):
    for _ in range(num):
        blue_ribbon_data = get_blue_ribbon_data(blue_ribbon_data,driver)

        body = driver.find_element(By.TAG_NAME,'body')

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

# 다음창 버튼 css path
button_path ='#page-selection > ul > li.next > a'

# 이태원과 성수 link list
links_list =['https://www.bluer.co.kr/search?query=%EC%9D%B4%ED%83%9C%EC%9B%90&foodType=&foodTypeDetail=&feature=&location=&locationDetail=&area=&areaDetail=&ribbonType=&priceRangeMin=0&priceRangeMax=1000&week=&hourMin=0&hourMax=48&year=&evaluate=&sort=&listType=&isSearchName=false&isBrand=false&isAround=false&isMap=false&zone1=%EC%84%9C%EC%9A%B8%20%EA%B0%95%EB%B6%81&zone2=%EC%9D%B4%ED%83%9C%EC%9B%90%2F%ED%95%B4%EB%B0%A9%EC%B4%8C%2F%EB%8F%99%EB%B9%99%EA%B3%A0&food1=&food2=&zone2Lat=37.54&zone2Lng=126.996',
             'https://bluer.co.kr/search?query=%EC%84%B1%EC%88%98&foodType=&foodTypeDetail=&feature=&location=&locationDetail=&area=&areaDetail=&ribbonType=&priceRangeMin=0&priceRangeMax=1000&week=&hourMin=0&hourMax=48&year=&evaluate=&sort=&listType=&isSearchName=false&isBrand=false&isAround=false&isMap=false&zone1=%EC%84%9C%EC%9A%B8%20%EA%B0%95%EB%B6%81&zone2=%EC%84%B1%EC%88%98%EB%8F%99&food1=&food2=&zone2Lat=37.545&zone2Lng=127.053#restaurant-filter-bottom']


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
for link in links_list:
    driver.get(link)
    time.sleep(3)

    # 총 몇 개의 데이터가 있는지 찾기
    data_num_string = driver.find_element(By.CSS_SELECTOR,'#restaurant-filter-bottom > div > div.list-restaurant-content.active > div.list-cnt').text
    time.sleep(1)

    data_num_arr = [x for x in data_num_string]
    result_num=''
    for i in data_num_arr:
        if i.isdigit():
            result_num+=i
    result_num = int(result_num)
    pages = result_num//32 +1


    body = driver.find_element(By.TAG_NAME,'body')
    blue_ribbon_data = save_datas(blue_ribbon_data,button_path,pages,driver)

    scroll(body)

    for _ in range(14):
        body.send_keys(Keys.PAGE_UP)
    button_x = driver.find_element(By.XPATH,'//*[@id="form-search-header"]/div[2]/div/div[1]/div/img[2]')
    button_x.click()
    time.sleep(2)


    driver.close()
