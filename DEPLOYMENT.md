# デプロイメントガイド

このドキュメントでは、GitHub Actionsを使った自動デプロイの設定方法を説明します。

## 📋 前提条件

- GitHubアカウント
- 本番サーバー（SSH接続可能）
- サーバーにrsyncがインストールされていること

## 🔧 セットアップ手順

### 1. SSH鍵ペアの生成（未作成の場合）

ローカルマシンまたは本番サーバーで以下を実行:

```bash
ssh-keygen -t ed25519 -C "github-actions@miakiss.co.jp" -f ~/.ssh/github_actions_miakiss
```

- パスフレーズは空欄でOK（GitHub Actionsで使用するため）

### 2. 公開鍵をサーバーに登録

```bash
# 公開鍵の内容を確認
cat ~/.ssh/github_actions_miakiss.pub

# サーバーに登録
ssh user@your-server.com
mkdir -p ~/.ssh
echo "公開鍵の内容" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
chmod 700 ~/.ssh
exit
```

### 3. GitHub Secretsの設定

GitHubリポジトリページで以下の手順で設定:

1. **Settings** タブをクリック
2. 左メニューの **Secrets and variables** > **Actions** をクリック
3. **New repository secret** をクリック
4. 以下の4つのSecretを追加:

#### `SSH_PRIVATE_KEY`
```bash
# 秘密鍵の内容をコピー
cat ~/.ssh/github_actions_miakiss
```
**内容全体**（`-----BEGIN OPENSSH PRIVATE KEY-----`から`-----END OPENSSH PRIVATE KEY-----`まで）をコピーしてGitHubのSecretに貼り付け

#### `SERVER_HOST`
サーバーのホスト名またはIPアドレス
```
例: miakiss.co.jp
または: 123.45.67.89
```

#### `SERVER_USER`
サーバーのSSHユーザー名
```
例: miakiss
または: www-data
```

#### `SERVER_PATH`
Webサイトのルートディレクトリ
```
例: /var/www/miakiss.co.jp
または: /home/miakiss/public_html
```

### 4. サーバー側の準備

サーバーにログインして、デプロイ先ディレクトリを作成:

```bash
ssh user@your-server.com
sudo mkdir -p /var/www/miakiss.co.jp
sudo chown user:user /var/www/miakiss.co.jp
exit
```

## 🚀 デプロイ方法

### 自動デプロイ

`master`ブランチにプッシュすると自動的にデプロイされます:

```bash
git add .
git commit -m "変更内容"
git push origin master
```

### 手動デプロイ

GitHubリポジトリページで:

1. **Actions** タブをクリック
2. 左メニューの **Deploy to Production** をクリック
3. **Run workflow** ボタンをクリック
4. ブランチを選択して **Run workflow** を実行

## 📊 デプロイの確認

### GitHub Actionsでの確認

1. リポジトリの **Actions** タブを開く
2. 最新のワークフロー実行をクリック
3. **deploy** ジョブをクリックして詳細を確認

### サーバーでの確認

```bash
ssh user@your-server.com
cd /var/www/miakiss.co.jp
ls -la
```

## 🔍 トラブルシューティング

### SSH接続エラー

```
Permission denied (publickey)
```

**対処法:**
1. サーバーの`~/.ssh/authorized_keys`に公開鍵が正しく登録されているか確認
2. GitHub Secretsの`SSH_PRIVATE_KEY`が正しいか確認
3. 秘密鍵の改行コードが崩れていないか確認

### rsyncエラー

```
rsync: failed to connect to server
```

**対処法:**
1. `SERVER_HOST`が正しいか確認
2. サーバーのファイアウォールでSSH（ポート22）が開いているか確認
3. サーバー側でrsyncがインストールされているか確認: `which rsync`

### パス権限エラー

```
rsync: mkdir failed: Permission denied
```

**対処法:**
1. デプロイ先ディレクトリの所有者・権限を確認
2. ユーザーに書き込み権限があるか確認:
```bash
sudo chown -R user:user /var/www/miakiss.co.jp
sudo chmod -R 755 /var/www/miakiss.co.jp
```

## 🛡 セキュリティベストプラクティス

1. **SSH鍵の管理**
   - GitHub Actions専用の鍵ペアを使用
   - パスフレーズなしの鍵を使用（GitHub Secretsに保存するため）
   - 鍵はローカルに保管せず、作成後すぐにGitHub Secretsに登録

2. **最小権限の原則**
   - デプロイ用のユーザーはWebディレクトリへの書き込み権限のみ
   - `sudo`権限は付与しない

3. **機密情報の管理**
   - `.env`ファイルはGitにコミットしない
   - サーバー側で直接`.env`を作成・管理
   - `contact/config.php`などの設定ファイルも除外リストに追加

## 📝 除外ファイル

以下のファイル・ディレクトリは自動的にデプロイから除外されます:

- `.git/`
- `.github/`
- `node_modules/`
- `__pycache__/`
- `.DS_Store`
- `.env`
- `requirements.txt`
- `scripts/`
- `test_server.py`
- `*.md`（ドキュメントファイル）
- `assets/`（開発用アセット）

## 🔄 ロールバック

問題が発生した場合、以前のコミットに戻す:

```bash
# 履歴を確認
git log --oneline

# 特定のコミットに戻す
git revert <commit-hash>
git push origin master

# または強制的に戻す（注意: 履歴が書き換わります）
git reset --hard <commit-hash>
git push -f origin master
```

## 📞 サポート

デプロイに関する問題が解決しない場合は、GitHub Issuesで報告してください。




