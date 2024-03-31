import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))




#TOP10 영화 csv파일 경로
data = pd.read_csv('static/images/weekly_box_office_details.csv')

movieTitle = data.loc[:,'title']

url = "http://www.cgv.co.kr/movies/?lt=1&ft=1"

keyword = movieTitle[1] #첫번째 영화 제목 가져오기
print(keyword)
driver.get(url)
time.sleep(2)

driver.find_element(By.XPATH, "//*[contains(text(),'" + keyword + "')]").click()
movie_url = driver.current_url

def get_movie_reviews(url, page_num = 10):
    wd = webdriver.Chrome()
    wd.get(url)

    writer_list = [] # 작성자
    review_list = [] # 리뷰
    date_list = [] # 작성일

    for page_no in range(1, page_num + 1):
        try:
            page_ul = wd.find_element(By.ID,'paging_point')
            page_a = page_ul.find_element(By.LINK_TEXT, str(page_no))
            page_a.click()
            time.sleep(2)

            writers = wd.find_elements(By.CLASS_NAME, 'writer-name')
            writer_list += [writer.text for writer in writers]

            reviews = wd.find_elements(By.CLASS_NAME, 'box-comment')
            review_list += [ review.text for review in reviews]

            dates = wd.find_elements(By.CLASS_NAME, 'day')
            date_list += [date.text for date in dates]

            if page_no % 10 == 0: # 현재 페이지가 10페이지일 경우
                next_button = page_ul.find_element(By.CLASS_NAME, 'btn-paging.next')
                next_button.click() # 다음 10개 버튼 누름
                time.sleep(1)
        except NoSuchElementException:
            break
    # writer필요없음 date도 필요없음 review만 필요
    movie_review_df = pd.DataFrame({'Writer' : writer_list,
                                    'Review' : review_list,
                                    'Date' : date_list})

    wd.close()
    return movie_review_df
#  1 2 3 4 5 6 7 8 9 10
movie_review_df = get_movie_reviews(movie_url, 10) # 리뷰 받을 페이지 숫자(숫자를 크게해 끝까지 가져올 수 있음)
movie_review_df.to_csv('reviews.csv', index=False)