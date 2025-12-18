# ブログ自動投稿ワークフロー

## 概要

Cursorで「今日の記事を作成して」と入力するだけで、SEO記事を自動生成し、
Git pushすると自動でXserverにデプロイされます。

**重複防止機能**（2025年12月更新）:
- 画像: 別の日と同じ画像は使用されません
- テーマ/キーワード: 過去に使用したキーワードは選択されません

## 毎日の作業フロー（約1分）

### 1. Cursorで記事生成

```
今日の記事を作成して
```

これだけで以下が自動実行されます：
- `blog/keywords.json` から未使用テーマを選択（重複チェック付き）
- `blog/article_template.html` 形式でHTML生成
- `blog/` フォルダにファイル保存
- `blog/images/` にユニークな画像をダウンロード
- `blog/published_articles.json` を更新
- `blog/used_keywords.json` を更新
- `blog/used_images.json` を更新

### 2. Git push

ターミナルで以下を実行：

```bash
git add .
git commit -m "記事追加: [記事タイトル]"
git push
```

### 3. 自動デプロイ

Git pushすると GitHub Actions が自動実行：
- JSONファイルの検証
- 重複キーワードのチェック
- FTP経由でXserverにデプロイ
- 1-2分後にサイトに反映

## ファイル構成

```
Miakiss_Web/
├── .cursorrules            # 記事生成ルール
├── blog/
│   ├── article_template.html   # HTMLテンプレート
│   ├── keywords.json           # 145件のキーワードテーマ
│   ├── published_articles.json # 公開済み記事リスト
│   ├── published_articles.js   # ブログ一覧表示用（自動生成）
│   ├── used_keywords.json      # 使用済みキーワード管理
│   ├── used_images.json        # 使用済み画像管理
│   ├── images/                 # 記事画像
│   └── [YYYY-MM-DD-slug].html  # 生成される記事
├── .github/workflows/
│   └── deploy.yml          # 自動デプロイ設定
└── scripts/
    ├── create_today_article.py  # キーワード選択
    ├── download_blog_image.py   # 画像ダウンロード
    ├── sync_blog_data.py        # データ同期
    ├── deploy_article.py        # デプロイ実行
    └── update_sitemap.py        # sitemap更新
```

## 重複防止の仕組み

### 画像の重複防止

`download_blog_image.py` は以下の仕組みで画像の重複を防止します：

1. `used_images.json` から過去に使用したシード値を読み込む
2. 使用されていないユニークなシードを生成（1-9999の範囲）
3. 画像ダウンロード後、使用したシードを `used_images.json` に記録

### キーワード/テーマの重複防止

`create_today_article.py` は以下の仕組みでキーワードの重複を防止します：

1. `used_keywords.json` から使用済みキーワードIDとテキストを読み込む
2. `published_articles.json` からも使用済み情報を取得してマージ
3. 未使用のキーワードのみから選択

## FTP直接アップロード時の注意事項

⚠️ **重要**: FileZillaなどでFTP経由で直接ファイルをアップロードした場合、
GitHub Actionsのデプロイ状態と不整合が発生する可能性があります。

### FTP直接アップロード後の同期方法

**方法1: 強制フルシンク（推奨）**

GitHub Actions の画面から手動でワークフローを実行し、
「Force full sync」オプションを有効にしてください。

1. GitHubリポジトリの「Actions」タブを開く
2. 「Deploy to Production via FTP」を選択
3. 「Run workflow」をクリック
4. 「Force full sync (reset FTP state)」にチェック
5. 「Run workflow」で実行

これにより、すべてのファイルが再アップロードされ、状態が同期されます。

**方法2: ローカルからの同期**

1. FTPでアップロードしたファイルをローカルにも反映
2. `git add .` でステージング
3. `git commit -m "FTPアップロード分を同期"`
4. `git push` でデプロイ

### FTP直接アップロードを避けるべき理由

- GitHub Actionsは差分デプロイを行うため、状態ファイルとサーバーの内容が不一致になる
- 不一致が発生すると、一部のファイルがデプロイされない可能性がある
- Git履歴にも残らないため、変更の追跡が困難になる

**推奨**: すべての変更はGit push経由で行い、FTP直接アップロードは緊急時のみに限定してください。

## GitHub Secrets 設定（初回のみ）

GitHubリポジトリの Settings > Secrets and variables > Actions で以下を設定：

| Secret名 | 値 |
|---------|---|
| `FTP_SERVER` | Xserverのホスト名（例: sv1234.xserver.jp） |
| `FTP_USERNAME` | FTPユーザー名 |
| `FTP_PASSWORD` | FTPパスワード |
| `FTP_SERVER_DIR` | アップロード先ディレクトリ（例: /miakiss.co.jp/public_html/） |

## キーワード戦略

### カテゴリ配分
- **A（新規制作）25%**: ホームページ制作の費用、選び方、事例
- **B（保守・サブスク）25%**: 保守の必要性、月額メリット
- **C（課題解決）20%**: 具体的な問題と解決策
- **D（用語解説）15%**: 技術用語の分かりやすい解説
- **E（補助金情報）15%**: 補助金の申請方法、活用事例

### オリジナル記事のポイント

1. **独自視点**: ミアキス代表・髙橋の経験談を入れる
2. **具体的数字**: 「約○○円」「○○%」など
3. **地域特化**: 埼玉県・戸田市の文脈
4. **会話調**: 「実は〜なんです」「よく聞かれるのが〜」
5. **Q&A活用**: 実際の相談事例風のやり取り

## トラブルシューティング

### 記事が生成されない
- `.cursorrules` が存在するか確認
- `blog/keywords.json` の形式が正しいか確認

### デプロイされない
- GitHub Secrets が正しく設定されているか確認
- GitHub Actions のログを確認
- FTP直接アップロードしていた場合は「強制フルシンク」を実行

### 同じキーワードが選択される
- `blog/used_keywords.json` が存在するか確認
- 存在しない場合は以下のコマンドで再構築:
  ```bash
  python3 scripts/create_today_article.py --sync
  ```

### 同じ画像が使われる
- `blog/used_images.json` が存在するか確認
- ファイルが破損している場合は削除して再生成

### published_articles.js が更新されない
- 以下のコマンドで手動同期:
  ```bash
  python3 scripts/sync_blog_data.py
  ```

## データ修復コマンド

### used_keywords.json を再構築
```bash
python3 scripts/create_today_article.py --sync
```

### published_articles.js を同期
```bash
python3 scripts/sync_blog_data.py
```

## 週末まとめ生成（オプション）

日曜日に1週間分をまとめて生成する場合：

```
今週分の記事を7本生成して。1本ずつファイルに保存して。
```

## お問い合わせ

システムに関する質問は株式会社ミアキスまで。
