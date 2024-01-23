#점수분포 보여주는 기능
import make_csv_wordcloud
from collections import Counter


import matplotlib.pyplot as plt

ratings = [d['rating'] for d in make_csv_wordcloud.comments]

# 'rating'의 값을 세고, 결과를 사전 형태로 반환합니다.
count = Counter(ratings)
# 바 차트를 생성합니다.
plt.bar(count.keys(), count.values())

#레이블 한글로
# x축에 레이블을 추가합니다.
plt.xlabel('rating')

# y축에 레이블을 추가합니다.
plt.ylabel('frequency')
# frequency를 가로로 출력하기위해서
plt.text(-0.1, 0.5, 'Count', rotation=0, va='center', ha='right', transform=plt.gca().transAxes)

# 차트에 제목을 추가합니다.
plt.title('ratio')
# 저장하고
plt.savefig('plot.png')
# 생성된 그래프를 화면에 출력하고, 내부적으로 그래프를 생성하기 위해 사용했던 메모리를 정리(clear)하는 역할

plt.show()
