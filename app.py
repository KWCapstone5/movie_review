from flask import Flask, render_template, url_for
import os
import urllib.parse
import re
import csv

app = Flask(__name__)

# URL 인코딩 필터 정의
def url_encode_filter(s):
    return urllib.parse.quote(s)

# 필터를 Flask 앱에 추가
app.jinja_env.filters['url_encode'] = url_encode_filter

# 파일 이름에서 숫자 추출
def extract_number(filename):
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else 0

# URL에 적합하게 영화 제목 변환
def format_movie_title(title):
    return title.replace(' ', '_').lower()

@app.route('/')
def movie_info():
    movies = []
    movie_base_folder = 'static/images/movies'
    movie_folders = [f for f in os.listdir(movie_base_folder) if os.path.isdir(os.path.join(movie_base_folder, f))]

    for movie_title in movie_folders:
        poster_folder_path = os.path.join(movie_base_folder, movie_title, 'poster')
        try:
            poster_files = os.listdir(poster_folder_path)
            # 포스터 이미지가 여러 개 있을 수 있으나, 여기서는 첫 번째 파일만 사용
            if poster_files:
                image_file = poster_files[0]
                image_url = os.path.join(poster_folder_path, image_file).replace('\\', '/')
                # 영화 제목에서 URL에 사용할 수 없는 문자 처리
                movie_url_title = urllib.parse.quote(movie_title)
                movies.append({
                    "title": movie_title,
                    "image_url": image_url,
                    "url": movie_url_title
                })
        except FileNotFoundError:
            print(f"Poster not found for movie: {movie_title}")

    return render_template('movie_info.html', movies=movies)

@app.route('/<movie_name>')
def movie(movie_name):
    movie_folder = f'static/images/movies/{movie_name}'
    cast_info = []
    actor_image_folder = os.path.join(movie_folder, 'actors')
    if os.path.exists(actor_image_folder):
        for actor_image in os.listdir(actor_image_folder):
            if actor_image.endswith('.jpg'):
                actor_name = os.path.splitext(actor_image)[0]
                image_url = os.path.join(actor_image_folder, actor_image).replace('\\', '/')
                cast_info.append({"name": actor_name, "image_url": image_url})

    # 포스터 및 감독 이미지는 예시로 하나만 처리합니다.
    # 실제 애플리케이션에서는 필요에 따라 다른 로직을 적용해야 할 수 있습니다.
    poster_image_url = ""
    poster_folder = os.path.join(movie_folder, 'poster')
    if os.listdir(poster_folder):
        poster_image_url = os.path.join(poster_folder, os.listdir(poster_folder)[0]).replace('\\', '/')

    return render_template('movie.html', movie_name=movie_name, cast_info=cast_info, poster_image_url=poster_image_url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)