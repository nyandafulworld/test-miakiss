# 株式会社ミアキス - ブログ記事作成ワークフロー

このドキュメントは、AIエディター（Cursor、Windsurf、GitHub Copilot等）でブログ記事を作成する際の完全なワークフロー手順書です。

---

## 基本情報

- **会社名**: 株式会社ミアキス
- **所在地**: 埼玉県戸田市
- **事業**: Web制作、EC運営支援、保守運用
- **ブランドカラー**: ティールグリーン `#0D9488`
- **回答言語**: 必ず日本語で回答すること

---

## ワークフロー概要

「今日の記事を作成して」と言われたら、以下の7ステップを順番に実行してください。

| Step | 内容 | 必須ファイル |
|------|------|-------------|
| 1 | テーマ選択 | `blog/keywords.json`, `blog/used_keywords.json` |
| 2 | 画像生成プロンプト提示 | - |
| 3 | ユーザーが画像を生成・保存 | `blog/images/` |
| 4 | 画像圧縮 | `scripts/compress_images.py` |
| 5 | HTML記事生成 | `blog/article_template.html` |
| 6 | データ同期 | `scripts/sync_blog_data.py` |
| 7 | Git コミット＆プッシュ | - |

---

## Step 1: テーマ選択

### 1.1 ファイルを読み込む

以下の2つのファイルを読み込んでください：

```
blog/keywords.json       # キーワードとテーマのマスターリスト
blog/used_keywords.json  # 使用済みキーワードの記録
```

### 1.2 未使用のキーワードを選択

- `keywords.json` の `keywords` 配列から1つ選ぶ
- `used_keywords.json` の `used_keyword_ids` に含まれていないIDを選ぶ
- カテゴリ配分を意識する：
  - **A（新規制作）**: 30% - 費用、選び方、事例
  - **B（保守）**: 40% - 必要性、リスク、月額メリット
  - **C（課題解決）**: 30% - 問題と解決策
  - **D（用語解説）**: 補足的に使用
  - **E（補助金情報）**: 補足的に使用

### 1.3 選択結果をユーザーに報告

以下の形式で報告してください：

```markdown
## ステップ1: テーマ選択

| 項目 | 内容 |
|------|------|
| **ID** | 16 |
| **カテゴリ** | A（新規制作案件向け） |
| **キーワード** | 店舗 ホームページ 必要 |
| **テーマ** | 店舗ビジネスにホームページは本当に必要か？ |
```

---

## Step 2: 画像生成プロンプト提示

### 2.1 必要な画像

| 種類 | サイズ | アスペクト比 | 必須 | 用途 |
|------|--------|-------------|------|------|
| ヘッダー画像 | 1200×630px | 約1.9:1 | ✅ | 記事トップに表示 |
| サムネイル画像 | 600×340px | 約16:9 | ✅ | 一覧ページで表示（高さ180px固定でトリミング） |
| 図解画像 | 800×450px | 16:9 | 任意 | 記事内の説明用 |

### 2.2 ファイル命名規則

```
{YYYY-MM-DD}-{slug}_header.png
{YYYY-MM-DD}-{slug}_thumbnail.png
{YYYY-MM-DD}-{slug}_diagram.png
```

**例**: `2026-01-21-store-website-necessity_header.png`

### 2.3 保存先

```
blog/images/
```

### 2.4 画像生成プロンプトのテンプレート

以下の形式でユーザーに提示してください：

