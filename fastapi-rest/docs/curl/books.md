# curl での書籍操作方法

書籍の登録・一覧確認・更新・削除を curl で行う手順をまとめます。

## 前提

すべてのエンドポイントに `Authorization: Bearer <TOKEN>` が必要です。  
トークンの取得方法は [login.md](./login.md) を参照してください。

```bash
TOKEN=$(curl -s -X POST http://127.0.0.1:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"password123"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['accessToken'])")
```

---

## 1. 書籍の登録

`POST /api/v1/books`

```bash
curl -s -X POST http://127.0.0.1:8000/api/v1/books \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title": "Python 実践入門",
    "author": "山田 太郎",
    "isbn": "9784297111205",
    "publisher": "技術評論社",
    "publishedYear": 2020,
    "status": "unread"
  }' | python3 -m json.tool
```

### レスポンス例（201 Created）

```json
{
    "id": "f524c978-8157-4f3a-9095-c94955217fb1",
    "title": "Python 実践入門",
    "author": "山田 太郎",
    "isbn": "9784297111205",
    "publisher": "技術評論社",
    "publishedYear": 2020,
    "status": "unread",
    "ownerUserId": null,
    "note": null,
    "createdAt": "2026-06-23T10:57:17.149111Z",
    "updatedAt": "2026-06-23T10:57:17.149117Z"
}
```

### リクエストフィールド

| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| `title` | string | ✅ | 書籍タイトル（1〜255文字） |
| `author` | string | ✅ | 著者名（1〜120文字） |
| `isbn` | string | ✅ | ISBN（10〜32文字） |
| `publisher` | string | | 出版社 |
| `publishedYear` | int | | 出版年（1000〜3000） |
| `status` | string | | `unread` / `reading` / `read`（省略時: `unread`） |
| `ownerUserId` | string | | 所有ユーザーの ID |
| `note` | string | | メモ |

---

## 2. 書籍一覧の確認

`GET /api/v1/books`

```bash
curl -s http://127.0.0.1:8000/api/v1/books \
  -H "Authorization: Bearer $TOKEN" \
  | python3 -m json.tool
```

### クエリパラメータ（任意）

| パラメータ | 説明 | 例 |
|---|---|---|
| `keyword` | タイトル・著者・ISBN で部分一致検索 | `?keyword=Python` |
| `status` | ステータスで絞り込み | `?status=unread` |
| `ownerUserId` | 所有ユーザーで絞り込み | `?ownerUserId=<UUID>` |
| `page` | ページ番号（デフォルト: 1） | `?page=2` |
| `limit` | 1ページあたり件数（デフォルト: 20, 最大: 100） | `?limit=10` |

```bash
# キーワード検索の例
curl -s "http://127.0.0.1:8000/api/v1/books?keyword=Python&status=unread" \
  -H "Authorization: Bearer $TOKEN" \
  | python3 -m json.tool
```

### レスポンス例（200 OK）

```json
{
    "items": [
        {
            "id": "f524c978-8157-4f3a-9095-c94955217fb1",
            "title": "Python 実践入門",
            "author": "山田 太郎",
            "isbn": "9784297111205",
            "publisher": "技術評論社",
            "publishedYear": 2020,
            "status": "unread",
            "ownerUserId": null,
            "note": null,
            "createdAt": "2026-06-23T10:57:17.149111Z",
            "updatedAt": "2026-06-23T10:57:17.149117Z"
        }
    ],
    "total": 1,
    "page": 1,
    "limit": 20
}
```

---

## 3. 書籍の更新

`PATCH /api/v1/books/{bookId}`

変更したいフィールドのみ指定します（指定しないフィールドは変更されません）。

```bash
BOOK_ID="f524c978-8157-4f3a-9095-c94955217fb1"

curl -s -X PATCH http://127.0.0.1:8000/api/v1/books/$BOOK_ID \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "status": "reading",
    "note": "読み始めました"
  }' | python3 -m json.tool
```

### レスポンス例（200 OK）

```json
{
    "id": "f524c978-8157-4f3a-9095-c94955217fb1",
    "title": "Python 実践入門",
    "author": "山田 太郎",
    "isbn": "9784297111205",
    "publisher": "技術評論社",
    "publishedYear": 2020,
    "status": "reading",
    "ownerUserId": null,
    "note": "読み始めました",
    "createdAt": "2026-06-23T10:57:17.149111Z",
    "updatedAt": "2026-06-23T10:57:17.311306Z"
}
```

---

## 4. 書籍の削除

`DELETE /api/v1/books/{bookId}`

```bash
BOOK_ID="f524c978-8157-4f3a-9095-c94955217fb1"

curl -s -o /dev/null -w "%{http_code}\n" \
  -X DELETE http://127.0.0.1:8000/api/v1/books/$BOOK_ID \
  -H "Authorization: Bearer $TOKEN"
```

成功時は `204 No Content` が返ります（レスポンスボディなし）。

---

## 5. よくあるエラー

| HTTP ステータス | code | 原因 | 対処 |
|---|---|---|---|
| `401 Unauthorized` | `UNAUTHORIZED` | トークンなし・期限切れ | 再ログインして `TOKEN` を更新 |
| `404 Not Found` | `NOT_FOUND` | 指定した `bookId` が存在しない | ID を確認して再試行 |
| `409 Conflict` | `CONFLICT` | 同じ ISBN の書籍がすでに存在する | ISBN を確認 |
| `422 Unprocessable Entity` | - | リクエストボディの形式が不正 | 必須フィールドと型を確認 |

