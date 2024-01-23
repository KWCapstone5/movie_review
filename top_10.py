# 리뷰에서 많이 나온 단어보여주기
# # 언급된 수 konply로 하거나 SOYNLP


# java home 경로설정 필요 konlpy 사용하려면

from konlpy.tag import Okt
from collections import Counter
import make_csv_wordcloud
#불용어 정하기
# 긍정리뷰
voc = make_csv_wordcloud.positive_reviews
okt_pos = Okt().pos(voc, norm=True,stem=True)    # 형태소 분석
words = [x for x, y in okt_pos if y in ['Noun']  ]  # 명사만 추출
words=[x for x in words if len(x)>1] # 한 글자 이상만
counter = Counter(words).most_common(10)   # 빈도수 기반
print(counter)

#
# # 부정리뷰
# voc = make_csv_wordcloud.negative_reviews
# okt_pos = Okt().pos(voc, norm=True,stem=True)    # 형태소 분석
# words = [x for x, y in okt_pos if y in ['Noun']]  # 명사만 추출
#
# counter = Counter(words).most_common(10)   # 빈도수 기반
# print(counter)

