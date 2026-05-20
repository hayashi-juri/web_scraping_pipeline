import sqlite3
import pandas as pd

# CSVの読み込み
df = pd.read_csv("books.csv")

# 価格の￡を除いてfloatに変換(DBに数値として保存するため)
df["price"] = df["price"].str.replace("£", "").astype(float)

# DB接続(存在しない場合は新規作成)
# conn/con: データベースへの「接続口」(connectionの略)
conn = sqlite3.connect("books.db")

# DataFrameをそのままテーブルに書き込む
df.to_sql(
    name = "books",
    con = conn,
    if_exists = "replace",
    index = False
)

cursor = conn.cursor() # 実際にSQLを実行する「窓口」

# # 評価がThreeの本を価格の高い順に表示
# cursor.execute("""
#     SELECT rating, AVG(price), COUNT(*)
#     FROM books
#     GROUP BY rating
#     ORDER BY AVG(price) DESC;
# """
# )

# rows = cursor.fetchall() # execute() で検索した結果を全部まとめて取ってくる
# for row in rows:
#     print(row)

# conn.close()

# 価格が40ポンド以上の本を、価格の安い順に表示してください。
# タイトルと価格だけ表示すること。
cursor.execute("""
    SELECT title, price
    FROM books
    WHERE price > 40
    ORDER BY price ASC;
"""
)

# 評価（rating）ごとに、本の冊数と平均価格を出してください。
# 平均価格の高い順に並べること。

cursor.execute("""
    SELECT rating, COUNT(*), AVG(price)
    FROM books
    GROUP BY rating
    ORDER BY AVG(price) DESC
""")

# 評価が Four または Five で、
# かつ価格が50ポンド未満の本のタイトル・価格・評価を表示してください。
cursor.execute("""
    SELECT title, rating, price
    FROM books
    WHERE (rating = 'Five' OR rating = 'FOUR') AND (price < 50)
"""
)

rows = cursor.fetchall() # execute() で検索した結果を全部まとめて取ってくる
for row in rows:
    print(row)

conn.close()
