from typing import Union

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from musinsa_crawler import MusinsaCrawler
from wconcept_crawler import WconceptCrawler


class CrawlerFactory:
    @staticmethod
    def get_crawler(
        site_name: str, category: str, file_name: str
    ) -> Union[MusinsaCrawler, WconceptCrawler]:
        # Wconcept 크롤링 불가능...
        # options = Options()
        # options.add_argument(
        #     "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        # )
        # options.add_argument("--disable-blink-features=AutomationControlled")
        # options.add_argument("--headless")

        # webdriver_manager를 통해 ChromeDriver를 설치하고, ChromeDriver를 사용하여 WebDriver 객체를 생성
        # https://www.selenium.dev/selenium/docs/api/py/webdriver_chrome/selenium.webdriver.chrome.service.html
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        if site_name == "musinsa":
            return MusinsaCrawler(driver, category, file_name)
        elif site_name == "wconcept":
            return WconceptCrawler(driver, category, file_name)
        else:
            raise ValueError(f"Unsupported site: {site_name}")
