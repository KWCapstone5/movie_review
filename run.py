import subprocess

# kobis_api.py 실행
subprocess.run(["python", "./static/images/kobis_api.py"])

# movie_image_maker.py 실행
subprocess.run(["python", "./static/images/kmdb_movie_info_maker.py"])
subprocess.run(["python", "./static/images/movie_image_maker.py"])

# app.py 실행
subprocess.run(["python", "./app.py"])
