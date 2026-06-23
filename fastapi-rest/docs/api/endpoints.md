# エンドポイント一覧

この API は家庭内の書籍管理を対象にした REST 仕様です。ここでは主要エンドポイントを一覧で示します。

## ヘルスチェック

| Method | Path | 認証 | 概要 |
| --- | --- | --- | --- |
| GET | /health | 不要 | サービス稼働確認 |

## 認証

| Method | Path | 認証 | 概要 |
| --- | --- | --- | --- |
| POST | /api/v1/auth/login | 不要 | ログインしてトークンを取得 |
| POST | /api/v1/auth/logout | 必要 | 現在のログイン状態を終了 |

## 書籍

| Method | Path | 認証 | 概要 |
| --- | --- | --- | --- |
| GET | /api/v1/books | 必要 | 書籍一覧を取得 |
| POST | /api/v1/books | 必要 | 書籍を登録 |
| GET | /api/v1/books/{bookId} | 必要 | 書籍の詳細を取得 |
| PATCH | /api/v1/books/{bookId} | 必要 | 書籍情報を更新 |
| DELETE | /api/v1/books/{bookId} | 必要 | 書籍を削除 |

### 書籍一覧の主なクエリパラメータ

| パラメータ | 説明 |
| --- | --- |
| page | ページ番号 |
| limit | 1ページあたり件数 |
| keyword | タイトル、著者、ISBN-13 のあいまい検索 |
| ownerUserId | 所有者で絞り込み |
| status | 状態で絞り込み |

## ユーザー

| Method | Path | 認証 | 概要 |
| --- | --- | --- | --- |
| GET | /api/v1/users | 必要 | ユーザー一覧を取得 |
| POST | /api/v1/users | 必要 | ユーザーを登録 |
| GET | /api/v1/users/{userId} | 必要 | ユーザーの詳細を取得 |
| PATCH | /api/v1/users/{userId} | 必要 | ユーザー情報を更新 |
| DELETE | /api/v1/users/{userId} | 必要 | ユーザーを削除 |

### ユーザー一覧の主なクエリパラメータ

| パラメータ | 説明 |
| --- | --- |
| page | ページ番号 |
| limit | 1ページあたり件数 |
| keyword | 名前、メールアドレスでの検索 |
| role | 役割で絞り込み |

## リソースの更新ルール

- `POST` は新規作成に使います。
- `PATCH` は部分更新に使います。
- `DELETE` は対象を完全に削除します。
- `GET` は副作用を持ちません。

