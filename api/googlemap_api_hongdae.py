
import googlemaps
import time

def save_datas(hongdae_data_list,place):
    hongdae_data_list.append(f'{place['name']},,{place['rating']},,{place['user_ratings_total']},,{place['vicinity']}')


#API 키로 클라이언트 생성
gmaps = googlemaps.Client(key="key")

location_list = [
    [37.5576978,126.9265751],  # 홍대입구역
    [37.55148566665506,126.92547929342999],      # 홍대
    [ 37.55091512490709,126.92099846890335 ],    # 상상마당
    [37.549439040198415,126.92335384318247],     
    [37.55383291324387, 126.91886777625561],           # 신한은행
    [37.558554228814316, 126.91899847101658],     # 하이업엔터
    [37.56269927417684, 126.9196730892676],       # 홍익디자인고등학교
    [37.56365700225048, 126.92370147364764],      # 커피리브레
    [37.56104531362837,126.92558295490328],      
    [37.555479409508884,126.92925530768194],    #언플래그드 홍대
    [37.56042951409789,126.92078469857216]
    ]   
hongdae_data_list=[]

for location_x,location_y in location_list:
    # 장소 검색 (예: 홍대입구역 주변 맛집)
    places_result = gmaps.places_nearby(
        location=(location_x, location_y),  # 위도, 경도 (성수역 주변)
        radius=70,                  # 70m 반경
        keyword="맛집",               # 검색 키워드
        type="food",            # 식당만
        language="ko"                 # 한글로 결과 받기
    )

    #결과 출력
    for place in places_result['results']:
        save_datas(hongdae_data_list,place)

    time.sleep(3)
    if 'next_page_token' in places_result:
        next_page_token = places_result['next_page_token']
    else:
        next_page_token = False
    while next_page_token:
        time.sleep(2)  # Delay to allow next_page_token to become valid
        places_result = gmaps.places_nearby(page_token=next_page_token)

        for place in places_result['results']:
            save_datas(hongdae_data_list,place)
        break
