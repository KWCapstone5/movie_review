from flask import Flask, render_template, url_for, render_template_string, request
import os
import urllib.parse
import re
import csv
import sqlite3
import pandas as pd
app = Flask(__name__)


                                           # fetchall()
def url_encode_filter(s):
    return urllib.parse.quote(s)

# 파일 이름에서 숫자 추출
def extract_number(filename):
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else 0

# URL에 적합하게 영화 제목 변환
def format_movie_title(title):
    return title.replace(' ', '_').lower()

# @app.route('/')
# def form():
#     return render_template_string('''
#         <form action="/submit" method="post">
#             이메일: <input type="text" name="email"><br>
#             문의 내용: <textarea name="content"></textarea><br>
#             <input type="submit" value="제출">
#         </form>
#     ''')

@app.route('/')
def movie_info():
    # 여부분에서 일단 csv파일 읽어오기?
    df = pd.read_csv('static/images/updated_weekly_box_office_details.csv')
    # 리뷰에서 긍정비율을 표시하면 좋겟다
    # df에서 사용할 수 있는 칼럼이름
    # ['movieCd', 'title', 'release_date', 'director', 'actors', 'genres', 'keyword', 'summary'],
    title = list(df['title'])  # 특정 열의 데이터에 접근
    release_date = list(df['release_date'])
    director = list(df['director'])
    actors = list(df['actors'])
    genres = list(df['genres'])
    keyword = list(df['keyword'])
    summary = list(df['summary'])

    # render_template 기능을 사용하면, 프론트로 변수를 전송할 수 잇음
    return render_template('new.html', num=list(range(10)), title=title, release_date=release_date, genres=genres)


def get_movie_details(movie_name):
    movie_details = {}
    with open('static/images/updated_weekly_box_office_details.csv', mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            print(row['title'] )
            print(movie_name)
            if row['title'] == movie_name:
                movie_details = row
                break
    return movie_details

@app.route('/<movie_name>')
def movie(movie_name):
    # moviefolder 파일명 바꾸고 이름에서 번호
    # 나머지 내용들은  csv에서 받아오면 movie_details처럼 movie_name도
    movie_folder = f'static/images/movies/{movie_name}'
    movie_details = get_movie_details(movie_name)
    cast_info = []
    actor_image_folder = os.path.join(movie_folder, 'actors')
    if os.path.exists(actor_image_folder):
        for actor_image in os.listdir(actor_image_folder):
            if actor_image.endswith('.jpg'):
                actor_name = os.path.splitext(actor_image)[0]
                image_url = os.path.join(actor_image_folder, actor_image).replace('\\', '/')
                cast_info.append({"name": actor_name, "image_url": image_url})

    poster_image_url = ""
    poster_folder = os.path.join(movie_folder, 'poster')
    if os.listdir(poster_folder):
        poster_image_url = os.path.join(poster_folder, os.listdir(poster_folder)[0]).replace('\\', '/')

    return render_template('movie.html',
                           movie_name=movie_name,
                           cast_info=cast_info,
                           poster_image_url=poster_image_url,
                           movie_details=movie_details)







#
# @app.route('/submit', methods=['POST'])
# def submit():
#     email = str(request.form['email'])
#     content = str(request.form['content'])
#     # 여기서 데이터 처리를 할 수 있습니다.
#     conn = sqlite3.connect('identifier.sqlite')#파일 경로를 잘 지정하자 ....
#     # 커서 획득
#     c = conn.cursor()
#     # flask에서 지원하는 sqlite 문법확인 필요 ....
#     c.execute('INSERT INTO contact (content, email) VALUES (?, ?)', (content, email))
#     conn.commit()
# # 연결 닫기
#     conn.close()
#     return "제출 성공하였습니다"
#
# @app.route('/')
# # render_template을 통해 db.html에 (왼쪽)user 라는 이름에 (오른쪽) user를 할당한다는 뜻이다.
# def test():
#
#     return render_template('contact.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)