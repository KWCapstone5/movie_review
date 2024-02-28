import os

import pandas as pd
from tqdm import tqdm

from transformers import ElectraTokenizer, ElectraForSequenceClassification
import torch
from wordcloud import WordCloud




#리뷰 csv파일을 읽어서 데이터프레임으로 만들기

df_ground_truth = pd.read_csv('data/CGVreviews.csv')

#파일별 리뷰생성하게 하기



# df_ground_truth에서 c1열을 가져와서 리스트로 만들기
comments = df_ground_truth['Review'].tolist()
print(comments)
print(len(comments))
# 2. 감성 분석 모델을 사용하여 댓글의 감성 예측
# KcELECTRA 토크나이저와 모델 로드
tokenizer = ElectraTokenizer.from_pretrained("beomi/KcELECTRA-base-v2022")
model = ElectraForSequenceClassification.from_pretrained("beomi/KcELECTRA-base-v2022")

# 예측된 감성 저장할 리스트
predicted_sentiments = []

for comment in tqdm(comments):
    #여기를 고치는게 좋을듯  숫자도 받을 수 있게
    #숫자 한글만 냅두고 나머지는 삭제
    new_sentence = tokenizer(comment, return_tensors='pt', truncation=True, padding=True)
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








#categorize.py에서 하는 일 여기서 처리
import ahocorasick

from konlpy.tag import Okt
# 객체생성
A = ahocorasick.Automaton()
# 카테고리별 단어 리스트
# 스토리,내용,유치,재미,감동,재미있다,재미있,재미있는,재미있어,재미있어요,재미있었,재미있었어,재미있었어요,재미있었음,재미있음,재미있지,재미있지만,개연성,각본,서사
story=['b급','각본','소재','작품성','작품','이야기','시나리오','삼류','신파','전개','짜임새','메세지','메시지','3류','스토리','내용','유치','개연성','각본','서사','지루',
       '재미없',
       '재미없는',
       '재미없어',
       '재미없어요',
       '재미없었',
       '재미없었어',
       '재미없었어요',
       '재미없었음',
       '재미없음',
       '재미없지',
       '재미없지만','b급','각본','소재','작품성','작품','이야기','시나리오','삼류','신파','전개','짜임새','메세지','메시지','3류','스토리','내용','유치','재미','감동','재미','재미있다','재미있는','재미있어','재미있어요','재미있었','재미있었어','재미있었어요','재미있었음','재미있음','재미있지','재미있지만','개연성','각본','서사']
# 배우,연기,연기력
actor=['연기자','출연자','출연진','배우','연기','연기력','캐릭터','연기자','출연자','출연진','배우','연기','연기력','캐릭터','발연기']
# 연출,볼거리,보는,듣는,음악,노래,음향,분위기,액션,영상,편집,CG,cg,영상미
directing=['화려','그래픽','씬','장면','OST','ost','색감','영상미','카메라','앵글','풍경','연출','볼거리','보는','듣는','음악','노래','음향','분위기','액션','영상','편집','CG','cg','영상미','3d','3D','3d로','3D로']
# ahocorasick 저장
# add_word(word, value) 메서드에서 word는 검색하고자 하는 패턴(단어)를 나타내고, value는 해당 패턴이 검색될 때 반환하고자 하는 값을 나타냅니다.
for word in story:
    A.add_word(word, 1)

for word in actor:
    A.add_word(word, 2)

for word in directing:
    A.add_word(word, 3)

# Ahocorasick 저장완료
A.make_automaton()

# 리뷰들 중 해당하는 단어가 있으면 거기에 append
# precontion: 리뷰들이 리스트로 있어야함 postcontion: 각각의 리스트에 해당하는 단어가 있으면 그 카테고리에 추가

# df_ground_truth
voc =list(df_ground_truth['Review'])

story_sorted=[] #1
actor_sorted=[] #2
directing_sorted=[]#3

