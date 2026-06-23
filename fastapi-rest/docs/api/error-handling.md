# エラーハンドリング

API は失敗時に共通のエラー形式を返します。クライアントはステータスコードと `code` を基準に処理します。

## エラー形式

```json
{
	"error": {
		"code": "VALIDATION_ERROR",
		"message": "入力値を確認してください",
		"details": [
			{
				"field": "title",
				"message": "title は必須です"
			}
		]
	}
}
```

## 主なエラーコード

| HTTP ステータス | code | 説明 |
|------------| --- | --- |
| 400        | VALIDATION_ERROR | 入力値の検証に失敗した |
| 401        | UNAUTHORIZED | 認証がない、または無効 |
| 403        | FORBIDDEN | 権限がない |
| 404        | NOT_FOUND | 対象が見つからない |
| 409        | CONFLICT | 重複や状態競合がある |
| 500        | INTERNAL_SERVER_ERROR | 想定外のエラー |
| 503        | SERVICE_UNAVAILABLE | サービス利用不可 |

## バリデーション例

- 書籍登録で `title` が空
- ユーザー登録で `email` が重複
- ログインで `password` が不足

## エラー応答の運用ルール

- `message` は人間が読める短い説明にします。
- `details` は必要な場合のみ返します。
- 内部実装の詳細やスタックトレースは返しません。

