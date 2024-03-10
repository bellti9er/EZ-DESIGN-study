from typing import Generator, Any

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


class WconceptCrawler:
    def __init__(self, driver: WebDriver, category: str, file_name: str, limit=1000):
        self.driver: WebDriver = driver
        self.category: str = category
        self.file_name: str = file_name
        self.limit: int = limit
        self.base_url: str = (
            "https://display.wconcept.co.kr/category/{category}?page={page}"
        )

    def generate_items(self) -> Generator[Any, Any, Any]:
        collected: int = 0
        page: int = 1

        while collected < self.limit:
            self.driver.get(self.base_url.format(category=self.category, page=page))

            # 동적인 웹사이트에서는 JS를 통해 비동기적으로 콘텐츠가 로드되므로, selenium이 페이지의 특정 요소에 접근할 수 있을 때까지 기다려야 함
            # https://mebadong.tistory.com/100
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div.product-list.type-list > div")
                )
            )

            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            items = soup.select("div.product-list.type-list > div")

            if not items:
                break

            for item in items:
                name = item.select_one(
                    "span.prdc-title > span.text.detail"
                ).text.strip()
                brand = item.select_one(
                    "span.prdc-title > span.text.title"
                ).text.strip()
                price = item.select_one(
                    "span.prdc-price > span.text.final-price > strong"
                ).text.strip()

                yield name, brand, price

                collected += 1

                if collected >= self.limit:
                    return

            page += 1
