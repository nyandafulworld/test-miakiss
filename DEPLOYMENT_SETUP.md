# デプロイ自動化セットアップガイド

## 概要

GitHub Actions を使用して、`git push` するだけで本番サーバーに自動デプロイされるシステムです。

## セットアップ手順

### 1. GitHub Secretsの設定

GitHubリポジトリで以下のSecretsを設定する必要があります。

#### 設定方法

1. GitHubリポジトリ（https://github.com/nyandafulworld/test-miakiss）にアクセス
2. **Settings** タブをクリック
3. 左サイドバーから **Secrets and variables** > **Actions** を選択
4. **New repository secret** ボタンをクリック
5. 以下の3つのSecretを追加：

#### 必要なSecrets

| Secret名 | 説明 | 例 |
|---------|------|---|
| `FTP_SERVER` | FTPサーバーのホスト名 | `ftp.miakiss.co.jp` |
| `FTP_USERNAME` | FTPユーザー名 | `miakiss_user` |
| `FTP_PASSWORD` | FTPパスワード | `your_password_here` |

### 2. GitHub Actionsワークフローの確認

`.github/workflows/deploy.yml` が作成されていることを確認：

```yaml
name: Deploy to Production via FTP

on:
  push:
    branches:
      - master
  workflow_dispatch:
```

このワークフローは以下のタイミングで実行されます：

- `master`ブランチに`push`された時
- GitHub UI から手動実行した時

### 3. デプロイの流れ

```mermaid
flowchart LR
    A[git push origin master] --> B[GitHub Actions起動]
    B --> C[コードをチェックアウト]
    C --> D[FTP Deploy Action実行]
    D --> E[本番サーバーにアップロード]
    E --> F[デプロイ完了]
```

#### 除外ファイル

以下のファイル・ディレクトリはデプロイ時に除外されます：

- `.git*` - Git関連ファイル
- `node_modules/` - Node.jsパッケージ
- `scripts/` - Pythonスクリプト
- `.env` - 環境変数ファイル
- `.DS_Store` - macOSシステムファイル
- `README.md`, `*.md` - ドキュメント
- `requirements.txt` - Python依存関係
- `test_server.py` - テストサーバー
- `.cursor/` - Cursorエディタ設定
- `image_backup/` - 画像バックアップ

### 4. デプロイの実行

#### 自動デプロイ（推奨）

```bash
# 記事作成後、デプロイスクリプトを実行
python3 scripts/deploy_article.py "2025-12-17-analytics" "Add new article"

# スクリプトが自動的に以下を実行：
# 1. git add
# 2. git commit
# 3. git push
# 4. GitHub Actions起動 → FTPデプロイ
```

#### 手動デプロイ

```bash
# ファイルを追加
git add blog/2025-12-17-analytics.html \
        blog/images/2025-12-17-analytics_header.jpg \
        blog/images/2025-12-17-analytics_thumbnail.jpg \
        blog/published_articles.json \
        sitemap.xml

# コミット
git commit -m "Add new blog article"

# プッシュ（これでGitHub Actionsが起動）
git push origin master
```

### 5. デプロイ状況の確認

#### GitHub Actions画面で確認

1. GitHubリポジトリの **Actions** タブを開く
2. 最新のワークフロー実行を確認
3. 緑のチェックマーク ✅ = 成功
4. 赤の×マーク ❌ = 失敗（ログを確認）

#### デプロイ時間

- **所要時間**: 約1-2分
- **タイムアウト**: 10分（それ以上かかる場合は失敗）

### 6. トラブルシューティング

#### デプロイが失敗する場合

**1. FTP接続エラー**

```
Error: Failed to connect to FTP server
```

**解決策**:
- GitHub SecretsのFTP_SERVER, FTP_USERNAME, FTP_PASSWORDが正しいか確認
- FTPサーバーがアクセス可能か確認
- IPアドレス制限がある場合は、GitHub Actionsの IP レンジを許可

**2. 認証エラー**

```
Error: Authentication failed
```

**解決策**:
- FTP_USERNAMEとFTP_PASSWORDが正しいか確認
- パスワードに特殊文字が含まれる場合、エスケープが必要な場合あり

**3. 権限エラー**

```
Error: Permission denied
```

**解決策**:
- FTPユーザーに書き込み権限があるか確認
- `server-dir` の設定が正しいか確認（現在は `/`）

#### GitHub Actionsのログを確認

```bash
# GitHub CLIを使用（インストール済みの場合）
gh run list
gh run view <run-id> --log
```

または、GitHub UI の Actions タブから確認。

### 7. セキュリティ上の注意

#### Secretsの管理

- **絶対にコードにパスワードを含めない**
- Secretsは GitHub UI でのみ設定
- `.env` ファイルは `.gitignore` で除外済み

#### アクセス制限

- 必要に応じて、FTPサーバー側でIP制限を設定
- GitHub Actions の IP レンジ: https://docs.github.com/en/actions/using-github-hosted-runners/about-github-hosted-runners#ip-addresses

### 8. 初回セットアップ確認

以下のチェックリストを確認：

- [ ] `.github/workflows/deploy.yml` が存在する
- [ ] GitHub Secretsに `FTP_SERVER` を設定
- [ ] GitHub Secretsに `FTP_USERNAME` を設定
- [ ] GitHub Secretsに `FTP_PASSWORD` を設定
- [ ] `git push` でGitHub Actionsが起動することを確認
- [ ] デプロイが成功することを確認（緑のチェックマーク）
- [ ] 本番サイトでファイルが更新されていることを確認

### 9. 手動デプロイ（GitHub UI）

GitHub Actionsを手動で実行する方法：

1. GitHubリポジトリの **Actions** タブを開く
2. 左サイドバーから **Deploy to Production via FTP** を選択
3. **Run workflow** ボタンをクリック
4. `master` ブランチを選択
5. **Run workflow** をクリック

### 10. 次回以降の使用方法

セットアップが完了したら、記事作成時は以下のコマンドだけで自動デプロイされます：

```bash
# ワークフロー全体（記事作成からデプロイまで）
python3 scripts/create_today_article.py  # キーワード選択
# AIが記事生成
# AIが画像取得
python3 scripts/deploy_article.py "<slug>" "<message>"  # 自動デプロイ
```

---

**最終更新**: 2025-12-17  
**ドキュメントバージョン**: 1.0

















