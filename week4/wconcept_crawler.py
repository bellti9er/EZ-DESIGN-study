import csv

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

    def crawl(self) -> None:
        collected: int = 0
        page: int = 1

        with open(self.file_name, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Brand", "Price"])

            while collected < self.limit:
                self.driver.get(self.base_url.format(category=self.category, page=page))

                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "div.product-list.type-list > div")
                    )
                )

                soup = BeautifulSoup(self.driver.page_source, "html.parser")
                items = soup.select("div.product-list.type-list > div")

                # Wconcept selectors 확인 필요
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
                    writer.writerow([name, brand, price])
                    collected += 1
                    if collected >= self.limit:
                        break
                page += 1

            self.driver.quit()
