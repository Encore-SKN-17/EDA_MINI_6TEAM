import api.googlemap_api_hongdae as hapi
import api.googlemap_api_itaewon as iapi
import api.googlemap_api_seongsu as sapi
import numpy as np
import pandas as pd


# data 담을 리스트 생성
data_total_list=[]
data_total_list.extend(hapi.hongdae_data_list)
data_total_list.extend(iapi.itaewon_data_list)
data_total_list.extend(sapi.seongsu_data_list)


# 중복값 처리하기 위해서 set 로 만들어서 data_set에 저장
data_set = set(data_total_list)

# 중복값 처리 후 list로 다시 변환
final_data_list = list(data_set)

# 리스트 정보를 분리해 담을 딕셔너리 생성
final_data_dict={
    'restaurant_name': [],
    'googleMap_review_point' : [],
    'googleMap_review_count' : [],
    'address' : []
}

# 데이터 ,, 로 분리해 final_data_dict 에 각 값을 저장
for data_contents in final_data_list:
    data_content = data_contents.split(sep=",,")
    final_data_dict['restaurant_name'].append(data_content[0])
    final_data_dict['googleMap_review_point'].append(float(data_content[1]))
    final_data_dict['googleMap_review_count'].append(int(data_content[2]))
    final_data_dict['address'].append(data_content[3])

# final_data_dict 로 DataFrame 만든 후 csv 파일로 만들어 저장
googlemap_df = pd.DataFrame(final_data_dict)
googlemap_df.to_csv('googlemap_data.csv',encoding='utf-8')