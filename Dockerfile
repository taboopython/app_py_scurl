# ベースとなるDockerイメージ指定
FROM python:3.8

# 作業ディレクトリを設定
WORKDIR /app

# ホストのファイルを/appにコピー
COPY . /app

# 必要なpythonパッケージのインストール
RUN pip install --no-cache-dir -r requirements.txt

# 環境変数を設定
ENV CSV_PATH=/app/data/sclist.csv

# コマンド実行
CMD ["python", "./src/main.py"]
