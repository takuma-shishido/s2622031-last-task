import re
import sqlite3
import time

import requests
from bs4 import BeautifulSoup

URL = "https://github.com/orgs/google/repositories"

conn = sqlite3.connect("github_google.db")
conn.execute("CREATE TABLE IF NOT EXISTS repositories (name TEXT PRIMARY KEY, language TEXT, stars TEXT)")

page = 1
while True:
    res = requests.get(URL, params={"page": page})
    # アクセスしすぎで 429 が返ったら待ってやり直す
    if res.status_code == 429:
        time.sleep(int(res.headers.get("Retry-After", 60)))
        continue
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "html.parser")
    # フッターにも h3 があるので、リポジトリ一覧の li 内の h3 だけを使う
    titles = [h3 for h3 in soup.find_all("h3") if h3.find_parent("li")]
    if not titles:
        break
    for h3 in titles:
        li = h3.find_parent("li")
        name = h3.find("a").text
        lang = li.find("span", class_=re.compile("PrimaryLanguageName"))
        stars = li.find("a", href=re.compile("/stargazers$")).text
        conn.execute("INSERT OR REPLACE INTO repositories VALUES (?, ?, ?)", (name, lang.text if lang else None, stars))
    conn.commit()
    page += 1
    time.sleep(1)

for row in conn.execute("SELECT * FROM repositories"):
    print(row)

conn.close()
