# パターンA: EC2 で `git clone` しない（PyCharm Deployment/SFTP 同期）

Windows 上の PyCharm から、編集内容を EC2 に自動アップロードして開発する手順です。

このパターンでは、PyCharm の **`SSH Interpreter`** を使う前提です。

## 向いているケース

- 1人または少人数で素早く開発したい
- EC2 側で Git 操作を最小限にしたい
- PyCharm の保存と同時に反映したい

## 1. 前提

- Windows に PyCharm (Professional 推奨)
- AWS EC2 (Rocky Linux) が起動済み
- セキュリティグループで `22/tcp` を許可
- 秘密鍵 (`.pem`) を保持
- EC2 に Python 3.11 以上が利用可能

## 2. EC2 インスタンスタイプ目安

- 最小構成（検証用）: `t3.small`
- 標準構成（開発用）: `t3.medium`
- 余裕あり: `t3.large`

`fastapi-rest` の通常開発なら、`t3.medium` で問題ないケースが多いです。

> 以前に PyCharm で「4コア必要」と表示された場合は、`SSH Interpreter` ではなく `Remote Development` の接続方式を選んでいた可能性があります。パターンAでは、まず `Python Interpreter` の `On SSH` を使う構成を想定しています。

## 3. SSH キー権限（Windows）

```powershell
icacls C:\path\to\your-key.pem /inheritance:r
icacls C:\path\to\your-key.pem /grant:r "$($env:USERNAME):(R)"
```

## 4. 事前疎通確認

```bash
ssh -i C:/path/to/your-key.pem rocky@<EC2_PUBLIC_IP>
```

## 5. PyCharm で SSH Interpreter を作成

1. `File` -> `Settings` -> `Project: ...` -> `Python Interpreter`
2. 歯車アイコン -> `Add...`
3. `On SSH` を選択
4. Host/Port/User/Key を入力
5. Interpreter path を選択（例: `/usr/bin/python3`）

## 6. Deployment (SFTP) を設定

1. `Settings` -> `Build, Execution, Deployment` -> `Deployment`
2. `+` で `SFTP` を追加
3. Connection
   - Host: `<EC2_PUBLIC_IP>`
   - Root path: `/home/rocky/work/fastapi-rest`
   - User: `rocky`
   - Auth: Key pair
4. Mappings
   - Local path: `.../python-ruff-lab/fastapi-rest`
   - Deployment path: `/`
5. `Tools` -> `Deployment` -> `Automatic Upload` を有効化

## 7. EC2 側セットアップ

```bash
cd /home/rocky/work/fastapi-rest
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
cp .env.example .env
```

## 8. 実行

PyCharm の Run Configuration で `uvicorn` を module 実行します。

- Module name: `uvicorn`
- Parameters: `main:app --host 0.0.0.0 --port 8000 --app-dir src --reload`
- Working directory: リモートのプロジェクトルート
- Interpreter: SSH Interpreter

## 9. 補足

- EC2 側で `git clone` は不要です。
- 公開アクセス時は `8000/tcp` の開放範囲を最小化してください。