```markdown
## ステップ2: Freepik用画像生成プロンプト

以下のプロンプトでFreepikで画像を生成してください。

### ヘッダー画像（必須）
- **サイズ**: 1200×630px
- **ファイル名**: `{YYYY-MM-DD}-{slug}_header.png`
- **保存先**: `blog/images/`

**プロンプト:**
```
[記事テーマに関連した具体的な画像プロンプト]
Teal green (#0D9488) accent colors. Professional photograph style, bright and inviting atmosphere. Japanese context.
```

### サムネイル画像（必須）
- **サイズ**: 600×340px（16:9比率）
- **ファイル名**: `{YYYY-MM-DD}-{slug}_thumbnail.png`
- **保存先**: `blog/images/`

**プロンプト:**
```
Simple flat illustration of [記事テーマに関連したシンプルなイラスト].
Teal green (#0D9488) and white color scheme. Minimalist Japanese style, clean modern design. Wide aspect ratio 16:9.
```

### 図解画像（任意・概念説明用）
- **サイズ**: 800×450px（16:9比率）
- **ファイル名**: `{YYYY-MM-DD}-{slug}_diagram.png`
- **保存先**: `blog/images/`

**プロンプト:**
```
Clean infographic showing [記事の概念を説明する図解].
Teal green (#0D9488) accent, minimalist Japanese design, white background, simple icons and arrows. Wide aspect ratio 16:9.
```
```

### 2.5 プロンプト作成のガイドライン

1. **ブランドカラー必須**: `Teal green (#0D9488)` を必ず含める
2. **日本文脈**: `Japanese` `Japan` などを含める
3. **シンプル**: `minimalist` `clean` `simple` などを使う
4. **明るい雰囲気**: `bright` `inviting` `professional` などを使う
5. **具体的な描写**: 抽象的な表現を避け、具体的なシーンを描写する

---

## Step 3: ユーザーによる画像生成・保存

ユーザーに以下を確認してください：

```markdown
---

## 次のステップ

1. 上記プロンプトでFreepikから画像を生成
2. PNG形式で `blog/images/` に保存
3. 保存完了したらお知らせください。画像圧縮とHTML記事を生成します。

画像の生成・保存は完了しましたか？
```

**重要**: ユーザーから「完了しました」等の返答があるまで、次のステップに進まないでください。

---

## Step 4: 画像圧縮

### 4.1 圧縮スクリプトの実行

```bash
cd /Users/game_gct/Miakiss_Web
python3 scripts/compress_images.py {YYYY-MM-DD}-{slug}
```

**例**:
```bash
python3 scripts/compress_images.py 2026-01-21-store-website-necessity
```

### 4.2 圧縮結果の確認

スクリプトは以下を実行します：
- PNG → JPEG に変換
- 画像サイズを最適化
- 元のPNGファイルを削除

成功すると以下のようなメッセージが表示されます：
```
✅ 圧縮完了: 3/3 画像
```

### 4.3 圧縮設定（参考）

| 画像タイプ | 最大幅 | 品質 | 最大サイズ |
|-----------|--------|------|-----------|
| header | 1200px | 82% | 100KB |
| thumbnail | 600px | 80% | 50KB |
| diagram | 800px | 85% | 80KB |

---

## Step 5: HTML記事生成

### 5.1 テンプレートの読み込み

```
blog/article_template.html
```

### 5.2 HTML生成の重要ルール

**⚠️ Markdown記法を使わず、すべてHTMLタグで記述すること**

| NG（Markdown） | OK（HTML） |
|----------------|------------|
| `**太字**` | `<strong>太字</strong>` |
| `*斜体*` | `<em>斜体</em>` |
| `[text](url)` | `<a href="url">text</a>` |
| `- リスト` | `<ul><li>リスト</li></ul>` |
| `# 見出し` | `<h2>見出し</h2>` |

### 5.3 記事の品質基準

| 項目 | 基準 |
|------|------|
| 文字数 | 2500〜3500文字 |
| h2見出し | 3〜5個 |
| 内部リンク | 必須（`/#service`, `/#pricing`, `/#contact`） |
| CTA | 記事末尾に問い合わせ誘導 |

### 5.4 オリジナル記事の必須ルール

1. **独自視点**: ミアキス代表の経験談や自社事例を入れる
2. **具体的数字**: 独自の見解を含める
3. **地域特化**: 埼玉県・戸田市の文脈を入れる
4. **会話調**: 自然な語り口で書く
5. **独自表現**: ありきたりな表現を避ける
6. **構成変更**: 一般的記事と異なる切り口で展開
7. **Q&A活用**: 実際の相談事例風のやり取りを含める

### 5.5 HTMLファイルの保存

- **ファイル名**: `{YYYY-MM-DD}-{slug}.html`
- **保存先**: `blog/`

**例**: `blog/2026-01-21-store-website-necessity.html`

### 5.6 プレースホルダーの置換

テンプレート内の以下のプレースホルダーを置換してください：

| プレースホルダー | 置換内容 |
|-----------------|---------|
| `{{TITLE}}` | 記事タイトル |
| `{{DESCRIPTION}}` | メタディスクリプション（120文字程度） |
| `{{SLUG}}` | 記事スラッグ（例: `2026-01-21-store-website-necessity`） |
| `{{DATE}}` | 公開日（YYYY-MM-DD形式） |
| `{{DATE_DISPLAY}}` | 表示用日付（YYYY.MM.DD形式） |
| `{{CONTENT}}` | 記事本文（HTMLタグで記述） |

### 5.7 Q&Aボックスのスタイル

相談事例風のQ&Aを入れる場合は以下のHTMLを使用：

```html
<div class="qa-box">
    <div class="qa-question">
        <span>質問内容をここに記述</span>
    </div>
    <div class="qa-answer">
        <span>回答内容をここに記述</span>
    </div>
</div>
```

### 5.8 図解画像の挿入

図解画像を記事内に挿入する場合：

```html
<img src="../blog/images/{SLUG}_diagram.jpg" 
     alt="図解の説明" 
     class="article-diagram">
```

---

## Step 6: データ同期

### 6.1 同期スクリプトの実行

```bash
cd /Users/game_gct/Miakiss_Web
python3 scripts/sync_blog_data.py
```

### 6.2 同期される内容

このスクリプトは以下を自動で行います：

1. `blog/` ディレクトリ内のHTMLファイルをスキャン
2. HTMLのメタタグから記事情報を抽出
3. `blog/published_articles.json` に新記事を追加
4. `blog/used_keywords.json` を更新
5. `blog/published_articles.js` を生成

### 6.3 成功メッセージ

```
✅ 同期完了
📊 記事数: XX件
```

---

## Step 7: Git コミット＆プッシュ

### 7.1 コミット

```bash
cd /Users/game_gct/Miakiss_Web
git add blog/
git commit -m "📝 新記事追加: {記事タイトル}（{YYYY-MM-DD}）"
```

### 7.2 プッシュ

```bash
git push
```

### 7.3 SSL証明書エラーが発生した場合

サンドボックス制限でプッシュに失敗した場合は、`required_permissions: ["all"]` を指定して再実行してください。

---

## 完了報告

すべてのステップが完了したら、以下の形式でユーザーに報告してください：

```markdown
## ✅ ブログ記事作成ワークフロー完了

本日の記事作成が完了しました！

---

### 📄 作成した記事

| 項目 | 内容 |
|------|------|
| **タイトル** | {記事タイトル} |
| **ファイル** | `blog/{YYYY-MM-DD}-{slug}.html` |
| **キーワードID** | {ID}（{キーワード}） |
| **カテゴリ** | {カテゴリ} |
| **文字数** | 約X,XXX文字 |

---

### 🖼️ 圧縮済み画像

| 画像 | サイズ |
|------|--------|
| ヘッダー画像 | XX.XKB |
| 図解画像 | XX.XKB |
| サムネイル画像 | XX.XKB |

---

### 📊 実行したステップ

1. ✅ `keywords.json` からテーマ選択（ID: XX）
2. ✅ Freepik用画像プロンプト提示
3. ✅ ユーザーが画像生成・保存
4. ✅ `scripts/compress_images.py` で画像圧縮（PNG→JPG）
5. ✅ HTML記事生成（Markdown記法なし、HTMLタグのみ使用）
6. ✅ `scripts/sync_blog_data.py` でデータ同期（記事数: XX件）
7. ✅ `git commit && git push` でデプロイ完了

---

記事がサイトに反映されました！🎉
```

---

## トラブルシューティング

### Q: 画像圧縮スクリプトでエラーが出る

**原因**: Pillowライブラリがインストールされていない

**解決策**:
```bash
pip3 install Pillow
```

### Q: PNG画像が見つからないエラー

**原因**: ファイル名が正しくない、または保存先が間違っている

**解決策**:
1. ファイル名が `{YYYY-MM-DD}-{slug}_header.png` 形式か確認
2. 保存先が `blog/images/` か確認

### Q: Git プッシュでSSL証明書エラー

**原因**: サンドボックス制限

**解決策**: `required_permissions: ["all"]` を指定して再実行

### Q: 同期スクリプトで「新しい記事はありません」と表示される

**原因**: 
- HTMLファイルが正しく保存されていない
- メタタグ（title, datePublished）が正しく設定されていない

**解決策**:
1. HTMLファイルが `blog/` に存在するか確認
2. `<title>` タグと `application/ld+json` の `datePublished` が設定されているか確認

---

## 関連ファイル一覧

```
Miakiss_Web/
├── .cursorrules                      # Cursorルール（簡易版）
├── BLOG_WORKFLOW.md                  # このファイル
├── blog/
│   ├── keywords.json                 # キーワードマスター
│   ├── used_keywords.json            # 使用済みキーワード
│   ├── article_template.html         # 記事テンプレート
│   ├── published_articles.json       # 公開済み記事データ
│   ├── published_articles.js         # JS用記事データ
│   ├── images/                       # 記事用画像
│   └── {YYYY-MM-DD}-{slug}.html      # 記事HTMLファイル
└── scripts/
    ├── compress_images.py            # 画像圧縮スクリプト
    └── sync_blog_data.py             # データ同期スクリプト
```

---

## 更新履歴

- **2026-01-21**: 初版作成
