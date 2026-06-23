# Ruff — インストール・実行ガイド

[Ruff](https://docs.astral.sh/ruff/) は Rust 製の高速な Python リンター＆フォーマッターです。  
このプロジェクトでは **開発依存パッケージ** として `pyproject.toml` に定義されています。

---

## 目次

1. [前提条件](#前提条件)
2. [インストール](#インストール)
3. [設定](#設定)
4. [実行方法](#実行方法)
5. [チェック結果の履歴](#チェック結果の履歴)
6. [残存エラーの対応方針](#残存エラーの対応方針)
7. [PyCharm との連携](./pycharm.md)

---

## 前提条件

| 項目 | バージョン |
|------|-----------|
| Python | 3.11 以上 |
| pip | 最新推奨 |

---

## インストール

### 方法 1: dev 依存としてインストール（推奨）

`pyproject.toml` の `[project.optional-dependencies]` に定義済みです。

```bash
# 仮想環境を作成・有効化
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# dev 依存パッケージ（Ruff 含む）をインストール
pip install -e ".[dev]"
```

### 方法 2: 単体インストール

```bash
pip install ruff==0.12.1
```

### インストール確認

```bash
ruff --version
# ruff 0.12.1
```

---

## 設定

Ruff の設定は `pyproject.toml` に記述されています。

```toml
[tool.ruff]
line-length = 100          # 1行の最大文字数
target-version = "py311"   # 対象 Python バージョン

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B"]
```

### 有効化ルールセット

| コード | 内容 |
|--------|------|
| `E` | pycodestyle エラー（スタイル違反） |
| `F` | Pyflakes（未使用変数・インポートなど） |
| `I` | isort（import の順序） |
| `UP` | pyupgrade（古い Python 構文の検出） |
| `B` | flake8-bugbear（バグになりやすいパターン） |

---

## 実行方法

以下のコマンドはプロジェクトルート（`pyproject.toml` があるディレクトリ）で実行してください。

### チェック（lint）

```bash
# src/ と tests/ 全体をチェック
ruff check src/ tests/
```

```bash
# 特定ファイルのみチェック
ruff check src/app/schemas.py
```

### 自動修正

修正可能な問題（`[*]` が付いているもの）を自動で修正します。

```bash
# 自動修正を適用
ruff check --fix src/ tests/
```

```bash
# 修正内容を事前確認（ファイルは変更しない）
ruff check --diff src/ tests/
```

### フォーマット

```bash
# コードフォーマット（black 互換）
ruff format src/ tests/
```

```bash
# フォーマット差分を確認（ファイルは変更しない）
ruff format --diff src/ tests/
```

### 統計情報付きチェック

```bash
# エラーの統計を表示
ruff check --statistics src/ tests/
```

### 出力フォーマットの変更

```bash
# GitHub Actions 用フォーマット
ruff check --output-format=github src/ tests/

# JSON 形式で出力
ruff check --output-format=json src/ tests/
```

---

## チェック結果の履歴

### 初回チェック結果（`ruff check src/ tests/`）

2026-06-23 時点：

| ルール | 件数 | 内容 |
|--------|------|------|
| `B008` | 20件 | `Depends()` / `Query()` をデフォルト引数で使用（FastAPI の正常パターン） |
| `E501` | 10件 | 行長 100 文字超 |
| `UP035` | 4件 | `typing.Dict` / `typing.List` は非推奨 |
| `UP045` | 30件 | `Optional[X]` → `X \| None` に変更推奨 |
| `UP006` | 12件 | `Dict` / `List` → `dict` / `list` に変更推奨 |
| `I001` | 3件 | import の順序が不正 |
| **合計** | **82件** | うち **43件** は `--fix` で自動修正可能 |

### 自動修正後（`ruff check --fix src/ tests/`）

2026-06-23 時点：

```bash
ruff check --fix src/ tests/
```

| ルール | 件数 | 内容 |
|--------|------|------|
| `B008` | 24件 | `Depends()` / `Query()` をデフォルト引数で使用（FastAPI の正常パターン） |
| `E501` | 11件 | 行長 100 文字超 |
| **合計** | **35件** | 自動修正不可（手動対応が必要） |

43件（`UP035` / `UP045` / `UP006` / `I001`）が自動修正済みです。

---

## 残存エラーの対応方針

### B008 — FastAPI の `Depends()` パターン

`B008` は FastAPI のイディオムとして意図的に使用されているため、  
`pyproject.toml` で無視設定を追加することを推奨します。

```toml
[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B"]
ignore = ["B008"]   # FastAPI の Depends() / Query() パターンを許容
```

### E501 — 行が長すぎる

`line-length` の値を引き上げるか、該当行を手動で折り返します。

```toml
[tool.ruff]
line-length = 120   # 必要に応じて調整
```




