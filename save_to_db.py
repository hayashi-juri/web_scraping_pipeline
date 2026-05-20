import sqlite3
import pandas as pd

# CSVの読み込み
df = pd.read_csv("books.csv")

# 価格の￡を除いてfloatに変換(DBに数値として保存するため)
df["price"] = df["price"].str.replace("£", "").astype(float)

print(df.dtypes) # 型を確認
print(df.head(3))

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

print("保存完了")

# 確認：SQLで読み直す
result = pd.read_sql("SELECT * FROM books LIMIT 5", conn)
print(result)

conn.close() # これを忘れるとDBファイルがロックされたままになる

# # close()を自動でやってくれる
# with sqlite3.connect("books.db") as conn:
#     df.to_sql("books", con=conn, if_exists="replace", index=False)
# # ← withブロックを出ると自動でclose()

conn = sqlite3.connect("books.db")
cursor = conn.cursor() # 実際にSQLを実行する「窓口」

# 評価がThreeの本を価格の高い順に表示
cursor.execute("""
    SELECT title, price, rating
    FROM books
    WHERE rating = "Three"
    ORDER BY price DESC
    LIMIT 5
"""
)

rows = cursor.fetchall() # execute() で検索した結果を全部まとめて取ってくる
for row in rows:
    print(row)

conn.close()