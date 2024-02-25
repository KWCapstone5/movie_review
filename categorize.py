# 카테고리화해주는 작업
import ahocorasick
#
from konlpy.tag import Okt
import make_csv_wordcloud
# 객체생성
A = ahocorasick.Automaton()







# 긍정리뷰에서 특성에 따라서 리뷰 분류
# 어떤 단어가 많이 나올 수 록 긍정적이게 평가하는가



# 스토리,내용,유치,재미,감동,재미있다,재미있,재미있는,재미있어,재미있어요,재미있었,재미있었어,재미있었어요,재미있었음,재미있음,재미있지,재미있지만,개연성,각본,서사
story=['b급','각본','소재','작품성','작품','이야기','시나리오','삼류','신파','전개','짜임새','메세지','메시지','3류','스토리','내용','유치','재미','감동','재미','재미있다','재미있는','재미있어','재미있어요','재미있었','재미있었어','재미있었어요','재미있었음','재미있음','재미있지','재미있지만','개연성','각본','서사']
# 배우,연기,연기력
actor=['연기자','출연자','출연진','배우','연기','연기력','캐릭터']
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

voc =  list(make_csv_wordcloud.positive_review_forhashing)

story_sorted=[]
actor_sorted=[]
directing_sorted=[]

# Sort reviews
for i in voc:
    # 한문장씩 읽어서 == i
    okt_pos = Okt().morphs(i, norm=True,stem=True)    # 단어로 끊어서 리스트로
    # story에 있는 어떤 단어라도 voc에 포함되어 있으면 True를 반환하고, 그 결과 "있음"을 출력. 만약 story의 단어가 voc에 없다면
    for word in okt_pos:
        category = (A.get(word,None))#단어가 없으면 None

        if category == 1:
            story_sorted.append(i)
        elif category == 2:
            actor_sorted.append(i)
        elif category == 3:
            directing_sorted.append(i)





    # if any(word in okt_pos for word in story):
    #     story_sorted.append(i)
    #
    # if any(word in okt_pos for word in actor):
    #     actor_sorted.append(i)
    #
    # if any(word in okt_pos for word in directing):
    #     directing_sorted.append(i)

#    확인
print(story_sorted)
print(actor_sorted)
print(directing_sorted)





# 부정리뷰에서 특성에 따라서 리뷰 분류
# 어떤 단어가 많이 나올 수 록 부정적이게 평가하는가 부정적인 리뷰에서는 어떤 단어가 많이 나왔을까

# 지루,재미없,재미없는,재미없어,재미없어요,재미없었,재미없었어,재미없었어요,재미없었음,재미없음,재미없지,재미없지만,개연성,각본,서사
# 배우,연기,연기력,발연기
# 연출,볼거리,보는,듣는,음악,노래,음향,분위기,액션,영상,편집,CG,cg,영상미
# 기타


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
       '재미없지만']
# 배우,연기,연기력
actor=['연기자','출연자','출연진','배우','연기','연기력','캐릭터','발연기']
# 연출,볼거리,보는,듣는,음악,노래,음향,분위기,액션,영상,편집,CG,cg,영상미
directing=['그래픽','씬','장면','OST','ost','색감','영상미','카메라','앵글','풍경','연출','볼거리','보는','듣는','음악','노래','음향','분위기','액션','영상','편집','CG','cg','3d','3D','3d로','3D로']
# ahocorasick 저장
# add_word(word, value) 메서드에서 word는 검색하고자 하는 패턴(단어)를 나타내고, value는 해당 패턴이 검색될 때 반환하고자 하는 값을 나타냅니다.
# for word in story:
#     A.add_word(word, 1)
#
# for word in actor:
#     A.add_word(word, 2)
#
# for word in directing:
#     A.add_word(word, 3)
# # Ahocorasick 저장완료
# A.make_automaton()
#
# # 리뷰들 중 해당하는 단어가 있으면 거기에 append
# # precontion: 리뷰들이 리스트로 있어야함 postcontion: 각각의 리스트에 해당하는 단어가 있으면 그 카테고리에 추가
#
# voc =  list(make_csv_wordcloud.negative_review_forhashing)
#
# story_sorted=[]
# actor_sorted=[]
# directing_sorted=[]
#
# # Sort reviews
# for i in voc:
#     # 한문장씩 읽어서 == i
#     okt_pos = Okt().morphs(i, norm=True,stem=True)    # 단어로 끊어서 리스트로
#     # story에 있는 어떤 단어라도 voc에 포함되어 있으면 True를 반환하고, 그 결과 "있음"을 출력. 만약 story의 단어가 voc에 없다면
#     for word in okt_pos:
#         category = (A.get(word,None))#단어가 없으면 None
#
#         if category == 1:
#             story_sorted.append(i)
#         elif category == 2:
#             actor_sorted.append(i)
#         elif category == 3:
#             directing_sorted.append(i)
#    확인
# print(story_sorted)
# print(actor_sorted)
# print(directing_sorted)


































# test용
# import os
#
# os.chdir('C:/Users/{user}/IdeaProjects/flaskapp/venv/Lib/site-packages/konlpy/java/open-korean-text-2.1.0.jar')
# os.getcwd()
#
# jar xvf open-korean-text-2.1.0.jar
#
#
# # data 확인
# with open(f"/usr/local/lib/python3.8/dist-packages/konlpy/java/org/openkoreantext/processor/util/noun/names.txt") as f:
#     data = f.read()

# okt 분류
# {
#     "Adjective": "형용사",
#     "Adverb": "부사",
#     "Alpha": "알파벳",
#     "Conjunction": "접속사",
#     "Determiner": "관형사",
#     "Eomi": "어미",
#     "Exclamation": "감탄사",
#     "Foreign": "외국어, 한자 및 기타기호",
#     "Hashtag": "트위터 해쉬태그",
#     "Josa": "조사",
#     "KoreanParticle": "(ex: ㅋㅋ)",
#     "Noun": "명사",
#     "Number": "숫자",
#     "PreEomi": "선어말어미",
#     "Punctuation": "구두점",
#     "ScreenName": "트위터 아이디",
#     "Suffix": "접미사",
#     "Unknown": "미등록어",
#     "Verb": "동사"
# }
