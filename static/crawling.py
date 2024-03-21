import urllib.request
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# 웹 애플리케이션의 테스트를 자동화하기 위한 프레임 워크
# 손으로 마우스 클릭해서 데이터를 검색하고 스크롤링 할 수 있다
import os
import time
# 중간마다 sleep를 걸어야 한다.

search_words = {
    "영화배우" : ['송강호', '조여정', '이정은', '현빈',
                  '손예진', '최우식', '이선균', '공유', '김다미', '김혜수', '박소담',  '이광수', '장혜진',
                  '정우성', '이병헌', '박해진', '김민재', '심은경', '안재홍', '이정재', '김남길', '김민희', '김지영',
                  '이이경', '유재명', '박명훈', '이영애', '전도연', '강하늘', '김무열', '공효진', '한석규', '김동욱',
                  '이지훈', '이제훈', '조한선', '라미란', '박지훈', '이하늬', '김민석', '정해인', '하정우', '이성민',
                  '김지수', '박정민', '송지효', '성동일', '이학주', '윤여정'],
    "드라마배우" : [
        '권나라', '김보라', '안효섭', '서지혜', '김정현', '조병규', '이성경', '남궁민', '오민석', '김혜수',
        '한석규', '유재명', '박은빈', '소주연', '주지훈', '김주헌', '김동희', '옥택연', '고수', '이연희', '이시언', '신동욱', '서현진', '진세연', '오정세',
        '이성민', '진경', '유태오', '임주환', '심은경', '임원희', '변정수', '주상욱', '윤나무', '이선균', '설인아', '김민규', '조보아',
        '이태환', '차예련', '최명길', '김홍파', '최윤소', '정유민', '김흥수', '정려원'
    ]
}

value = 0
for name in search_words['드라마배우']:
    binary = '/Users/geonukkim/Downloads/chromedriver'
    # 크롬 웹 브라우저를 열기 위한 크롬 드라이버
    # 팬텀 js를 이용하면 백그라운드로 실행 할 수 있음.

    browser = webdriver.Chrome(binary)
    # 브라우저를 인스턴스화

    browser.get("https://search.naver.com/search.naver?where=image&amp;sm=stb_nmr&amp;")
    # 네이버의 이미지 검색 url
    elem = browser.find_element_by_id("nx_query")
    # nx_query는 네이버 이미지 검색에 해당하는 input창 id

    search_name = '배우'+name
    elem.send_keys(search_name)
    elem.submit()
    # 스크롤링( 스크롤을 내리는 동작)을 반복할 횟수
    for i in range(1, 2):
        browser.find_element_by_xpath("//body").send_keys(Keys.END)
        # 웹창을 클릭 후 END키를 누르는 동작
        # 브라우저 아무데서나 END키 누른다고 페이지가 내려가지 않음
        # body를 활성화한 후 스크롤 동작
        time.sleep(1)
        # 이미지가 로드 되는 시간 5초
        # 로드가 되지 않은 상태에서 자장하기 되면 No image로 뜸.
    time.sleep(1)
    # 네크워크의 속도를 위해 걸어둔 sleep
    html = browser.page_source
    # 크롬 브라우저에서 현재 불러온 소스 코드를 가져옴
    soup = BeautifulSoup(html, "lxml")
    # beautiful soup을 사용해서 html 코드를 검색할 수 있도록 설정

    def fetch_list_url():
        # 이미지를 url이 있는 img 태그의 img클래스로 감
        params = []
        imgList = soup.find_all("img", class_="_img")
        for im in imgList:
            # params 리스트 변수에 images url을 담음
            params.append(im["src"])
        return params

    def fetch_detail_url():
        dir_name = "./" + search_name + '/'
        os.makedirs(dir_name)
        params = fetch_list_url()
        a = 1
        for p in params:
            # 다운받을 폴더경로 입력
            urllib.request.urlretrieve(p ,  dir_name + str(a) + ".jpg")
            a = a + 1

    fetch_detail_url()