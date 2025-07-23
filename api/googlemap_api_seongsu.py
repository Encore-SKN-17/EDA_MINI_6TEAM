
import googlemaps
import time

def save_datas(seongsu_data_list, place):
    seongsu_data_list.append(f'{place['name']},,{place['rating']},,{place['user_ratings_total']},,{place['vicinity']}')


#API 키로 클라이언트 생성
gmaps = googlemaps.Client(key="key")

#location 위도 경도 리스트
location_list = [
    [37.544581,127.055961],  # 성수역
    [37.5476,127.0468],      # 뚝섬역
    [37.543574174,127.044727503],    # 서울숲역
    [37.539488594282,127.05399315351],     
    [37.5391, 127.0570],           # 경수초등학교
    [37.53871972, 127.0549075],     # 뚝도시장
    [37.5373, 127.0526],       # 성수동성당
    [37.5766481740232, 126.983533363501] ,     # 성수소극장 
    [37.53691791888463,127.05561093718303 ],   # 서울 은치과의원
    [37.537302200152695,127.05265245681875 ],    #cafe oldtown
    [37.53986818492165, 127.05668239379106 ],    #금금
    [37.54126260942328, 127.0609492760157 ]   #프롤라
    ]   

# googlemap_data={
#     '식당 이름': [],
#     '식당 주소' : [],
#     '리뷰 개수': [],
#     '리뷰 점수': []
# }

seongsu_data_list =[]

for location_x,location_y in location_list:
    # 장소 검색 (예: 성수역 주변 맛집)
    places_result = gmaps.places_nearby(
        location=(location_x, location_y),  # 위도, 경도 (성수역 주변)
        radius=70,                      # 70m 반경
        keyword="맛집",               # 검색 키워드
        type="food",                # 식당만
        language="ko"                 # 한글로 결과 받기
    )

    #결과 출력
    for place in places_result['results']:
        save_datas(seongsu_data_list,place)
        
    time.sleep(3)

    if 'next_page_token' in places_result:
        next_page_token = places_result['next_page_token']
    else:
        next_page_token = False

    while next_page_token:
        time.sleep(2)  # Delay to allow next_page_token to become valid
        places_result = gmaps.places_nearby(page_token=next_page_token)

        for place in places_result['results']:
            save_datas(seongsu_data_list,place)
        break

