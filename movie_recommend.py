from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer

import pandas as pd
import numpy as np
from dotenv import load_dotenv
load_dotenv(verbose=True)

df = pd.read_csv('./movieDataSet.csv')

tf_idf = TfidfVectorizer()
df['summary'] = df['summary'].fillna('')
tf_idf_matrix = tf_idf.fit_transform(df['summary'])

cosine_sim = linear_kernel(tf_idf_matrix, tf_idf_matrix)
# 맵핑(mapping)
indices = pd.Series(df.index, index=df['movieCode'])

# movieCode
# 171883        0
# 169581        1
# 155665        2
# 165461        3
# 158256        4


#
# # # 영화제목 입력하면 그걸 인덱스 몇번째인지 확인해서 그걸토대로 작동  대신 title을 넣어 검색할 수 있게 수정
# # #
# # 입력된
def get_recommendations(index, size, cosine_sim=cosine_sim):
    # movieCode 대신 title을 넣어 검색할 수 있게 수정

    # 입력된 무비코드를 기반으로 인덱스를 가져옵니다
    idx = indices[index]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    # 당연히 가장 유사한 건 자기 자신이기 때문에 0번 배열은 제외하고 1번 배열부터
    sim_scores = sim_scores[1:size+1]
    movie_indices = [i[0] for i in sim_scores]
    score = [i[1] for i in sim_scores]
# 이는 'movieCode' 열의 특정 행들만을 선택하여 반환합니다
    return df['title'].iloc[movie_indices]

# 지금은 무비코드가 아닌 인덱스 기반으로 작동되고 있음
# 강철비 인덱스 입력했을 때
title=input('영화제목을 입력하세요: ')
# 사용자가 입력한 영화 제목에 해당하는 행을 선택해서 그에 맞는 인덱스를 찾음
new=((df[df['title'] == title]).index[0])

a=list(get_recommendations(new, 4))
# 추천된 영화제목만 가져와서 처리
print(a)


# 인덱스 영화제목
# 11029                  낯선 사람
# 2905              강철비2: 정상회담
# 83                        공조
# 9235                    외사경찰
# 15069    광복70년 특별기획 슈퍼코리아의 꿈


