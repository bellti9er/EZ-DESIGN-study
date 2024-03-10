# Week 3

iterator 패턴에 대해 공부합니다.

</br>

## Lecture

- [iterator](https://refactoring.guru/design-patterns/iterator)

### Iterator

- `iterator`는 여러 데이터 집합에 순차적으로 접근할 떄, 그 데이터가 어떻게 구성되어 있는지(ex. 배열, 리스트, 트리 등) 고려하지 않고 순회할 수 있게 해주는 행동 디자인 패턴
  - 해당 패턴은 데이터를 순회하는 행동을 별도의 이터레이터 객체로 추출하여, 데이터 구조가 복잡해도 클라이언트 코드가 간단한 방법으로 요소에 접근할 수 있게 해줌
  - 모든 이터레이터는 동일한 인터페이스를 구현해야 하며, 그로 인해 개발자가 내부 구조를 몰라도 간단하게 데이터를 하나씩 처리할 수 있게 해줌

</br>

## Assignment

무신사, wconcept Crawler를 구현합니다.

- Crawler는 패션 플랫폼 특정 카테고리 상품 목록 페이지를 돌며 아래와 같은 부분(item box)의 html 태그를 파싱하여 name, brand, price를 수집합니다.
  ![image](https://github.com/bellti9er/bellti9er/assets/132914700/542e27bb-925f-4cbc-9ddc-c650d6ba1666)

  - 기본적으로 Crawler는 category(001001 등)를 인자로 받고 base url로부터 상품 목록 url을 구성해 1페이지부터 시작합니다. example urls의 query params를 유심히 살펴보세요.
    - example urls
      - https://www.musinsa.com/categories/item/003004?d_cat_cd=003004&brand=&list_kind=small&sort=pop_category&sub_sort=&page=3&display_cnt=90&group_sale=&exclusive_yn=&sale_goods=&timesale_yn=&ex_soldout=&plusDeliveryYn=&kids=&color=&price1=&price2=&shoeSizeOption=&tags=&campaign_id=&includeKeywords=&measure=
      - https://display.wconcept.co.kr/category/women/001001?page=2
  - Crawler는 iterator 패턴을 포함하고 있습니다.

    - 페이지를 돌 때마다 페이지 안의 상품 정보들을 파싱하고, 다음 페이지로 넘어가고 나서 상품이 하나도 없으면 iterate를 종료합니다.
    - FacebookIterator를 사용하는 곳에서는 getNext를 호출하면 Profile을 받을 수 있는 것처럼 iterator를 사용하는 곳에서는 상품 정보를 포함하는 html 태그(item box)만을 받을 수 있습니다.
      ![image](https://github.com/bellti9er/bellti9er/assets/132914700/be4a7427-85ad-4f51-9d89-221b43b20d2d)
    - iterate해서 나오는 html 태그를 활용하여 각각 name, brand, price를 파싱해서 csv로 저장합니다.

      - musinsa selectors

        ```python
        item_box_selector="#searchList > li.li_box",
        name_selector="div.li_inner > div.article_info > p.list_info > a",
        brand_selector="div.li_inner > div.article_info > p.item_title > a",
        price_selector="div.li_inner > div.article_info > p.price",
        ```

      - wconcept selectors는 chrome 개발자 도구로 직접 찾아보세요.

    - python에서 iterator 패턴은 굳이 getNext 등의 인터페이스를 따로 구성하지 않더라도 Generator로 쉽게 구현할 수 있습니다. 기회가 된다면 도전해보세요.

- 무신사에서 숏팬츠 1000개, wconcept에서 아우터 100개 정보를 모아보세요.
- selenium, bs4 모듈을 사용합니다.

</br>

## Apply

```python
# musinsa_crawler.py

class MusinsaCrawler:
    def __init__(self, driver: WebDriver, category: str, file_name: str, limit=1000):
        . . .

    def generate_items(self) -> Generator[Any, Any, Any]:
        collected: int = 0
        page: int = 1

        while collected < self.limit:
            self.driver.get(self.base_url.format(category=self.category, page=page))

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "#searchList > li.li_box")
                )
            )

            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            items = soup.select("#searchList > li.li_box")

            if not items:
                break

            for item in items:
                name = item.select_one(
                    "div.li_inner > div.article_info > p.list_info > a"
                ).text.strip()
                brand = item.select_one(
                    "div.li_inner > div.article_info > p.item_title > a"
                ).text.strip()
                price = item.select_one(
                    "div.li_inner > div.article_info > p.price"
                ).text.strip()

                yield name, brand, price

                collected += 1

                if collected >= self.limit:
                    return

            page += 1
```

```python
# run_crawler.py

if __name__ == "__main__":
    site_name_musinsa = "musinsa"
    category_musinsa = "003009"
    file_name_musinsa = "musinsa_short_pants.csv"

    . . .

    musinsa_crawler = CrawlerFactory.get_crawler(
        site_name_musinsa, category_musinsa, file_name_musinsa
    )

    with open(file_name_musinsa, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Brand", "Price"])

        for name, brand, price in musinsa_crawler.generate_items():
            writer.writerow([name, brand, price])

    . . .

```

- `OOO_crawler.py` 와 `run_crawler.py` 를 통해 이터레이터 패턴을 부분 적용
- `OOOCrawler` 클래스의 `generate_items` 메소드는 웹 페이지의 HTML 구조나 BeautifulSoup 을 사용하는 방식 등 컬렉션의 내부 구조에 대한 세부 사항을 클라이언트 코드로부터 숨김
  - 클라이언트는 코드는 단지 메소드를 호출하여 각 상품의 정보를 순처적으로 얻을 수 있음
- 클라이언트 코드(`run_crawler.py`)는 컬렉션의 순회 방식에 대해 고려하거나 걱정할 필요가 없게 만듦
  - 상품 목록의 순회 방식을 변경하거나 특정 필터 기능을 적용하고 싶을떄 컬렉션을 사용하는 클라이언트 코드는 변경할 필요가 없음
- 상품 정보의 수집과 csv 파일로의 저장을 분리하여 각각의 책임을 명확히 함

</br>

## Tests

### Musinsa CSV

![image](https://github.com/bellti9er/bellti9er/assets/132914700/3aafc09e-64cc-4d10-929b-f60f4dc014f1)

</br>

### Wconcept CSV

> Failed

![image](https://github.com/bellti9er/bellti9er/assets/132914700/379248f2-9550-4091-93e3-088aa8de0bd7)

</br>
