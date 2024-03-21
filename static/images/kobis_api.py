import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime, timedelta
import os
import re

# 유효하지 않은 파일/폴더 이름 문자 제거 또는 대체 함수
def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', '', filename)  # 유효하지 않은 문자를 제거

# 영화 상세 정보 조회 함수
def get_movie_info(api_key, movie_id):
    url = f"https://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.xml?key={api_key}&movieCd={movie_id}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'xml')
    
    # 영화 기본 정보 추출
    movie_info = {
        'movieCd': movie_id,
        'title': sanitize_filename(soup.find('movieNm').text),
        'release_date': soup.find('openDt').text,
        'director': sanitize_filename(soup.find('director').find('peopleNm').text) if soup.find('director') else 'Unknown',
        'actors': ", ".join([sanitize_filename(actor.find('peopleNm').text) for actor in soup.find_all('actor')[:10]])
    }
    
    return movie_info
    
# 일별 박스오피스 정보 조회 함수
def fetch_daily_box_office(api_key, target_date):
    url = f"http://kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.xml?key={api_key}&targetDt={target_date}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'xml')
    
    movies = []
    for item in soup.find_all('dailyBoxOffice'):
        movie_id = item.find('movieCd').text
        movie_info = get_movie_info(api_key, movie_id)
        movies.append(movie_info)
    
    return movies

# API 키와 대상 날짜 설정
api_key = ''
yesterday = datetime.now() - timedelta(days=1)
target_date = yesterday.strftime("%Y%m%d")

# 영화 정보 가져오기
movies = fetch_daily_box_office(api_key, target_date)

# CSV 파일로 저장
csv_file_path = './static/images/weekly_box_office_details.csv'
with open(csv_file_path, 'w', newline='', encoding='utf-8') as file:
    fieldnames = ['movieCd', 'title', 'release_date', 'director', 'actors']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    
    writer.writeheader()
    for movie in movies:
        writer.writerow(movie)

print(f"Data saved to {csv_file_path}")
