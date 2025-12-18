# ブログ画像自動取得 - セットアップガイド

## 概要

ブログ記事用の画像を**Unsplash API**と**Pexels API**から自動取得するシステムです。
両方のAPIは**完全無料**で使用できます。

## APIキーの取得方法

### 1. Unsplash APIキーの取得（推奨）

**無料プラン**
- 制限: 50リクエスト/時間
- 高品質な写真が豊富
- 商用利用可能

**取得手順:**

1. [Unsplash Developers](https://unsplash.com/developers)にアクセス
2. 「Register as a developer」をクリック
3. アカウント作成（無料）
4. 「New Application」を作成
   - Application name: `Miakiss Blog Images`
   - Description: `Auto-fetch blog images for Miakiss website`
5. 作成されたアプリの**Access Key**をコピー

### 2. Pexels APIキーの取得（フォールバック）

**無料プラン**
- 制限: 200リクエスト/時間
- Unsplashより制限が緩い
- 商用利用可能

**取得手順:**

1. [Pexels API](https://www.pexels.com/api/)にアクセス
2. 「Get Started」をクリック
3. アカウント作成（無料）
4. **API Key**が即座に発行されるのでコピー

## ローカル環境の設定

### 1. `.env`ファイルの作成

プロジェクトルートに`.env`ファイルを作成します：

```bash
# .envファイル（プロジェクトルートに配置）

# Unsplash API
UNSPLASH_ACCESS_KEY=あなたのUnsplashアクセスキー

# Pexels API
PEXELS_API_KEY=あなたのPexelsAPIキー
```

⚠️ **重要:** `.env`ファイルはGitにコミットしないでください（既に.gitignoreに追加済み）

### 2. Pythonパッケージのインストール

```bash
pip install -r requirements.txt
```

または個別にインストール：

```bash
pip install requests Pillow python-dotenv
```

## GitHub Actionsの設定（自動デプロイ用）

GitHub Actionsで自動的に画像を取得するには、リポジトリにSecretsを追加します。

### 手順:

1. GitHubリポジトリページを開く
2. `Settings` > `Secrets and variables` > `Actions`
3. `New repository secret`をクリック
4. 以下のSecretsを追加:

| Secret名 | 値 |
|---------|---|
| `UNSPLASH_ACCESS_KEY` | UnsplashのAccess Key |
| `PEXELS_API_KEY` | PexelsのAPI Key |

※ 既存のFTP関連のSecretsも必要です：
- `FTP_SERVER`
- `FTP_USERNAME`
- `FTP_PASSWORD`
- `FTP_SERVER_DIR`

## 使い方

### 方法1: 記事作成時に自動実行（推奨）

Cursorで記事を作成すると、自動的に画像が取得されます：

```
今日の記事を作成して
```

自動的に実行される処理：
1. 記事HTMLの生成
2. **画像の自動取得**（新機能！）
   - アイキャッチ画像（800px幅）
   - ヘッダー画像（1200px幅）
3. `published_articles.json`の更新
4. Git push → 自動デプロイ

### 方法2: 手動で画像を取得

既存の記事に画像を追加したい場合：

```bash
python scripts/fetch_blog_images.py "記事のslug" "記事タイトル" "記事の説明"
```

例：
```bash
python scripts/fetch_blog_images.py \
  "2025-12-06-toda-sme-website-necessity" \
  "戸田市の中小企業がホームページを作るべき理由" \
  "戸田市の中小企業にホームページは本当に必要？"
```

## 画像の保存先

```
blog/images/
├── 2025-12-06-toda-sme-website-necessity_thumbnail.jpg  # アイキャッチ（800px）
├── 2025-12-06-toda-sme-website-necessity_header.jpg      # ヘッダー（1200px）
└── ...
```

## トラブルシューティング

### 画像が取得できない

**原因1: APIキーが設定されていない**
```bash
# .envファイルが存在するか確認
ls -la .env

# 内容を確認（キーが正しく設定されているか）
cat .env
```

**原因2: API制限に達した**
- Unsplash: 50リクエスト/時間
- Pexels: 200リクエスト/時間

→ 時間をおいてから再試行してください

**原因3: ネットワークエラー**
```bash
# インターネット接続を確認
ping google.com
```

### 画像が表示されない

**フォールバック機能**
画像が見つからない場合、自動的に`image/ogp.png`（デフォルト画像）が表示されます。

**確認方法:**
```bash
# 画像ファイルが存在するか確認
ls -la blog/images/
```

## 料金について

**完全無料**です！

- Unsplash: 無料（50リクエスト/時間）
- Pexels: 無料（200リクエスト/時間）

毎日1記事の場合、どちらのAPIも十分な余裕があります。

## クレジット表記（推奨）

画像は商用利用可能ですが、以下のクレジット表記を推奨します：

- Unsplash: `Photo by [Photographer Name] on Unsplash`
- Pexels: `Photo by [Photographer Name] from Pexels`

記事内にクレジットを記載する場合は、画像キャプションに含めると良いでしょう。

## サポート

問題が発生した場合は、以下を確認してください：

1. `.env`ファイルが正しく設定されているか
2. `requirements.txt`のパッケージがインストールされているか
3. APIキーが有効か（Unsplash/Pexelsのダッシュボードで確認）

それでも解決しない場合は、エラーメッセージを確認してください。


















