import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def get_places_details(place_name, max_results=50):
    """카카오 지도에서 여러 페이지를 이동하면서 최대 max_results개 장소 크롤링"""

    # Chrome WebDriver 설정
    options = Options()
    # options.add_argument("--headless")  # ⚠️ 주석 처리 (브라우저 띄워서 확인할 것)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=3")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # 카카오 지도에서 장소 검색
        search_url = f"https://map.kakao.com/?q={place_name}"
        print(f"🔍 '{place_name}' 검색 중... ({search_url})")
        driver.get(search_url)

        # 검색 결과가 나올 때까지 최대 10초 대기
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'li.PlaceItem'))
            )
        except Exception:
            print("❌ 검색 결과를 찾을 수 없습니다. HTML 구조를 다시 확인하세요.")
            return None

        results = []
        page = 1  # 현재 페이지 번호

        while len(results) < max_results:
            print(f"📄 페이지 {page}에서 크롤링 중...")

            # 현재 페이지에서 장소 목록 가져오기
            places = driver.find_elements(By.CSS_SELECTOR, 'li.PlaceItem')

            for place in places:
                if len(results) >= max_results:  # 최대 개수 초과하면 중단
                    break

                try:
                    place_name = place.find_element(By.CSS_SELECTOR, 'a.link_name').text
                    rating = place.find_element(By.CSS_SELECTOR, 'em.num').text
                    review_count = place.find_element(By.CSS_SELECTOR, 'a.review em').text

                    results.append({
                        "name": place_name,
                        "rating": rating,
                        "review_count": review_count
                    })

                    print(f"   🏠 {len(results)}. {place_name} - ⭐ {rating} | 💬 {review_count}")

                except Exception as e:
                    print("⚠️ 장소 정보를 가져오는 데 실패:", e)

            # 다음 페이지 버튼 클릭 (번호 증가)
            page += 1
            try:
                next_page_button = driver.find_element(By.CSS_SELECTOR, f'a#info\\.search\\.page\\.no{page}')
                driver.execute_script("arguments[0].click();", next_page_button)  # JavaScript로 클릭
                time.sleep(3)  # 페이지 로딩 대기
            except:
                print("🚫 다음 페이지가 없습니다. 크롤링 종료.")
                break

        return results

    except Exception as e:
        print("❌ 크롤링 실패:", e)
        return None

    finally:
        driver.quit()  # WebDriver 종료

# 🔹 테스트 실행
if __name__ == "__main__":
    place_name = "부산 맛집"
    results = get_places_details(place_name, max_results=50)

    if results:
        print("\n✅ 최종 크롤링된 장소 목록:")
        for idx, place in enumerate(results, start=1):
            print(f"{idx}. {place['name']} - ⭐ {place['rating']} | 💬 {place['review_count']}")
