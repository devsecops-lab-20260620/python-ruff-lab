# PostgreSQL 準備手順（既存 PostgreSQL 利用）

この手順は、**PostgreSQL サーバー自体はすでに存在している**前提で、`fastapi-rest` から接続できる状態にするための準備をまとめています。

## 1. 事前確認

- PostgreSQL の接続情報を確認
  - ホスト名または IP
  - ポート（通常 `5432`）
  - 管理ユーザー名
  - 管理ユーザーのパスワード
- `fastapi-rest` を動かすサーバーから PostgreSQL へ到達できること

## 2. アプリ用 DB / ユーザーを作成

`postgres` ユーザーで接続して、アプリ専用の DB とユーザーを作成します。

```bash
psql -h <POSTGRES_HOST> -p 5432 -U postgres -d postgres
```

```sql
CREATE DATABASE bookshelf;
CREATE USER bookshelf_user WITH PASSWORD 'change-me-strong-password';
GRANT ALL PRIVILEGES ON DATABASE bookshelf TO bookshelf_user;
```

> 既存の命名ルールがある場合は、`bookshelf` / `bookshelf_user` を読み替えてください。

## 3. 権限を追加（接続先 DB 内）

アプリがテーブル作成・更新できるよう、スキーマ権限を付与します。

```bash
psql -h <POSTGRES_HOST> -p 5432 -U postgres -d bookshelf
```

```sql
GRANT USAGE, CREATE ON SCHEMA public TO bookshelf_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO bookshelf_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT USAGE, SELECT, UPDATE ON SEQUENCES TO bookshelf_user;
```

## 4. `pg_hba.conf` / `postgresql.conf` の確認

DB サーバー側の設定で、アプリサーバーからの接続を許可します。

- `pg_hba.conf`: 接続元 IP と認証方式（`scram-sha-256` など）を許可
- `postgresql.conf`: `listen_addresses` が適切に設定されていること

設定変更後、PostgreSQL をリロードまたは再起動します（環境に合わせて実施）。

## 5. FastAPI 側の `.env` 設定

`fastapi-rest` のルートで `.env` を作成し、`DATABASE_URL` を PostgreSQL 用に設定します。

```bash
cp .env.example .env
```

`.env` 例:

```dotenv
DATABASE_URL=postgresql+psycopg://bookshelf_user:change-me-strong-password@<POSTGRES_HOST>:5432/bookshelf
JWT_SECRET=replace-with-a-secure-random-string
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_SECONDS=3600
APP_NAME=bookshelf-api
APP_VERSION=1.0.0
```

## 6. Python 依存関係をインストール

PostgreSQL 接続には `psycopg` が必要です。

```bash
python -m pip install -r requirements.txt
python -m pip install "psycopg[binary]"
```

## 7. 接続確認

まず PostgreSQL へ直接接続できることを確認します。

```bash
psql -h <POSTGRES_HOST> -p 5432 -U bookshelf_user -d bookshelf -c "SELECT version();"
```

次に FastAPI を起動してヘルスチェックを確認します。

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --app-dir src
curl http://127.0.0.1:8000/health
```

## 8. よくあるエラー

- `password authentication failed`
  - ユーザー名・パスワード、`pg_hba.conf` の認証方式を確認
- `no pg_hba.conf entry`
  - 接続元 IP の許可設定を追加
- `connection refused`
  - DB ポート開放、`listen_addresses`、ネットワーク経路を確認
- `permission denied for schema public`
  - スキーマ権限 (`USAGE`, `CREATE`) を再確認

