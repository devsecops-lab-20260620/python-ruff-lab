# パターンB: EC2 で `git clone` する（EC2 側で Git 運用）

EC2 上にリポジトリをクローンし、EC2 側で `git pull` しながら開発する手順です。

このパターンでも、Python 実行環境としては PyCharm の **`SSH Interpreter`** を使う前提で整理しています。

## 向いているケース

- EC2 側でブランチ切替や pull を行いたい
- チーム運用でサーバー側状態を明示的に管理したい
- 本番運用に近いフローで開発したい

## 1. 前提

- Windows に PyCharm (Professional 推奨)
- AWS EC2 (Rocky Linux) が起動済み
- セキュリティグループで `22/tcp` を許可
- 秘密鍵 (`.pem`) を保持
- EC2 に Python 3.11 以上、Git が利用可能

## 2. EC2 インスタンスタイプ目安

- 最小構成（検証用）: `t3.small`
- 標準構成（開発用）: `t3.medium`
- 余裕あり: `t3.large`

`git clone` を含めても、通常の FastAPI 開発なら `t3.medium` で十分なことが多いです。

> ただし、PyCharm の `Remote Development` 機能で EC2 上に IDE バックエンドを置く構成では、PyCharm 側が CPU コア数やメモリ要件を案内することがあります。以前の「4コア必要」は、この接続方式だった可能性があります。

## 3. EC2 に SSH 接続

```bash
ssh -i C:/path/to/your-key.pem rocky@<EC2_PUBLIC_IP>
```

## 4. EC2 でリポジトリをクローン

```bash
mkdir -p /home/rocky/work
cd /home/rocky/work
git clone <YOUR_GITHUB_REPOSITORY_URL> fastapi-rest
cd fastapi-rest
```

## 5. EC2 側セットアップ

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
cp .env.example .env
```

## 6. PyCharm で SSH Interpreter を作成

1. `File` -> `Settings` -> `Project: ...` -> `Python Interpreter`
2. 歯車アイコン -> `Add...`
3. `On SSH` を選択して EC2 接続情報を入力
4. Interpreter path を選択（例: `/usr/bin/python3`）

## 7. PyCharm のプロジェクトを開く方法

- 方法1: ローカルにも同じ Git リポジトリをクローンし、PyCharm でローカル編集
- 方法2: PyCharm の Remote Development 機能を使い、EC2 側のソースを直接扱う

> パターンBでは、EC2 側の Git 状態を正として運用するのが分かりやすいです。

## 8. 実行

```bash
cd /home/rocky/work/fastapi-rest
source .venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000 --app-dir src --reload
```

## 9. 日常運用コマンド（EC2 側）

```bash
cd /home/rocky/work/fastapi-rest
git fetch --all
git checkout <branch>
git pull --ff-only
source .venv/bin/activate
python -m pytest -q
```

## 10. 補足

- 公開アクセス時は `8000/tcp` の開放範囲を最小化してください。
- 長時間 CPU 負荷が続く場合は `t3.large` 以上も検討してください。

