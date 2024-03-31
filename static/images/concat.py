
# 주간영화리스트를 받아와서 그 정보를 기존 movieDataSet 추가
# 작동 됨
import pandas as pd
# 주간영화리스트를 받아와서 그 정보를 기존 movieDataSet 추가
df2 = pd.read_csv('./updated_weekly_box_office_details.csv')

# df2.columns = ['movieCode', 'title', 'summary', 'genres']
# 다중 칼럼 선택
# movieCd,title,summary,genres

selected_columns = df2[['movieCd', 'title', 'summary','genres']]

# Read the CSV file into a DataFrame

# 합치기 전에 칼럼명과 수를 맞춰줘야지
# 길이 다르면 안됨 합치기 안됨
selected_columns.to_csv('./movieDataSet.csv', mode='a', index=False, header=False)