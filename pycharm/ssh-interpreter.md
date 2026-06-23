# SSH Interpreter を使う構成（今回の推奨）

今回の構成では、**PyCharm の `SSH Interpreter` を使う方法を推奨**します。

この方法は、PyCharm の IDE 本体は **Windows 側** で動かし、**Python 実行環境だけを EC2 側** に置く構成です。
そのため、以前表示されたような **「4コア必要」** という条件に引っかかりにくく、`t3.medium` でも進めやすいです。

## この構成が向いている理由

- EC2 側に IDE バックエンドを常駐させない
- 通常の FastAPI 開発であれば `t3.medium` でも実用的
- PyCharm の補完・編集は手元 Windows 側で完結しやすい
- `Remote Development` より構成が分かりやすい

## 注意: 選ぶメニューを間違えない

PyCharm には似たようなリモート接続方法があります。

### 選ぶもの

- `File` -> `Settings` -> `Project: ...` -> `Python Interpreter`
- 歯車アイコン -> `Add...`
- `On SSH`

### 今回は選ばないもの

- `Remote Development`
- `JetBrains Gateway`
- IDE バックエンドをリモート起動する接続方式

> 以前の「4コア必要だから接続できない」は、`SSH Interpreter` ではなく `Remote Development` 系の接続を選んでいた可能性が高いです。

## 推奨 EC2 スペック

- 推奨: `t3.medium`
- さらに軽く試すだけなら: `t3.small`
- テストや複数プロセスで余裕を持たせたいなら: `t3.large`

`fastapi-rest` の通常開発では、まず `t3.medium` から始める方針で問題ないことが多いです。

## SSH Interpreter 設定手順

1. `File` -> `Settings` -> `Project: ...` -> `Python Interpreter`
2. 歯車アイコン -> `Add...`
3. `On SSH` を選択
4. 接続先を入力
   - Host: `<EC2_PUBLIC_IP>`
   - Port: `22`
   - Username: `rocky`（AMI に応じて `ec2-user` など）
   - Authentication type: `Key pair`
   - Private key file: `C:\path\to\your-key.pem`
5. Interpreter path を選択
   - 例: `/usr/bin/python3`
   - 仮想環境を使うなら例: `/home/rocky/work/fastapi-rest/.venv/bin/python`

## EC2 側の初期セットアップ例

```bash
cd /home/rocky/work/fastapi-rest
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
cp .env.example .env
```

## FastAPI 実行設定

PyCharm の `Run Configuration` で次のように設定します。

- Run type: `Python`
- Module name: `uvicorn`
- Parameters: `main:app --host 0.0.0.0 --port 8000 --app-dir src --reload`
- Working directory: `/home/rocky/work/fastapi-rest`
- Python interpreter: 作成した `SSH Interpreter`

## どの運用パターンと組み合わせるか

- EC2 に `git clone` しない場合: `pattern-a-sftp.md`
- EC2 に `git clone` する場合: `pattern-b-git-clone.md`

どちらのパターンでも、**Python の実行方法としては `SSH Interpreter` を使う**方針で問題ありません。

