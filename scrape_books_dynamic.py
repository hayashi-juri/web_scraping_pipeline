from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True) # headless=Falseにするとブラウザが目に見えて動く
    page = browser.new_page()

    page = browser.new_page()

    page.goto("http://books.toscrape.com/")

    # JS描画が終わるまで待つ
    page.wait_for_selector("article.product_pod")

    # 描画後のHTMLをBeautifulSoupに渡す
    html = page.content()
    soup = BeautifulSoup(html, "lxml")

    # あとはBeautifulSoupと同じ
    books = []
    for article in soup.find_all("article", class_="product_pod"):
        title = article.h3.a["title"]
        price = article.find("p", class_="price_color").text
        books.append({"title": title, "price": price})
    
    browser.close()

df = pd.DataFrame(books)
print(df)