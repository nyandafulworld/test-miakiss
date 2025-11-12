<?php
// 簡易デバッグ用ファイル
header('Content-Type: text/plain; charset=utf-8');

echo "=== デバッグ情報 ===\n";
echo "現在時刻: " . date('Y-m-d H:i:s') . "\n";
echo "PHP Version: " . PHP_VERSION . "\n";
echo "ドキュメントルート: " . $_SERVER['DOCUMENT_ROOT'] . "\n";
echo "現在のディレクトリ: " . __DIR__ . "\n";

echo "\n=== ファイル存在確認 ===\n";
$files = ['config.php', 'handler.php', 'get_token.php', 'security.php', 'validation.php', 'mail.php'];
foreach ($files as $file) {
    echo $file . ": " . (file_exists(__DIR__ . '/' . $file) ? "存在" : "なし") . "\n";
}

echo "\n=== 設定ファイル読み込みテスト ===\n";
try {
    require_once __DIR__ . '/config.php';
    echo "config.php: 読み込み成功\n";
    echo "ADMIN_EMAIL: " . ADMIN_EMAIL . "\n";
    echo "SITE_URL: " . SITE_URL . "\n";
} catch (Exception $e) {
    echo "config.php: エラー - " . $e->getMessage() . "\n";
}

echo "\n=== CSRFトークン生成テスト ===\n";
try {
    session_start();
    require_once __DIR__ . '/security.php';
    $token = SecurityHelper::generateCSRFToken();
    echo "CSRFトークン生成: 成功\n";
    echo "トークン: " . substr($token, 0, 20) . "...\n";
} catch (Exception $e) {
    echo "CSRFトークン生成: エラー - " . $e->getMessage() . "\n";
}

echo "\n=== リクエスト情報 ===\n";
echo "REQUEST_METHOD: " . $_SERVER['REQUEST_METHOD'] . "\n";
echo "HTTP_HOST: " . $_SERVER['HTTP_HOST'] . "\n";
echo "REQUEST_URI: " . $_SERVER['REQUEST_URI'] . "\n";

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    echo "\n=== POST データ ===\n";
    print_r($_POST);
}
?> 