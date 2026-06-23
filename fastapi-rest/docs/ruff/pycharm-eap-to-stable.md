# PyCharm EAP から安定版への切り替え

AWS EC2 リモート接続環境で **PyCharm 2026.2 EAP** を使用している場合、  
プラグインの互換性問題が発生しやすいため、安定版への切り替えを推奨します。

---

## 現在の最新安定版

| エディション | バージョン | 用途 |
|-------------|-----------|------|
| PyCharm Professional | **2025.1.x** | リモート開発（SSH / EC2）に対応 |
| PyCharm Community | **2025.1.x** | ローカル開発のみ（SSH リモート非対応） |

> AWS EC2 へのリモート接続には **Professional エディション** が必要です。

---

## 方法 1: JetBrains Toolbox App で切り替える（推奨）

Toolbox App を使うと複数バージョンの並行管理・アンインストールが簡単です。

### Toolbox App のインストール（未インストールの場合）

```bash
# Linux への Toolbox App インストール例
curl -fsSL https://raw.githubusercontent.com/nagygergo/jetbrains-toolbox-install/master/jetbrains-toolbox.sh | bash
```

または公式サイトからダウンロード：  
https://www.jetbrains.com/toolbox-app/

### 安定版 PyCharm のインストール手順

1. **Toolbox App** を起動する
2. **PyCharm Professional** の横にある **▼（バージョン選択）** をクリック
3. **Available versions** から `2025.1.x`（EAP でないもの）を選択
4. **Install** をクリック

### EAP のアンインストール

1. Toolbox App の一覧で **PyCharm 2026.2 EAP** を探す
2. 右の **⚙️** → **Uninstall** をクリック
3. 設定を残すか確認ダイアログが表示される → **Remove** または **Keep** を選択

---

## 方法 2: 直接ダウンロードして切り替える

1. 公式ダウンロードページを開く  
   https://www.jetbrains.com/pycharm/download/other.html

2. **Version** プルダウンで `2025.1.x` を選択

3. **Linux (.tar.gz)** をダウンロード

4. 展開してインストール

```bash
tar -xzf pycharm-professional-2025.1.*.tar.gz -C ~/opt/
~/opt/pycharm-2025.1.*/bin/pycharm.sh
```

---

## 切り替え後の設定移行

### プロジェクト設定はそのまま引き継がれる

`.idea/` ディレクトリ内の設定は安定版でも使用できます。

### SSH インタープリタの再設定

AWS EC2 へのリモート接続は再設定が必要な場合があります。

1. **Settings** → **Project** → **Python Interpreter** を開く
2. **⚙️ Add Interpreter** → **On SSH** を選択
3. EC2 の接続情報を入力する

| 項目 | 値 |
|------|-----|
| Host | EC2 のパブリック IP または DNS |
| Username | `ec2-user` / `ubuntu` など |
| Authentication | **Key pair** → `.pem` ファイルを指定 |

### Ruff プラグインのインストール

安定版に切り替えたあとは Marketplace から��常どおりインストールできます。

1. **Settings** → **Plugins** → **Marketplace**
2. `Ruff` を検索 → **Install**
3. PyCharm を再起動

---

## まとめ

```
EAP → 安定版 切り替え手順

  1. JetBrains Toolbox App を使う（推奨）
     → PyCharm Professional 2025.1.x をインストール
     → EAP をアンインストール

  2. 切り替え後
     → SSH インタープリタを再設定（EC2 接続）
     → Ruff プラグインを Marketplace からインストール
     → ruff check src/ tests/ で動作確認
```

