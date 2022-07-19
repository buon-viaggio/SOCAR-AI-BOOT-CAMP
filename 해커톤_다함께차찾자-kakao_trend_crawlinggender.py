from selenium import webdriver
from selenium.webdriver.common.by import By

import time
import pandas as pd


def selenium_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    # options.add_argument('window-size=1920x1080')
    options.add_argument('disable-gpu')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driveRoute = 'chromedrive route'
    driver = webdriver.Chrome(driveRoute, options=options)
    driver.implicitly_wait(10)

    return driver


if __name__ == "__main__":
    # 명소 값 가져오기
    socarfileRoute = 'socar data excel route'
    socar = pd.read_excel(socarfileRoute)
    space = socar['명칭'].values.tolist()
    SearchValues1 = []

    outputData = 'output excel route'

    # 셀레니움 init
    url = 'https://datatrend.kakao.com/'
    driver = selenium_driver()
    driver.get(url)

    count = 0

    try:
        for name in space:

            count += 1

            # 검색창 클릭 및 검색어 입력
            search_box = driver.find_element(By.XPATH, "//*[@id='keyword']")
            search_box.send_keys(f'{name}')

            # 검색어 조회하기 버튼 클릭
            driver.find_element(By.XPATH, "//*[@id='root']/div/div/main/article/div[4]/button[2]").click()
            time.sleep(0.5)

            # 여성 비율
            try:
                # 값 추출
                values1 = driver.find_element(By.XPATH, "//*[@id='root']/div/div/main/article/div[1]/section[2]/div/div[2]/span[2]").text
                SearchValues1.append(values1)
            except Exception as e:
                SearchValues1.append(0)

            # 뒤로가기
            driver.back()

            # checking
            if count % 10 == 0 :
                print(count, name, values1)

    except Exception as e:
        outputdata1 = pd.DataFrame(SearchValues1, columns=['여성'])
        outputdata1.to_csv(outputData)

        print(name, e)
        exit()

    outputdata1 = pd.DataFrame(SearchValues1, columns=['여성'])
    outputdata1.to_csv(outputData, mode='w')
