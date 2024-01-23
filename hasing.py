from konlpy.tag import Okt
from collections import Counter
from ckonlpy.tag import Twitter

import pandas as pd
# java home 설정 필요 konlpy 사용하려면
voc = make_csv_wordcloud.positive_reviews

okt_pos = Okt().pos(voc, norm=True)    # 형태소 분석
words = [x for x, y in okt_pos if y in ['Noun']]  # 명사만 추출

counter = Counter(words).most_common(10)   # 빈도수 기반
print(counter)