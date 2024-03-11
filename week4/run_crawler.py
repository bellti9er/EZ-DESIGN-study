import csv

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

    with open(file_name_musinsa, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Brand", "Price"])

        for name, brand, price in musinsa_crawler.generate_items():
            writer.writerow([name, brand, price])

    wconcept_crawler = CrawlerFactory.get_crawler(
        site_name_wconcept, category_wconcept, file_name_wconcept
    )

    with open(file_name_wconcept, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Brand", "Price"])

        for name, brand, price in wconcept_crawler.generate_items():
            writer.writerow([name, brand, price])
