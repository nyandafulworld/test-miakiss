# ブログ機能について

## 概要

このWebサイトには、ローカルファイルでもWebサーバーでも動作するブログ機能が実装されています。

## ファイル構成

```
Miakiss_Web/
├── index.html                          # トップページ（最新3記事を表示）
├── blog.html                           # ブログ一覧ページ（全記事をページネーション表示）
├── blog/
│   ├── published_articles.json         # 記事データ（マスター）
│   ├── published_articles.js           # 記事データ（JavaScriptファイル、自動生成）
│   └── [各記事のHTMLファイル]
└── scripts/
    ├── sync_blog_data.py               # JSONからJSファイルを生成するスクリプト
    └── update_index.py                 # サイトマップ更新スクリプト
```

## 新しい記事を追加する手順

### 1. 記事HTMLファイルを作成

`blog/` ディレクトリに新しい記事のHTMLファイルを作成します。

ファイル名の形式: `YYYY-MM-DD-slug.html`

例: `2025-12-06-new-article.html`

### 2. published_articles.json に記事情報を追加

`blog/published_articles.json` を編集し、新しい記事の情報を追加します。

```json
{
  "slug": "2025-12-06-new-article",
  "title": "記事のタイトル",
  "date": "2025-12-06",
  "category": "A",
  "keyword": "キーワード",
  "description": "記事の説明文（抜粋）"
}
```

### 3. JavaScriptファイルを同期

ターミナルで以下のコマンドを実行し、`published_articles.js` を更新します。

```bash
cd /Users/game_gct/Miakiss_Web
python3 scripts/sync_blog_data.py
```

**重要:** この手順を忘れると、ローカルファイルで開いた際に新しい記事が表示されません。

### 4. 動作確認

ブラウザで `index.html` または `blog.html` を開き、新しい記事が表示されることを確認します。

**ローカルファイルで確認する場合:**
- そのまま HTMLファイルをブラウザで開く

**ローカルサーバーで確認する場合:**
```bash
python3 test_server.py
# http://localhost:8000 にアクセス
```

## 記事データの形式

### 必須フィールド

- `slug`: 記事のスラッグ（ファイル名と一致させる、拡張子なし）
- `title`: 記事のタイトル
- `date`: 公開日（YYYY-MM-DD形式）
- `description`: 記事の説明文（一覧ページで表示される抜粋）

### オプションフィールド

- `category`: 記事のカテゴリ（A, B, Cなど）
- `keyword`: SEO用キーワード

## トラブルシューティング

### 記事が表示されない

1. **ブラウザのキャッシュをクリア**
   - `Ctrl + Shift + R` (Windows/Linux)
   - `Cmd + Shift + R` (Mac)

2. **published_articles.js を再生成**
   ```bash
   python3 scripts/sync_blog_data.py
   ```

3. **ブラウザのコンソールを確認**
   - `F12` キーを押してデベロッパーツールを開く
   - Consoleタブでエラーメッセージを確認

### よくあるエラー

**「○件の記事を読み込みました」と表示されるのに記事が見えない**
- スタイルシートの問題の可能性があります
- `style.css` が正しく読み込まれているか確認してください

**「ローカルデータから記事を読み込みます」と表示されない**
- `published_articles.js` が読み込まれていません
- HTMLファイルに `<script src="blog/published_articles.js"></script>` が含まれているか確認してください

## 技術的な詳細

### ローカルファイル対応の仕組み

1. `published_articles.js` をHTMLの`<script>`タグで読み込む
2. JavaScriptファイルは `window.BLOG_ARTICLES_DATA` にデータを格納
3. ブログ読み込み処理は、まずグローバル変数をチェック
4. グローバル変数が存在すればそれを使用（ローカルファイル対応）
5. 存在しなければfetch APIでJSONを読み込む（Webサーバー対応）

この仕組みにより、ローカルファイルでもWebサーバーでも同じコードで動作します。

### データの同期

- **マスターデータ:** `published_articles.json`
- **自動生成ファイル:** `published_articles.js`

`published_articles.json` を編集したら、必ず `sync_blog_data.py` を実行してJavaScriptファイルを更新してください。

## 本番環境へのデプロイ

本番環境では、以下のファイルをアップロードしてください：

- `index.html`
- `blog.html`
- `blog/published_articles.json`
- `blog/published_articles.js`
- `blog/[各記事のHTMLファイル]`
- `style.css`
- その他必要なアセットファイル

**注意:** `test_server.py` や `scripts/` ディレクトリは、本番環境にアップロードする必要はありません（開発用ツールです）。

## 更新履歴

- **2025-12-06:** ローカルファイル対応を実装（published_articles.js を使用）
- **2025-12-06:** ブログ一覧ページ作成、ページネーション機能追加










