# fastapi-rest

書籍管理システム向けの FastAPI ベース REST API サーバーです。

## 実装済み機能

- ヘルスチェック: `GET /health`
- 認証: `POST /api/v1/auth/login`, `POST /api/v1/auth/logout`
- 書籍 CRUD: `GET/POST /api/v1/books`, `GET/PATCH/DELETE /api/v1/books/{bookId}`
- ユーザー CRUD: `GET/POST /api/v1/users`, `GET/PATCH/DELETE /api/v1/users/{userId}`
- 共通エラー形式（`error.code`, `error.message`, `error.details`）

## ディレクトリ

- `src/main.py`: FastAPI エントリポイント
- `src/app/models.py`: SQLAlchemy モデル
- `src/app/routers/`: API ルーター
- `tests/test_api.py`: API の基本動作テスト

## 前提条件

- Python 3.11+
- PostgreSQL（本番想定）
  - ローカル簡易実行は SQLite をデフォルト利用

## Linux 上で直に実行する方法

1. プロジェクトディレクトリへ移動
2. 依存関係をインストール
3. `.env.example` を `.env` にコピーして必要に応じて編集
4. アプリを起動

```bash
cd /path/to/python-ruff-lab/fastapi-rest
python -m pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --host 0.0.0.0 --port 8000 --app-dir src --reload
```

### Linux でのテスト実行

```bash
cd /path/to/python-ruff-lab/fastapi-rest
python -m pytest -q
```

## 初期ログインユーザー

起動時に以下の管理者ユーザーを自動作成します（存在しない場合のみ）。

- email: `admin@example.com`
- password: `password123`

## コンテナで実行する方法

1. `.env.example` を `.env` にコピーして必要に応じて編集
2. イメージをビルド
3. コンテナを起動

```bash
cd /path/to/python-ruff-lab/fastapi-rest
cp .env.example .env
docker build -t fastapi-rest .
docker run --rm -p 8000:8000 --env-file .env fastapi-rest
```
