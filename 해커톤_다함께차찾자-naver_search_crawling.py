from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

import time
import pandas as pd

def selenium_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    # options.add_argument('window-size=1920x1080')
    driveRoute = 'chromedrive route'
    options.add_argument('disable-gpu')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(driveRoute, options=options)
    driver.implicitly_wait(1)

    return driver


if __name__ == "__main__":
    # 명소 값 가져오기
    socarfileRoute = 'socar data excel route'
    outputPc = 'output(pc) excel route'
    outputMb = 'output(mobile) excel route'
    socar = pd.read_excel('socarfileRoute')
    space = socar['명칭'].values.tolist()
    pcValues = []
    mbValues = []

    # 셀레니움 init
    url = 'https://manage.searchad.naver.com/customers/2607514/tool/keyword-planner'
    driver = selenium_driver()
    driver.get(url)
    action = ActionChains(driver)
    count = 0

    # 로그인
    # naverId = 'test'
    # naverPw = 'test'
    # driver.find_element(By.XPATH, "//*[@id='root']/div/div/div/div/div/div[2]/div/a").click()
    # driver.find_element(By.XPATH, "//*[@id='container']/div/div/div[2]/div[1]/button").click()
    # box1 = driver.find_element(By.XPATH, "//*[@id='id']")
    # box1.send_keys(naverId)
    # box2 = driver.find_element(By.XPATH, "//*[@id='pw']")
    # box2.send_keys(naverPw)
    # driver.find_element(By.XPATH, "//*[@id='log.login']").click()

    time.sleep(30)

    try:
        for name in space:
            count += 1

            # 검색창 클릭 및 검색어 입력
            search_box = driver.find_element(By.XPATH, "//*[@id='root']/div/div[2]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/div/textarea")
            search_box.clear()
            search_box.send_keys(f'{name}')

            # 검색어 조회하기 버튼 클릭
            driver.find_element(By.XPATH, "//*[@id='root']/div/div[2]/div/div/div[2]/div[1]/div[1]/div[3]/button").click()
            time.sleep(0.5)

            # pc / mobile 별도 추출
            try:
                # 값 추출
                pc = driver.find_element(By.XPATH, "//*[@id='root']/div/div[2]/div/div/div[2]/div[1]/div[2]/div[2]/div/div[2]/table/tbody/tr/td[3]").text
                mb = driver.find_element(By.XPATH, "//*[@id='root']/div/div[2]/div/div/div[2]/div[1]/div[2]/div[2]/div/div[2]/table/tbody/tr/td[4]").text

                pcValues.append(pc)
                mbValues.append(mb)

            except Exception as e:
                print(e)
                pcValues.append(-1)
                mbValues.append(-1)

            # checking
            if count % 10 == 0 :
                print(count, name, pc, mb)


    except Exception as e:
        print(name, e)
        outputdata1 = pd.DataFrame(pcValues, columns=['pc'])
        outputdata2 = pd.DataFrame(mbValues, columns=['mb'])
        outputdata1.to_csv(outputPc)
        outputdata2.to_csv(outputMb)
        exit()

    outputdata1 = pd.DataFrame(pcValues, columns=['pc'])
    outputdata2 = pd.DataFrame(mbValues, columns=['mb'])
    outputdata1.to_csv(outputPc)
    outputdata2.to_csv(outputMb)
