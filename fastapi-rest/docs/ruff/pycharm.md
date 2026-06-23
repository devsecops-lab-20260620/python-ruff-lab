# PyCharm で Ruff エラーを確認する

PyCharm には Ruff のエラーをエディタ上で表示する方法が **3 通り** あります。

---

## 方法 1: Ruff プラグインを使う（推奨）

JetBrains 公式の **Ruff プラグイン** を導入すると、ファイルを編集するたびにリアルタイムで  
Ruff のエラーがエディタ内に波線表示されます。

### プラグインが見つからない場合

#### ⚠️ PyCharm EAP を使用している場合

**PyCharm 2026.2 EAP** などの EAP（Early Access Program）ビルドでは、  
プラグインの **互換バージョン範囲外** となり Marketplace に表示されないことがあります。

| 状況 | 原因 |
|------|------|
| Marketplace に `Ruff` が表示されない | プラグインが EAP ビルドに未対応 |
| インストールはできるが動作しない | API の互換性の問題 |

**対処法：**

1. **EAP 対応版プラグインを直接ダウンロードする**  
   - https://plugins.jetbrains.com/plugin/20574-ruff/versions  
   - バージョン一覧から **Compatible with: 2026.x EAP** のものを選んで `.zip` をダウンロード  
   - **Settings → Plugins → ⚙️ → Install Plugin from Disk** で zip を選択

2. **EAP 向けに互換チェックを無効化する（非推奨・自己責任）**  
   - **Settings → Plugins → ⚙️ → Manage Plugin Repositories** に以下を追加  
     ```
     https://plugins.jetbrains.com/plugins/eap/list
     ```
   - 再度 Marketplace で `Ruff` を検索する

3. **安定版 PyCharm（2025.x）に切り替える（推奨）**  
   - EAP は開発中ビルドのため、本番・開発作業には安定版を推奨  
   - 詳細手順: [EAP から安定版への切り替え](./pycharm-eap-to-stable.md)

#### Marketplace の検索で見つからないその他の原因

4. **検索キーワードを変える**  
   - `Ruff` の代わりに `astral` や `linter` で検索する

5. **プラグインリポジトリの接続を確認する**  
   - **Settings → Plugins → ⚙️ → Manage Plugin Repositories** を開く  
   - デフォルトの `https://plugins.jetbrains.com` が登録されているか確認する

### インストール手順（通常）

1. PyCharm メニュー → **Settings（設定）** を開く  
   `Ctrl+Alt+S`（macOS: `Cmd+,`）
2. **Plugins（プラグイン）** → **Marketplace** タブを選択
3. 検索欄に `Ruff` と入力
4. **Ruff**（Astral Software 製）を選択して **Install** をクリック
5. PyCharm を再起動

### Ruff プラグインの設定

インストール後、インタープリタと実行ファイルを確認します。

1. **Settings** → **Tools** → **Ruff** を開く
2. **Ruff executable** に仮想環境の Ruff パスを指定する  
   例: `.venv/bin/ruff`（自動検出される場合は不要）
3. **Use ruff format** にチェックを入れると `ruff format` も有効化される

### 確認できること

| 機能 | 内容 |
|------|------|
| リアルタイム警告 | エディタ上に波線でエラーを表示 |
| クイックフィックス | `Alt+Enter` で自動修正を適用 |
| ファイル保存時の自動修正 | **Settings → Tools → Ruff → Run on save** を有効化 |
| フォーマット | `ruff format` をコード整形として使用 |

---

## 方法 2: External Tools に登録する（プラグインなし）

プラグインが使えない場合でも、**External Tools** に登録すれば  
PyCharm のメニューやショートカットから `ruff check` を実行できます。

### 登録手順

1. **Settings** → **Tools** → **External Tools** を開く
2. **+（追加）** をクリック
3. 以下の値を入力する

| 項目 | 値 |
|------|-----|
| **Name** | `Ruff Check` |
| **Program** | `$ProjectFileDir$/.venv/bin/ruff` |
| **Arguments** | `check src/ tests/ --statistics` |
| **Working directory** | `$ProjectFileDir$` |

4. **OK** で保存

### 自動修正版も追加する

同様にもう 1 つ追加します。

| 項目 | 値 |
|------|-----|
| **Name** | `Ruff Fix` |
| **Program** | `$ProjectFileDir$/.venv/bin/ruff` |
| **Arguments** | `check --fix src/ tests/` |
| **Working directory** | `$ProjectFileDir$` |

### 実行方法

- メニュー → **Tools** → **External Tools** → **Ruff Check**  
- 結果は PyCharm 下部の **Run** パネルに表示されます

---

## 方法 3: 内蔵ターミナルから実行する

PyCharm 内蔵ターミナルから `ruff check` を実行する方法です。  
設定不要で最もシンプルです。

### ターミナルを開く

- メニュー → **View** → **Tool Windows** → **Terminal**  
  または `Alt+F12`

### コマンド例

```bash
# 全ファイルをチェック
ruff check src/ tests/

# 統計情報付き
ruff check src/ tests/ --statistics

# 自動修正可能なエラーを修正
ruff check --fix src/ tests/
```

---

## 現在の残存エラー（2026-06-23 時点）

`ruff check --fix` 適用後、以下の **35件** が残っています。

| ルール | 件数 | 対応 |
|--------|------|------|
| `B008` | 24件 | FastAPI の `Depends()` パターン → `ignore` 設定を推奨 |
| `E501` | 11件 | 行長 100 文字超 → 手動折り返し or `line-length` 調整 |

### B008 を抑制する（推奨）

`B008` は FastAPI の正常なパターンのため、`pyproject.toml` で無視設定を追加します。

```toml
# pyproject.toml
[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B"]
ignore = ["B008"]
```

---

## まとめ

> **⚠️ PyCharm 2026.2 EAP をご利用の場合**  
> EAP ビルドはプラグインの互換性制限により Marketplace に `Ruff` が表示されないことがあります。  
> プラグインのバージョン一覧ページ（https://plugins.jetbrains.com/plugin/20574-ruff/versions）から  
> EAP 対応版 `.zip` を手動インストールするか、**方法 2・3** をご利用ください。

```
PyCharm で Ruff を使う方法

  ┌─────────────────────────────────────────────────────┐
  │  方法 1: Ruff プラグイン（推奨）                     │
  │    → Marketplace で "Ruff" を検索してインストール    │
  │    → EAP の場合は versions ページから zip を取得     │
  │    → エディタ上にリアルタイムで波線表示              │
  ├─────────────────────────────────────────────────────┤
  │  方法 2: External Tools に登録                       │
  │    → Settings → Tools → External Tools              │
  │    → メニューから ruff check を呼び出せる            │
  │    → EAP でも動作する                                │
  ├─────────────────────────────────────────────────────┤
  │  方法 3: 内蔵ターミナルで ruff check 実行            │
  │    → Alt+F12 でターミナルを開く                      │
  │    → ruff check src/ tests/                          │
  │    → EAP でも動作する                                │
  └─────────────────────────────────────────────────────┘
```



