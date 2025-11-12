# お問い合わせフォームシステム セットアップガイド

## 概要

HTMLサイト用の高機能お問い合わせフォームシステムです。Contact Form 7風の機能を独自のPHPバックエンドで実装しています。

## 機能

- ✅ **セキュリティ対策**
  - CSRFトークンによる不正送信防止
  - XSS攻撃対策
  - レート制限（連続送信防止）
  - ハニーポット（スパム対策）
  - 禁止ワードフィルター

- ✅ **メール機能**
  - 管理者宛通知メール（HTML形式）
  - お客様宛自動返信メール
  - 日本語対応

- ✅ **バリデーション**
  - サーバーサイド検証
  - リアルタイムエラー表示
  - 詳細なエラーメッセージ

- ✅ **ユーザビリティ**
  - Ajax送信（ページリロードなし）
  - ローディング表示
  - レスポンシブ対応

## システム要件

- **PHP**: 7.4以上
- **拡張モジュール**: mbstring, json
- **権限**: ログディレクトリへの書き込み権限
- **メール**: サーバーのメール送信機能（sendmail または SMTP）

## インストール手順

### 1. ファイル配置

プロジェクトルートに以下の構造でファイルを配置：

```
/
├── index.html
├── thanks.html
├── style.css
├── contact/
│   ├── config.php
│   ├── handler.php
│   ├── get_token.php
│   ├── security.php
│   ├── validation.php
│   ├── mail.php
│   └── test.php
└── logs/
    └── (自動作成)
```

### 2. 設定ファイルの編集

`contact/config.php` を編集して、以下の設定を変更：

```php
// メール設定（必須）
define('ADMIN_EMAIL', 'your-email@example.com'); // 実際のメールアドレス
define('FROM_EMAIL', 'noreply@example.com');     // 送信元アドレス
define('SITE_URL', 'https://your-site.com');    // サイトURL

// SMTP設定（サーバー環境に合わせて調整）
define('SMTP_HOST', 'localhost');
define('SMTP_PORT', 587);
// 必要に応じてSMTP認証情報を設定
```

### 3. ディレクトリ権限設定

```bash
# ログディレクトリの権限設定
chmod 755 logs/
chmod 644 logs/*.log
```

### 4. 動作テスト

テスト用スクリプトを実行：

```bash
# ブラウザで以下にアクセス
https://your-site.com/contact/test.php
```

## 設定項目詳細

### メール設定

| 項目 | 説明 | デフォルト値 |
|------|------|-------------|
| `ADMIN_EMAIL` | 管理者メールアドレス | info@miakiss.co.jp |
| `FROM_EMAIL` | 送信元メールアドレス | noreply@miakiss.co.jp |
| `COMPANY_NAME` | 会社名 | 株式会社ミアキス |
| `SITE_URL` | サイトURL | https://www.miakiss.co.jp |

### セキュリティ設定

| 項目 | 説明 | デフォルト値 |
|------|------|-------------|
| `MAX_SUBMISSIONS_PER_HOUR` | 1時間あたりの最大送信数 | 5 |
| `SESSION_TIMEOUT` | セッションタイムアウト（秒） | 3600 |
| `HONEYPOT_FIELD` | ハニーポットフィールド名 | website |

### バリデーション設定

| 項目 | 説明 | デフォルト値 |
|------|------|-------------|
| `MAX_NAME_LENGTH` | 名前の最大文字数 | 100 |
| `MAX_EMAIL_LENGTH` | メールアドレスの最大文字数 | 255 |
| `MAX_MESSAGE_LENGTH` | メッセージの最大文字数 | 2000 |

## トラブルシューティング

### メールが送信されない場合

1. **PHP設定確認**
   ```bash
   php -m | grep -E "(mbstring|iconv)"
   ```

2. **sendmail設定確認**
   ```bash
   php -i | grep sendmail_path
   ```

3. **ログ確認**
   ```bash
   tail -f logs/error.log
   ```

### CSRFトークンエラーが頻発する場合

- セッション設定を確認
- サーバーの時刻設定を確認
- SESSION_TIMEOUTの値を調整

### スパム送信が多い場合

- `MAX_SUBMISSIONS_PER_HOUR` を下げる
- `$forbidden_words` 配列にキーワードを追加
- IPアドレス制限を実装

## カスタマイズ

### 新しいフィールドを追加

1. HTMLフォームにフィールドを追加
2. `validation.php` にバリデーション処理を追加
3. `mail.php` のメール本文テンプレートを更新

### メール本文のカスタマイズ

`contact/mail.php` の以下のメソッドを編集：
- `getAdminMailBody()` - 管理者宛メール
- `getCustomerMailBody()` - お客様宛メール

### スタイルのカスタマイズ

`style.css` の「Contact Section」部分を編集。

## セキュリティ注意事項

1. **定期的なログ確認**
   - `logs/contact.log` で正常な送信を確認
   - `logs/error.log` でエラーを監視

2. **ファイル権限**
   - PHPファイルは 644 権限
   - ディレクトリは 755 権限
   - ログファイルは 644 権限

3. **定期メンテナンス**
   - 古いログファイルの削除
   - レート制限ファイルのクリーンアップ（自動実行）

## サポート

設定や運用でご不明な点がございましたら、以下までお問い合わせください：

- 技術サポート: [サポート連絡先]
- ドキュメント: このREADMEファイル
- ログ確認: `/logs/` ディレクトリ

---

**重要**: 本番環境での運用前に、必ずテスト環境で動作確認を行ってください。 