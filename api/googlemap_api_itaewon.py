
import googlemaps
import time

def save_datas(itaewon_data_list,place):
    itaewon_data_list.append(f'{place['name']},,{place['rating']},,{place['user_ratings_total']},,{place['vicinity']}')


#API 키로 클라이언트 생성
gmaps = googlemaps.Client(key="key")

location_list = [
    [37.541850406511855,126.99602833660526],  # 식물원 버스정거장
    [37.542300757291756,126.99286001517044],      # 디앤에이 스튜디오
    [37.54192222682539,126.99121933405068],    # 서울이태원 베이스캠프 투어
    [37.54053459184569,126.99002009814781 ],      # 다원아파트
    [37.538912847199924, 126.99069920447705],           # 서울디지텍고등학교
    [37.538246293457924, 126.99348271224203],     # 카페 TRVR
    [37.53444411486626, 126.99433160522102],       # 이태원역
    [37.53244392611005, 126.99507847130062] ,     # 이태원1동주민센터
    [37.53241675243366,126.99237446175073],   # 용산구청
    [37.53347115670704, 126.99823501377598]   # 이태원 벽화거리
    ]   
itaewon_data_list=[]

for location_x,location_y in location_list:
    # 장소 검색 (예: 이태원역 주변 맛집)
    places_result = gmaps.places_nearby(
        location=(location_x, location_y),  # 위도, 경도
        radius=70,                  # 70m 반경
        keyword="맛집",               # 검색 키워드
        type="food",                # 식당만
        language="ko"                 # 한글로 결과 받기
    )

    #결과 출력
    for place in places_result['results']:
        save_datas(itaewon_data_list,place)

    time.sleep(3)
    if 'next_page_token' in places_result:
        next_page_token = places_result['next_page_token']
    else:
        next_page_token = False
    while next_page_token:
        time.sleep(2)  # Delay to allow next_page_token to become valid
        places_result = gmaps.places_nearby(page_token=next_page_token)

        for place in places_result['results']:
            save_datas(itaewon_data_list,place)
            