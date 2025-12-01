# ブログ自動投稿ワークフロー

## 概要

Cursorで「今日の記事を作成して」と入力するだけで、SEO記事を自動生成し、
Git pushすると自動でXserverにデプロイされます。

## 毎日の作業フロー（約1分）

### 1. Cursorで記事生成

```
今日の記事を作成して
```

これだけで以下が自動実行されます：
- `blog/keywords.json` から未使用テーマを選択
- `blog/article_template.html` 形式でHTML生成
- `blog/` フォルダにファイル保存
- `blog/published_articles.json` を更新

### 2. Git push

ターミナルで以下を実行：

```bash
git add .
git commit -m "記事追加: [記事タイトル]"
git push
```

### 3. 自動デプロイ

Git pushすると GitHub Actions が自動実行：
- `index.html` のブログセクションを更新
- `sitemap.xml` に新記事URLを追加
- FTP経由でXserverにデプロイ

## ファイル構成

```
Miakiss_Web/
├── .cursorrules            # 記事生成ルール
├── blog/
│   ├── article_template.html   # HTMLテンプレート
│   ├── keywords.json           # 105件のキーワードテーマ
│   ├── published_articles.json # 公開済み記事リスト
│   └── [YYYY-MM-DD-slug].html  # 生成される記事
├── .github/workflows/
│   └── deploy.yml          # 自動デプロイ設定
└── scripts/
    ├── update_index.py     # index.html更新
    └── update_sitemap.py   # sitemap更新
```

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
- **A（新規制作）30%**: ホームページ制作の費用、選び方、事例
- **B（保守・サブスク）40%**: 保守の必要性、月額メリット ★重点
- **C（課題解決）30%**: 具体的な問題と解決策

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

### index.htmlが更新されない
- `scripts/update_index.py` のパスが正しいか確認
- `blog/published_articles.json` の形式を確認

## 週末まとめ生成（オプション）

日曜日に1週間分をまとめて生成する場合：

```
今週分の記事を7本生成して。1本ずつファイルに保存して。
```

## お問い合わせ

システムに関する質問は株式会社ミアキスまで。
