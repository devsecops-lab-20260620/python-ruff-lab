# curl でのログイン方法

`fastapi-rest` の認証エンドポイントを curl で操作する手順をまとめます。

## 前提

- API サーバーが `http://127.0.0.1:8000` で起動していること
- 初期管理者アカウントが存在していること（サーバー起動時に自動作成）

---

## 1. ログイン（アクセストークン取得）

```bash
curl -s -X POST http://127.0.0.1:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "password123"
  }'
```

### レスポンス例

```json
{
    "accessToken": "<JWT_TOKEN>",
    "tokenType": "Bearer",
    "expiresIn": 3600,
    "user": {
        "id": "a0252324-8669-443a-8f8e-d82c27d38daa",
        "name": "System Admin",
        "email": "admin@example.com",
        "role": "admin",
        "createdAt": "2026-06-23T10:48:00.145925Z",
        "updatedAt": "2026-06-23T10:48:00.145931Z"
    }
}
```

---

## 2. トークンをシェル変数に保存（便利なワンライナー）

以降のリクエストで使い回せるよう、`TOKEN` 変数に自動保存します。

```bash
TOKEN=$(curl -s -X POST http://127.0.0.1:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"password123"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['accessToken'])")

echo "TOKEN=$TOKEN"
```

---

## 3. 認証が必要なエンドポイントへのリクエスト

`Authorization: Bearer <TOKEN>` ヘッダーを付与します。

### ユーザー一覧取得

```bash
curl -s http://127.0.0.1:8000/api/v1/users \
  -H "Authorization: Bearer $TOKEN" \
  | python3 -m json.tool
```

### 書籍一覧取得

```bash
curl -s http://127.0.0.1:8000/api/v1/books \
  -H "Authorization: Bearer $TOKEN" \
  | python3 -m json.tool
```

---

## 4. ログアウト

```bash
curl -s -X POST http://127.0.0.1:8000/api/v1/auth/logout \
  -H "Authorization: Bearer $TOKEN"
```

---

## 5. 初期ログインユーザー

| email | password | role |
|---|---|---|
| `admin@example.com` | `password123` | admin |

---

## 6. よくあるエラー

| HTTP ステータス | 原因 | 対処 |
|---|---|---|
| `401 Unauthorized` | トークンなし・期限切れ | 再ログインして `TOKEN` を更新 |
| `403 Forbidden` | 権限不足（`user` ロール） | `admin` アカウントでログイン |
| `422 Unprocessable Entity` | リクエストボディの形式が不正 | `email` / `password` フィールドを確認 |

