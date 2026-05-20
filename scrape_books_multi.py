import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE_URL = "http://books.toscrape.com/catalogue/page-{}.html"
all_books = []

for page_num in range(1, 6):
    url = BASE_URL.format(page_num)
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, "lxml")

    for article in soup.find_all("article", class_="product_pod"):
        title = article.h3.a["title"]
        price = article.find("p", class_="price_color").text
        rating = article.p["class"][1]

        all_books.append(
            {
                "title": title,
                "price": price,
                "rating": rating,
            }
        )

    print(f"ページ {page_num} 完了: 累計 {len(all_books)} 件")
    time.sleep(1)

df = pd.DataFrame(all_books)
df.to_csv("books.csv", index=False)  # index=False 行番号を消す
# CSV: カンマで区切られたデータが行単位で並ぶ形式
print(f"\n合計 {len(df)} 件を books.csv に保存しました")
