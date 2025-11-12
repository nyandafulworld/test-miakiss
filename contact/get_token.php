<?php
// CSRFトークン取得API

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
} catch (Exception $e) {
    echo json_encode([
        'success' => false,
        'message' => 'システムエラーが発生しました。'
    ], JSON_UNESCAPED_UNICODE);
    exit;
}

// GETのみ許可
if ($_SERVER['REQUEST_METHOD'] !== 'GET') {
    http_response_code(405);
    echo json_encode([
        'success' => false,
        'message' => '不正なリクエストです。'
    ], JSON_UNESCAPED_UNICODE);
    exit;
}

try {
    // CSRFトークンを生成
    $token = SecurityHelper::generateCSRFToken();
    
    echo json_encode([
        'success' => true,
        'csrf_token' => $token
    ], JSON_UNESCAPED_UNICODE);
    
} catch (Exception $e) {
    SecurityHelper::log("CSRFトークン生成エラー: " . $e->getMessage(), 'error');
    
    http_response_code(500);
    echo json_encode([
        'success' => false,
        'message' => 'トークンの生成に失敗しました。'
    ], JSON_UNESCAPED_UNICODE);
}
?> 