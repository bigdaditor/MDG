from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

def setup():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    )
    service = Service('./driver/chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def search(keyword):
    driver = setup()
    driver.get('https://www.coupang.com')

    try:
        # 팝업 닫기 (존재하는 경우)
        try:
            close_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "close"))
            )
            close_button.click()
        except:
            pass

        # 검색어 입력
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.RETURN)

        # 검색 결과 로딩 대기
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "search-product"))
        )

        # 스크롤 다운 (더 많은 결과 로딩)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        products = driver.find_elements(By.CLASS_NAME, "search-product")

        results = []
        for product in products[:10]:  # 상위 10개 제품만 처리
            try:
                item = {}
                item['name'] = product.find_element(By.CLASS_NAME, "name").text
                price = product.find_element(By.CLASS_NAME, "price-value").text
                price = int(price.replace(',', ''))
                item['price'] = price
                results.append(item)

            except:
                continue

        return results
    except TimeoutException:
        print("페이지 로딩 시간이 초과되었습니다. 네트워크 연결을 확인하거나 나중에 다시 시도해주세요.")
        return []
    except Exception as e:
        print(f"크롤링 중 오류가 발생했습니다: {str(e)}")
        return []
    finally:
        driver.quit()