<?php
// お問い合わせフォーム設定ファイル
// 
// セキュリティ注意: 機密情報は環境変数で管理してください
// エックスサーバーの場合: .htaccess に SetEnv で設定

// メール設定
define('ADMIN_EMAIL', 'info@miakiss.com'); // 管理者メールアドレス
define('FROM_EMAIL', 'info@miakiss.com'); // 送信元メールアドレス
define('COMPANY_NAME', '株式会社ミアキス');
define('SITE_URL', 'https://miakiss.com'); // サイトURL

// SMTP設定（エックスサーバー用設定）
define('SMTP_HOST', 'localhost');
define('SMTP_PORT', 587);
define('SMTP_USERNAME', ''); // エックスサーバーでは通常不要
define('SMTP_PASSWORD', ''); // エックスサーバーでは通常不要
define('SMTP_SECURE', 'tls'); // tls または ssl

// セキュリティ設定
define('CSRF_TOKEN_NAME', 'csrf_token');
define('SESSION_TIMEOUT', 3600); // 1時間

// reCAPTCHA v3 設定（環境変数から取得、なければデフォルト値を使用）
// 本番環境では .htaccess で SetEnv を使用して設定することを推奨
define('RECAPTCHA_SITE_KEY', getenv('RECAPTCHA_SITE_KEY') ?: '6LfRFFAsAAAAALVIl9P5l4o55mrpJcwrlNB5l7HH');
define('RECAPTCHA_SECRET_KEY', getenv('RECAPTCHA_SECRET_KEY') ?: '6LfRFFAsAAAAALfvUUaAMP5TZ3BM0o9hlXRwk0_4');
define('RECAPTCHA_SCORE_THRESHOLD', 0.5); // スコア閾値（0.0-1.0、低いほどボットの可能性が高い）
define('RECAPTCHA_VERIFY_URL', 'https://www.google.com/recaptcha/api/siteverify');

// スパム対策設定
define('MAX_SUBMISSIONS_PER_HOUR', 10); // 1時間あたりの最大送信数
define('HONEYPOT_FIELD', 'website'); // ハニーポットフィールド名

// ログ設定
define('LOG_DIR', __DIR__ . '/../logs/');
define('CONTACT_LOG', LOG_DIR . 'contact.log');
define('ERROR_LOG', LOG_DIR . 'error.log');

// 許可する文字数
define('MAX_NAME_LENGTH', 100);
define('MAX_EMAIL_LENGTH', 255);
define('MAX_MESSAGE_LENGTH', 2000);

// 禁止ワード（スパム対策）
$forbidden_words = [
    'viagra', 'casino', 'lottery', 'winner', 'congratulations',
    'click here', 'free money', 'make money', 'work from home'
];

// ログディレクトリの作成
if (!is_dir(LOG_DIR)) {
    mkdir(LOG_DIR, 0755, true);
}
?> 