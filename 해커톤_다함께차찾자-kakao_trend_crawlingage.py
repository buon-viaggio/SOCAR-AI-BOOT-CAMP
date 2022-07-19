from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

import numpy as np
import pandas as pd


def selenium_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    # options.add_argument('window-size=1920x1080')
    options.add_argument('disable-gpu')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driveRoute = 'chromedrive route'
    driver = webdriver.Chrome(driveRoute, options=options)
    driver.implicitly_wait(1)

    return driver


if __name__ == "__main__":
    outputData = 'output excel route'

    # 명소 값 가져오기
    socar = pd.read_excel('C:\\Users\\real1\\Desktop\\socar\\space.xlsx')
    space = socar['명칭'].values.tolist()
    SearchValues1 = np.array([])

    # 셀레니움 init
    url = 'https://datatrend.kakao.com/'
    driver = selenium_driver()
    driver.get(url)
    action = ActionChains(driver)
    count = 0

    try:
        for name in space:
            count += 1

            # 검색창 클릭 및 검색어 입력
            search_box = driver.find_element(By.XPATH, "//*[@id='keyword']")
            search_box.send_keys(f'{name}')
            driver.find_element(By.XPATH, "//*[@id='root']/div/div/main/article/div[3]/div[2]/div[4]/div[2]/label[3]/span").click()

            # 검색어 조회하기 버튼 클릭
            driver.find_element(By.XPATH, "//*[@id='root']/div/div/main/article/div[4]/button[2]").click()
            #time.sleep(0.2)

            # 나이대별 검색 가져오기
            for i in range(6):
                try:
                    # 값 추출
                    action.move_to_element(driver.find_elements(By.CLASS_NAME, "highcharts-point")[i]).click().perform()

                    age = driver.find_element(By.XPATH, f"//*[contains(@id,'highcharts')]/div/span/div/ul/li/span[3]").text
                    action.pause(0.3)

                    SearchValues1 = np.append(SearchValues1, age)

                except Exception as e:
                    SearchValues1 = np.append(SearchValues1, 0)

            # 뒤로가기
            driver.back()

            # checking
            if count % 10 == 0 :
                print(count, name)

        reshaped = SearchValues1.reshape(count, 6)

    except Exception as e:
        print(name, e)
        outputdata1 = pd.DataFrame(reshaped, columns=['10', '20', '30', '40', '50', '60'])
        outputdata1.to_csv(outputData)
        exit()

    outputdata1 = pd.DataFrame(reshaped, columns=['10', '20', '30', '40', '50', '60'])
    outputdata1.to_csv(outputData, mode='w')
