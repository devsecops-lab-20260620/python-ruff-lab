# Bookshelf API 概要

家庭内の書籍を管理するための REST API 仕様をまとめます。対象は、書籍情報の登録・閲覧・更新・削除、管理するユーザーの登録・閲覧・更新・削除、ユーザーのログイン・ログアウト、ヘルスチェックです。

## 基本方針

- API は JSON をやり取りします。
- ベースパスは `/api/v1` とします。
- 認証が必要な API は `Authorization: Bearer <token>` を要求します。
- 成功時は用途に応じて `200 OK`、`201 Created`、`204 No Content` を返します。
- 失敗時は共通エラー形式を返します。

## 対象リソース

### 書籍

家庭で管理する書籍の情報です。想定する主な属性は次のとおりです。

- `id`
- `title`
- `author`
- `isbn`（ISBN-13。例: `978-4-7819-1628-6`）
- `publisher`
- `publishedYear`
- `status`
- `createdAt`
- `updatedAt`

### ユーザー

書籍を管理するユーザーの情報です。想定する主な属性は次のとおりです。

- `id`
- `name`
- `email`
- `role`
- `createdAt`
- `updatedAt`

#### role の値

`role` には以下の値があります。

- `admin` - 管理者。全ての機能にアクセス可能
- `user` - 一般ユーザー。基本機能にアクセス可能
- `guest` - ゲストユーザー。限定的な機能のみアクセス可能

### 認証

ログインはユーザーの認証情報を受け取り、以後の API 呼び出しで使うトークンを返します。ログアウトは現在の認証状態を終了します。

### ヘルスチェック

サービスが稼働しているかを確認する軽量なエンドポイントです。

## 共通レスポンスの考え方

- 取得系は単体オブジェクトまたは配列を返します。
- 一覧系はページング情報を返します。
- 作成系は作成したリソースを返します。
- 削除系は本文なしで返すことがあります。

## 想定ステータスコード

- `200 OK`
- `201 Created`
- `204 No Content`
- `400 Bad Request`
- `401 Unauthorized`
- `403 Forbidden`
- `404 Not Found`
- `409 Conflict`
- `500 Internal Server Error`

## エンドポイント一覧

詳細は各ファイルを参照してください。

- `docs/api/endpoints.md`
- `docs/api/auth.md`
- `docs/api/error-handling.md`
- `docs/api/versioning.md`
