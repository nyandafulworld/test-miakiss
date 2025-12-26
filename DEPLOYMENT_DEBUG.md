# デプロイデバッグガイド

## 現在の状況

2025-12-17の記事（Googleアナリティクス）が本番サイトに反映されていません。

## 実施した対応

### 1. published_articles.js の同期
```bash
✅ sync_blog_data.py を実行
✅ published_articles.js に記事を追加
✅ Git コミット & プッシュ完了
```

### 2. GitHub Actions のトリガー
```bash
✅ 空のコミットで強制トリガー (69912f8)
✅ デバッグログを追加 (5895928)
```

### 3. 確認手順

**ステップ1: GitHub Actions の実行を確認**

1. 以下のURLを開く：
   ```
   https://github.com/nyandafulworld/test-miakiss/actions
   ```

2. 最新の2つのワークフロー実行を確認：
   - `Trigger deployment: Force FTP sync` (69912f8)
   - `Debug: Add verbose logging` (5895928)

3. ステータスを確認：
   - ✅ 緑のチェックマーク = 成功
   - 🔄 黄色の丸 = 実行中
   - ❌ 赤のX = 失敗

**ステップ2: ログを確認**

失敗している場合、ワークフロー実行をクリックして詳細を確認：

1. "Deploy to FTP Server" ジョブをクリック
2. 各ステップのログを展開
3. 特に以下を確認：
   - "Show files to be deployed" - ファイルが存在するか
   - "Deploy to FTP server" - FTP接続とアップロードが成功しているか

## 考えられる問題と対処法

### 問題1: GitHub Actions が実行されていない

**症状**: Actionsページにワークフロー実行が表示されない

**原因**:
- GitHub Actions が無効になっている
- ワークフローファイルに構文エラーがある

**対処法**:
1. リポジトリ設定で Actions を有効化
   - Settings > Actions > General > "Allow all actions and reusable workflows"
2. YAML構文エラーをチェック

### 問題2: GitHub Actions が失敗している

**症状**: 赤いX マーク

**考えられる原因**:

#### A. FTP接続エラー
```
Error: Failed to connect to FTP server
```
**対処法**:
- GitHub Secrets (FTP_SERVER, FTP_USERNAME, FTP_PASSWORD) を確認
- FTPサーバーがアクセス可能か確認
- ファイアウォール設定を確認

#### B. 認証エラー
```
Error: Authentication failed
```
**対処法**:
- FTP_USERNAME と FTP_PASSWORD が正しいか確認
- パスワードに特殊文字が含まれる場合、エスケープを確認

#### C. パーミッションエラー
```
Error: Permission denied
```
**対処法**:
- FTPユーザーに書き込み権限があるか確認
- `server-dir` が正しいディレクトリを指しているか確認

### 問題3: デプロイは成功しているがファイルが反映されない

**症状**: GitHub Actions は緑のチェックマークだが、サイトに反映されない

**考えられる原因**:

#### A. server-dir の設定が間違っている

現在の設定:
```yaml
server-dir: /
```

**確認方法**:
FTPクライアントで接続して、正しいディレクトリ構造を確認：
- `public_html/` なのか
- `www/` なのか
- `httpdocs/` なのか
- `/` (ルート) なのか

**対処法**:
正しいディレクトリを `.github/workflows/deploy.yml` の `server-dir` に設定

#### B. キャッシュの問題

**対処法**:
1. ブラウザのキャッシュをクリア (Ctrl+Shift+Del / Cmd+Shift+Del)
2. プライベートブラウジングで確認
3. 別のデバイスで確認
4. CDNキャッシュをクリア（使用している場合）

#### C. FTP同期の差分検出問題

FTP-Deploy-Action は `.ftp-deploy-sync-state.json` で差分を管理しています。

**対処法**:
ワークフローに以下を追加してフルデプロイを強制：

```yaml
- name: Deploy to FTP server
  uses: SamKirkland/FTP-Deploy-Action@v4.3.5
  with:
    server: ${{ secrets.FTP_SERVER }}
    username: ${{ secrets.FTP_USERNAME }}
    password: ${{ secrets.FTP_PASSWORD }}
    server-dir: /
    dangerous-clean-slate: true  # ← フルデプロイを強制
```

**⚠️ 注意**: `dangerous-clean-slate: true` はサーバー上のファイルをすべて削除してから再アップロードするため、本番環境では慎重に使用してください。

### 問題4: 特定のファイルが除外されている

**症状**: 一部のファイルだけがデプロイされない

**原因**: `exclude` パターンに一致している

**現在の除外設定**:
```yaml
exclude: |
  **/.git*
  **/node_modules/**
  **/scripts/**
  **/.env
  **/.DS_Store
  **/README.md
  **/*.md
  **/requirements.txt
  **/test_server.py
  **/.cursor/**
  **/image_backup/**
```

**確認方法**:
デバッグログ (Show files to be deployed) で確認

**対処法**:
除外パターンから該当ファイルを削除

## 次のアクション

1. **GitHub Actions のログを確認**:
   - https://github.com/nyandafulworld/test-miakiss/actions
   - 最新2つの実行ログを確認

2. **ログの内容を報告**:
   - エラーメッセージがあればコピー
   - "Show files to be deployed" の出力を確認

3. **FTPサーバーの確認**:
   - 正しい `server-dir` を確認
   - ファイルが実際にアップロードされているか確認

4. **キャッシュクリア**:
   - ブラウザキャッシュをクリア
   - プライベートブラウジングで再確認

## 緊急対応：手動デプロイ

GitHub Actions が解決できない場合、FTPクライアントで手動デプロイ：

**デプロイするファイル**:
```
blog/2025-12-17-analytics.html
blog/images/2025-12-17-analytics_header.jpg
blog/images/2025-12-17-analytics_thumbnail.jpg
blog/published_articles.js  ← 特に重要！
blog/published_articles.json
sitemap.xml
```

**FTP接続情報**:
GitHub Secrets に設定されている情報を使用

---

**作成日**: 2025-12-17  
**最終更新**: 2025-12-17

