# 데이터프레임에 'category' 열을 추가하고 문자열로 초기화합니다.
df_ground_truth['category']= 'story'
filtered_df = df_ground_truth.reset_index()  # 인덱스를 리셋합니다.

for idx, i in enumerate(voc):
    # 한문장씩 읽어서 == i
    okt_pos = Okt().morphs(i, norm=True,stem=True)    # 단어로 끊어서 리스트로
    # story에 있는 어떤 단어라도 voc에 포함되어 있으면 True를 반환하고, 그 결과 "있음"을 출력. 만약 story의 단어가 voc에 없다면
    for word in okt_pos:
        category = (A.get(word,None))#단어가 없으면 None

        if category == 1:
            story_sorted.append(i)
            # Assign category values to 'category' column
            # filtered_df.loc[filtered_df['comment'] 'category'] = 'story'
            # df.loc[행의 인덱스, 열 이름] = 바꿀 값
            filtered_df.loc[idx, 'category'] = 'story'  # 인덱스를 사용하여 'category' 값을 변경합니다.
        elif category == 2:
            actor_sorted.append(i)
            filtered_df.loc[idx, 'category'] = 'actor'
        elif category == 3:
            directing_sorted.append(i)
            filtered_df.loc[idx, 'category'] = 'directing'
        # 데이터프레임에 추가


# #    확인
print(story_sorted)
print(actor_sorted)
print(directing_sorted)
# 생성된 데이터프레임 확인
print(filtered_df.head())
#  데이터프레임을 CSV 파일로 저장
filtered_df.to_csv('data/metadata.csv', index=False, encoding='utf-8-sig')






# 나눔고딕 폰트 파일의 경로 지정
nanum_gothic_font_path = 'NanumGothic.ttf' # 예시 경로입니다. 실제 경로에 맞게 수정하세요.


wordcloud_directory = 'static/images/wordcloud'


#긍정리뷰
def color(word,random_state=None,**kwargs):
    return 'rgb(0,0,200)' #blue
# # df 형태는 기본적으로 object라서
positive_reviews = df_ground_truth[df_ground_truth["sentiment_predicted"] == 1]["Review"]
#   categorize.py에서 사용 make_csv_wordcloud로 기능 합침
# positive_review_forhashing = df_ground_truth[df_ground_truth["sentiment_predicted"] == 1]["Review"]

# 그냥하면 안되고 문자열 형식으로 바꿔주고 난 다음에 생성가능
positive_reviews= ' '.join(positive_reviews)
# print(positive_reviews)


# 긍정 리뷰 워드 클라우드 생성 (단어 10개) 해결
positive_wordcloud = WordCloud(
    font_path=nanum_gothic_font_path,
    width=800,
    height=400,
    background_color='white',
    prefer_horizontal=True,
    min_word_length=2,
    max_words=10,
    color_func=color


).generate(positive_reviews)
positive_wordcloud.to_file(os.path.join(wordcloud_directory, "positive_wordcloud.jpg"))


# 부정리뷰
def color(word,random_state=None,**kwargs):
    return 'rgb(200,0,0)' #red
# df_ground_truth에서 sentiment_predicted가 0인 리뷰만 추출
negative_reviews = df_ground_truth[df_ground_truth["sentiment_predicted"] == 0]["Review"]
# 그냥하면 안되고 문자열 형식으로 바꿔주고 난 다음에 생성가능
negative_reviews= ' '.join(negative_reviews)

# # 부정 리뷰 워드 클라우드 생성
negative_wordcloud = WordCloud(
    font_path=nanum_gothic_font_path,
    width=800,
    height=400,
    background_color='white',
    prefer_horizontal=True,
    min_word_length=2,
    max_words=10,
    color_func=color
).generate(negative_reviews)

# 워드 클라우드 이미지 저장
negative_wordcloud.to_file(os.path.join(wordcloud_directory, "negative_wordcloud.jpg"))

