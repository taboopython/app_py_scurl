import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
import chardet

# ファイルのパスを環境変数から取得
csv_path = os.getenv('CSV_PATH', 'sclist.csv')

# ファイルのエンコーディングを検出
with open(csv_path, 'rb') as f:
    result = chardet.detect(f.read())

# 検出されたエンコーディングで CSV ファイルを読み込む
df = pd.read_csv(csv_path, encoding=result['encoding'])

# URLを保存するための空のリストを作成
urls = []

# User-Agentヘッダー
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
}

# 各ショッピングセンターについて
for center in df['center']:
    # Google検索のURLを作成
    url = f"https://www.google.com/search?q={center}"

    # Google検索の結果ページを取得
    response = requests.get(url, headers=headers)

    # HTMLを解析
    soup = BeautifulSoup(response.text, 'html.parser')

    # 最初の検索結果のURLを取得
    div = soup.find('div', class_='kCrYT')
    if div is not None:
        a = div.find('a')
        if a is not None:
            result = a.get('href')
            if result is not None:
                urls.append(result)
            else:
                urls.append("No href found")
        else:
            urls.append("No a tag found")
    else:
        urls.append("No div found")

    # Googleのポリシーに違反しないように、少し待つ
    time.sleep(1)

# URLのリストをCSVファイルに保存
df['url'] = urls
df.to_csv('/app/data/shopping_centers_with_urls.csv', encoding='utf-8', index=False)
