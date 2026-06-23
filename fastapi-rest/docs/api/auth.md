# 認証

この API では、ログインしたユーザーに対して Bearer トークンを発行し、以後の認証が必要な API で利用します。

## 事前条件

- ログイン用の `email` と `password` が必要です。
- 認証が必要な API には `Authorization: Bearer <token>` を付与します。

## ログイン

`POST /api/v1/auth/login`

### リクエスト例

```json
{
	"email": "yamada@example.com",
	"password": "password123"
}
```

### レスポンス例

```json
{
	"accessToken": "eyJhbGciOi...",
	"tokenType": "Bearer",
	"expiresIn": 3600,
	"user": {
		"id": "550e8400-e29b-41d4-a716-446655440000",
		"name": "山田 太郎",
		"email": "yamada@example.com",
		"role": "admin"
	}
}
```

### エラー例

- `400 Bad Request`: 入力値が不足している
- `401 Unauthorized`: 認証に失敗した
- `503 Internal Server Error`: 想定外のエラー

## ログアウト

`POST /api/v1/auth/logout`

### 説明

- 現在のトークンを無効化します。
- クライアントは以後そのトークンを再利用しません。

### レスポンス例

```json
{
	"message": "Logged out"
}
```

### エラー例

- `401 Unauthorized`: トークンが指定されていない（`Authorization` ヘッダーがない）
- `401 Unauthorized`: トークンが不正、または期限切れ

## 認証が必要な API

- 書籍の一覧、登録、詳細、更新、削除
- ユーザーの一覧、登録、詳細、更新、削除
- ログアウト
