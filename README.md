# 株式会社ミアキス - 公式ホームページ

埼玉県戸田市のホームページ制作会社「株式会社ミアキス」の公式Webサイトです。

## 🌐 サイトURL

- 本番環境: https://www.miakiss.co.jp

## 📋 主な機能

- **ローカルSEO対策済み**: 戸田市・埼玉県向けに最適化
- **補助金情報ページ**: Web制作に使える補助金を紹介
- **Google Maps埋め込み**: 実在性のアピール
- **レスポンシブデザイン**: PC・タブレット・スマホ対応
- **お問い合わせフォーム**: reCAPTCHA v3によるスパム対策
- **ブログ機能**: SEO対策済みの記事投稿システム

## 🚀 自動デプロイ

GitHubにプッシュすると、GitHub Actionsが自動的に本番サーバーへデプロイします。

### セットアップ手順

1. **GitHubリポジトリのSettings > Secrets and variables > Actions**に以下のSecretsを追加:

   - `SSH_PRIVATE_KEY`: サーバーへのSSH秘密鍵
   - `SERVER_HOST`: サーバーのホスト名またはIPアドレス
   - `SERVER_USER`: サーバーのユーザー名
   - `SERVER_PATH`: デプロイ先のディレクトリパス（例: `/var/www/miakiss.co.jp`）

2. **デプロイ**: masterブランチにプッシュすると自動的にデプロイされます

```bash
git add .
git commit -m "feat: 新機能を追加"
git push origin master
```

## 📁 ディレクトリ構造

```
.
├── index.html              # トップページ
├── subsidy.html           # 補助金情報ページ（NEW）
├── blog.html              # ブログ一覧ページ
├── privacy.html           # プライバシーポリシー
├── tokusho.html           # 特定商取引法
├── thanks.html            # お問い合わせ完了ページ
├── style.css              # メインスタイルシート
├── sitemap.xml            # サイトマップ
├── robots.txt             # robots.txt
├── blog/                  # ブログ記事
│   ├── *.html            # 各記事HTMLファイル
│   ├── images/           # 記事画像
│   ├── published_articles.json
│   └── published_articles.js
├── contact/               # お問い合わせフォーム
│   ├── handler.php       # フォーム送信処理
│   ├── mail.php          # メール送信
│   └── security.php      # セキュリティ設定
├── image/                # 画像ファイル
├── scripts/              # Python管理スクリプト
└── .github/
    └── workflows/
        └── deploy.yml    # 自動デプロイ設定
```

## 🛠 ローカル開発

### Pythonテストサーバー起動

```bash
python3 test_server.py
```

ブラウザで `http://localhost:8000` にアクセス

### ブログ記事の作成

```bash
# キーワードファイルから記事を生成
cd scripts
python3 sync_blog_data.py
```

## 📝 更新履歴

### 2025-12-10
- ✅ ローカルSEO強化
  - ヘッダーに電話番号追加
  - Google Maps埋め込み
  - 対応エリアの明記
  - 補助金情報ページの新規作成
  - 代表挨拶に戸田市への想いを追加
  - 構造化データに電話番号追加

### 2025-12-01 - 2025-12-10
- ブログ記事10件追加
- 記事画像の自動取得システム構築

### 2025-11-01
- 初期リリース

## 🔒 セキュリティ

- reCAPTCHA v3によるスパム対策
- CSRFトークン保護
- PHPセッション管理
- メールアドレス検証

## 📞 お問い合わせ

**株式会社ミアキス**
- 住所: 〒335-0011 埼玉県戸田市喜沢2-41-14 エフアゼリア喜沢303
- 電話: 048-400-2808
- URL: https://www.miakiss.co.jp

## 📄 ライセンス

Copyright © 2025 Miakiss Inc. All Rights Reserved.

