import pandas as pd
import requests
from tqdm import tqdm

import re
import numpy as np
from transformers import ElectraTokenizer, ElectraForSequenceClassification
import torch
import time
from wordcloud import WordCloud

# 1. 다음 API에서 가져온 레이팅을 기반으로 긍정(1) 또는 부정(0)으로 분류하여 CSV 파일 만들기
def categorize_rating(rating):
    if 6 <= rating <= 10:
        return 1  # 긍정
    elif 1 <= rating <= 4:
        return 0  # 부정
    else:
        return -1  # 레이팅이 범위에 속하지 않으면 무시

# 댓글을 가져오기 위한 URL 초기 설정
movie_id = 149662594
offset = 0
comments = []

# 모든 댓글을 가져올 때까지 반복
while True:
    url = f'https://comment.daum.net/apis/v1/posts/{movie_id}/comments?parentId=0&offset={offset}&limit=100&sort=LATEST&isInitial=false&hasNext=true'
    response = requests.get(url)
    data = response.json()

    # 댓글 추출
    current_comments = [{"comment": comment['content'], "rating": comment['rating']} for comment in data]
    comments.extend(current_comments)

    # 다음 페이지가 있는지 확인
    if len(data) < 100:
    # if len(data) == 100:
        break

    # 다음 페이지를 위해 offset 증가
    offset += 100

    # 서버 부하를 줄이기 위한 딜레이
    time.sleep(0.5)

# DataFrame으로 변환하여 CSV 파일로 저장
df_ground_truth = pd.DataFrame(comments)
df_ground_truth["sentiment_ground_truth"] = df_ground_truth["rating"].apply(categorize_rating)

# 2. 감성 분석 모델을 사용하여 댓글의 감성 예측
# KcELECTRA 토크나이저와 모델 로드
tokenizer = ElectraTokenizer.from_pretrained("beomi/KcELECTRA-base-v2022")
model = ElectraForSequenceClassification.from_pretrained("beomi/KcELECTRA-base-v2022")

# 예측된 감성 저장할 리스트
predicted_sentiments = []

for comment in tqdm(comments):
    #여기를 고치는게 좋을듯  숫자도 받을 수 있게
    #숫자 한글만 냅두고 나머지는 삭제
    new_sentence = re.sub(r'[^가-힣0-9 ]', '', comment["comment"])
    new_sentence = tokenizer(new_sentence, return_tensors='pt', truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**new_sentence)
    logits = outputs.logits
    probabilities = torch.softmax(logits, dim=1)
    score = probabilities[0][1].item()  # 긍정 클래스의 확률 (1: 긍정, 0: 부정)
    predicted_sentiment = 1 if score > 0.5 else 0
    predicted_sentiments.append(predicted_sentiment)

# 예측된 감성을 DataFrame에 추가
df_ground_truth["sentiment_predicted"] = predicted_sentiments

# 정확도 계산 (5점은 무시)
filtered_df = df_ground_truth[df_ground_truth["rating"] != 5]
accuracy = np.mean(filtered_df["sentiment_ground_truth"] == filtered_df["sentiment_predicted"])
# new=(filtered_df["sentiment_ground_truth"] == filtered_df["sentiment_predicted"]).sum()
# //filtered_df['sentiment_predicted'].sum()
print(accuracy)
print(filtered_df['sentiment_predicted'].sum())


# 결과 DataFrame을 CSV 파일로 저장
filtered_df.to_csv('data/ground_truth_and_predictions_electra.csv', index=False, encoding='utf-8-sig')

# 결과를 text파일로 저장
# filtered_df.to_csv('test.txt', index = False)
#
#
# # 나눔고딕 폰트 파일의 경로 지정
# nanum_gothic_font_path = 'NanumGothic.ttf' # 예시 경로입니다. 실제 경로에 맞게 수정하세요.
#
#
# wordcloud_directory = 'static/images/wordcloud'
#
# def color(word,random_state=None,**kwargs):
#     return 'rgb(0,0,255)' #blue
# # df 형태는 기본적으로 object라서
positive_reviews = df_ground_truth[df_ground_truth["sentiment_predicted"] == 1]["comment"]
#   hashong.py에서 사용
positive_review_forhashing = df_ground_truth[df_ground_truth["sentiment_predicted"] == 1]["comment"]

# 그냥하면 안되고 문자열 형식으로 바꿔주고 난 다음에 생성가능
positive_reviews= ' '.join(positive_reviews)
# print(positive_reviews)

# positive_wordcloud = WordCloud(
#     font_path=nanum_gothic_font_path,
#     width=800,
#     height=400,
#     background_color='white',
#     prefer_horizontal=True,
#     min_word_length=3,
#     max_words=10,
#     color_func=color
#
#
# ).generate(positive_reviews)
# positive_wordcloud.to_file(os.path.join(wordcloud_directory, "positive_wordcloud.jpg"))
#

# 부정리뷰
# def color(word,random_state=None,**kwargs):
#     return 'rgb(255,0,0)' #red
#
# negative_reviews = df_ground_truth[df_ground_truth["sentiment_predicted"] == 0]["comment"]
# negative_reviews= ' '.join(negative_reviews)
#
# # # 부정 리뷰 워드 클라우드 생성
# negative_wordcloud = WordCloud(
#     font_path=nanum_gothic_font_path,
#     width=800,
#     height=400,
#     background_color='white',
#     prefer_horizontal=True,
#     min_word_length=3,
#     max_words=10,
#     color_func=color
# ).generate(negative_reviews)
#
# # 워드 클라우드 이미지 저장
# negative_wordcloud.to_file(os.path.join(wordcloud_directory, "negative_wordcloud.jpg"))