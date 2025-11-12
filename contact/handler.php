<?php
// メインのお問い合わせフォーム処理

// エラー表示を無効化
error_reporting(0);
ini_set('display_errors', 0);

// 出力バッファリング開始
ob_start();

session_start();

// JSON レスポンス用のヘッダー設定
header('Content-Type: application/json; charset=utf-8');

// 設定ファイルの読み込み
try {
    require_once __DIR__ . '/config.php';
    require_once __DIR__ . '/security.php';
    require_once __DIR__ . '/validation.php';
    require_once __DIR__ . '/mail.php';
} catch (Exception $e) {
    echo json_encode([
        'success' => false,
        'message' => 'システムエラーが発生しました。',
        'errors' => []
    ], JSON_UNESCAPED_UNICODE);
    exit;
}

// POST以外は拒否
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode([
        'success' => false,
        'message' => '不正なリクエストです。',
        'errors' => []
    ], JSON_UNESCAPED_UNICODE);
    exit;
}

try {
    // リクエストデータを取得
    $input_data = $_POST;
    
    // 入力データをサニタイズ
    $sanitized_data = SecurityHelper::sanitize($input_data);
    
    // CSRFトークンの検証
    $csrf_token = $sanitized_data['csrf_token'] ?? '';
    if (!SecurityHelper::validateCSRFToken($csrf_token)) {
        throw new Exception('セキュリティトークンが無効です。ページを再読み込みしてもう一度お試しください。');
    }
    
    // ハニーポットチェック
    if (!SecurityHelper::checkHoneypot($sanitized_data)) {
        SecurityHelper::log('ハニーポット検出', 'warning');
        throw new Exception('不正な送信を検出しました。');
    }
    
    // レート制限チェック
    if (!SecurityHelper::checkRateLimit()) {
        throw new Exception('送信回数が制限を超えています。しばらく時間をおいてから再度お試しください。');
    }
    
    // reCAPTCHA v3 検証
    $recaptcha_token = $sanitized_data['recaptcha_token'] ?? '';
    $recaptcha_result = SecurityHelper::verifyRecaptcha($recaptcha_token);
    
    if (!$recaptcha_result['success']) {
        throw new Exception($recaptcha_result['error']);
    }
    
    // バリデーション処理
    $validator = new ValidationHelper();
    if (!$validator->validateAll($sanitized_data)) {
        $errors = $validator->getErrors();
        http_response_code(400);
        echo json_encode([
            'success' => false,
            'message' => '入力内容に問題があります。',
            'errors' => $errors
        ], JSON_UNESCAPED_UNICODE);
        exit;
    }
    
    // フォームデータを取得
    $name = $sanitized_data['name'];
    $email = $sanitized_data['email'];
    $message = $sanitized_data['message'];
    
    // メール送信処理
    $admin_mail_sent = MailHelper::sendAdminMail($name, $email, $message);
    $customer_mail_sent = MailHelper::sendCustomerMail($name, $email, $message);
    
    if (!$admin_mail_sent) {
        SecurityHelper::log('管理者宛メール送信失敗', 'error');
        throw new Exception('お問い合わせの送信に失敗しました。しばらく時間をおいてから再度お試しください。');
    }
    
    // 成功ログ
    SecurityHelper::log("お問い合わせ送信成功: {$name} ({$email})");
    
    // レスポンス
    echo json_encode([
        'success' => true,
        'message' => $validator->getSuccessMessage(),
        'redirect' => 'thanks.html'
    ], JSON_UNESCAPED_UNICODE);
    
} catch (Exception $e) {
    // エラーハンドリング
    $error_message = $e->getMessage();
    
    // エラーログ
    SecurityHelper::log("お問い合わせエラー: {$error_message}", 'error');
    
    // エラーレスポンス
    http_response_code(400);
    echo json_encode([
        'success' => false,
        'message' => $error_message,
        'errors' => []
    ], JSON_UNESCAPED_UNICODE);
}

// CSRFトークンをクリア
if (isset($_SESSION[CSRF_TOKEN_NAME])) {
    unset($_SESSION[CSRF_TOKEN_NAME]);
    unset($_SESSION['csrf_time']);
}
?> 