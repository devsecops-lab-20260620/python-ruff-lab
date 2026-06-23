# PyCharm + AWS EC2 開発ガイド

Windows 上の PyCharm から AWS EC2 (Rocky Linux) で `python-ruff-lab/fastapi-rest` を開発する手順を、運用パターンごとに分割しています。

## ドキュメント一覧

- `ssh-interpreter.md`
  - 今回の推奨構成
  - `t3.medium` で進めやすい `SSH Interpreter` 利用手順
- `pattern-a-sftp.md`
  - EC2 で `git clone` しない
  - PyCharm Deployment/SFTP 同期で開発
- `pattern-b-git-clone.md`
  - EC2 で `git clone` する
  - EC2 側で Git 運用しながら開発

## どちらを選ぶか

- 今回の推奨: `SSH Interpreter` を使う
- すぐ始めたい/単純運用: パターンA
- サーバー側でも Git 操作したい/本番寄り: パターンB

どちらのパターンでも、通常の FastAPI 開発用途であれば `t3.medium` は実用的な選択です。

## PyCharm の「SSH 接続」には 2 種類ある点に注意

- `SSH Interpreter` を使う方法
  - Python インタープリタだけを EC2 上に置く方式
  - 一般に 4 コア要件の話とは別です
- `Remote Development` / `JetBrains Client` を使う方法
  - IDE バックエンド自体を EC2 上で動かす方式
  - 環境や PyCharm の案内によっては、CPU コア数やメモリ要件が表示されることがあります

以前に「4コア必要だから接続できない」と表示された場合は、`SSH Interpreter` ではなく `Remote Development` 側の接続フローを選んでいた可能性があります。

