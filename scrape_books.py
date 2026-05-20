# 静的なWebページ用
import requests # HTMLを取得
from bs4 import BeautifulSoup # 必要な・特定の情報を取得
import pandas as pd

# 1. ページ取得
url = "http://books.toscrape.com/"
response = requests.get(url)

print(f"ステータスコード: {response.status_code}") # 200なら成功
response.encoding = response.apparent_encoding # 文字化け防止
print(f"文字コード: {response.encoding}")

# よくあるエラー
# status_code: 403 アクセス拒否 → User-Agent ヘッダーをつける

# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
# }
# response = requests.get(url, headers=headers)
#
# 文字化け 文字コードのズレ → response.encoding = "utf-8" を明示

# 2. HTMLをパース
# コンピュータが理解しやすいようにHTMLのテキストデータを解析し、
# 構造化されたデータに変換すること
soup = BeautifulSoup(response.text, "lxml")
#print(soup)
# 3. 本のデータを取得
books = []

# 取りたい要素（本のタイトルなど）の上で 右クリック → 「検証」/調査
for article in soup.find_all("article", class_="product_pod"):
    title = article.h3.a["title"]
    price = article.find("p", class_ = "price_color").text
    rating = article.p["class"][1]
    availability = article.find("p", class_ = "instock availability").text.strip() # .strip()は\nとわける
    if availability == "In stock":
        availability = "O"
    else:
        availability = "X"

    books.append({
        "title": title,
        "price": price,
        "rating": rating,
        "availability": availability,
    })

# 4. DataFrameにして表示
# Pandasの「DataFrame型」は、
# 表形式のデータ（行と列で構成されるデータ）を扱うための基本的なデータ構造
# PythonでExcelのような表データを扱いたいときに便利
df = pd.DataFrame(books)
print(df)
print(f"\n取得件数: {len(df)}件")