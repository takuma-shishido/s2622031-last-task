# github-google-scraper

GitHub の [Google organization](https://github.com/orgs/google/repositories) が管理しているリポジトリを全件スクレイピングし、
以下の情報を SQLite (`github_google.db`) に保存して `SELECT` で表示します。

- リポジトリ名
- 主要な言語
- スターの数（GitHub の表示どおり。例: `9k`, `2.6k`, `308`）

GitHub API は使わず、HTML を `requests` + `BeautifulSoup` で解析しています。
各ページの取得後に `time.sleep(1)` を入れています。

## 実行方法

[uv](https://docs.astral.sh/uv/) が必要です。

```sh
uv sync
uv run main.py
```

## テーブル定義

```sql
CREATE TABLE repositories (
    name     TEXT PRIMARY KEY,  -- リポジトリ名
    language TEXT,              -- 主要な言語（無い場合は NULL）
    stars    TEXT               -- スター数
);
```
