from crawler_factory import CrawlerFactory

if __name__ == "__main__":
    site_name_musinsa = "musinsa"
    category_musinsa = "003009"
    file_name_musinsa = "musinsa_short_pants.csv"

    site_name_wconcept = "wconcept"
    category_wconcept = "001001"
    file_name_wconcept = "wconcept_outer.csv"

    musinsa_crawler = CrawlerFactory.get_crawler(
        site_name_musinsa, category_musinsa, file_name_musinsa
    )
    musinsa_crawler.crawl()

    # wconcept_crawler = CrawlerFactory.get_crawler(
    #     site_name_wconcept, category_wconcept, file_name_wconcept
    # )
    # wconcept_crawler.crawl()
