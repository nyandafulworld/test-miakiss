<?php
// お問い合わせフォームシステム テストファイル

// 設定ファイルの読み込み
require_once __DIR__ . '/config.php';
require_once __DIR__ . '/security.php';
require_once __DIR__ . '/validation.php';
require_once __DIR__ . '/mail.php';

?>
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>お問い合わせフォームシステム テスト</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.6; }
        .test-section { background: #f8f9fa; padding: 20px; margin: 20px 0; border-radius: 5px; }
        .success { color: #155724; background: #d4edda; border: 1px solid #c3e6cb; }
        .error { color: #721c24; background: #f8d7da; border: 1px solid #f5c6cb; }
        .info { color: #0c5460; background: #d1ecf1; border: 1px solid #bee5eb; }
        .warning { color: #856404; background: #fff3cd; border: 1px solid #ffeaa7; }
        pre { background: #f1f1f1; padding: 10px; border-radius: 3px; overflow-x: auto; }
        .button { background: #0D9488; color: white; padding: 10px 20px; border: none; border-radius: 3px; cursor: pointer; }
        .button:hover { background: #0F766E; }
    </style>
</head>
<body>
    <h1>🔧 お問い合わせフォームシステム テスト</h1>
    
    <div class="test-section info">
        <h2>📋 システム情報</h2>
        <ul>
            <li><strong>PHP バージョン:</strong> <?php echo PHP_VERSION; ?></li>
            <li><strong>現在時刻:</strong> <?php echo date('Y-m-d H:i:s'); ?></li>
            <li><strong>タイムゾーン:</strong> <?php echo date_default_timezone_get(); ?></li>
            <li><strong>ログディレクトリ:</strong> <?php echo LOG_DIR; ?></li>
        </ul>
    </div>

    <?php
    // テスト実行
    $tests = [];
    
    // 1. PHP拡張モジュールチェック
    $tests['mbstring'] = extension_loaded('mbstring');
    $tests['json'] = extension_loaded('json');
    
    // 2. ディレクトリ権限チェック
    $tests['log_dir_writable'] = is_writable(LOG_DIR);
    
    // 3. 設定値チェック
    $tests['admin_email_set'] = !empty(ADMIN_EMAIL) && ADMIN_EMAIL !== 'info@miakiss.co.jp';
    $tests['from_email_set'] = !empty(FROM_EMAIL);
    
    // 4. CSRFトークン生成テスト
    try {
        $csrf_token = SecurityHelper::generateCSRFToken();
        $tests['csrf_generation'] = !empty($csrf_token);
    } catch (Exception $e) {
        $tests['csrf_generation'] = false;
    }
    
    // 5. バリデーションテスト
    $validator = new ValidationHelper();
    $test_data = [
        'name' => 'テスト太郎',
        'email' => 'test@example.com',
        'message' => 'これはテストメッセージです。システムの動作確認を行っています。'
    ];
    $tests['validation'] = $validator->validateAll($test_data);
    
    // 6. メール設定テスト（実際には送信しない）
    $tests['mail_function'] = function_exists('mail') || function_exists('mb_send_mail');
    ?>
    
    <div class="test-section">
        <h2>🧪 テスト結果</h2>
        
        <h3>必須拡張モジュール</h3>
        <ul>
            <li>mbstring: <?php echo $tests['mbstring'] ? '<span class="success">✓ 利用可能</span>' : '<span class="error">✗ 未インストール</span>'; ?></li>
            <li>json: <?php echo $tests['json'] ? '<span class="success">✓ 利用可能</span>' : '<span class="error">✗ 未インストール</span>'; ?></li>
        </ul>
        
        <h3>ファイル権限</h3>
        <ul>
            <li>ログディレクトリ書き込み権限: <?php echo $tests['log_dir_writable'] ? '<span class="success">✓ 書き込み可能</span>' : '<span class="error">✗ 書き込み不可</span>'; ?></li>
        </ul>
        
        <h3>設定確認</h3>
        <ul>
            <li>管理者メールアドレス: <?php echo $tests['admin_email_set'] ? '<span class="success">✓ 設定済み</span>' : '<span class="warning">⚠ デフォルト値のまま</span>'; ?></li>
            <li>送信元メールアドレス: <?php echo $tests['from_email_set'] ? '<span class="success">✓ 設定済み</span>' : '<span class="error">✗ 未設定</span>'; ?></li>
        </ul>
        
        <h3>機能テスト</h3>
        <ul>
            <li>CSRFトークン生成: <?php echo $tests['csrf_generation'] ? '<span class="success">✓ 正常</span>' : '<span class="error">✗ エラー</span>'; ?></li>
            <li>バリデーション機能: <?php echo $tests['validation'] ? '<span class="success">✓ 正常</span>' : '<span class="error">✗ エラー</span>'; ?></li>
            <li>メール関数: <?php echo $tests['mail_function'] ? '<span class="success">✓ 利用可能</span>' : '<span class="error">✗ 利用不可</span>'; ?></li>
        </ul>
    </div>
    
    <div class="test-section">
        <h2>📧 メール送信テスト</h2>
        
        <?php if (isset($_POST['test_mail'])): ?>
            <div class="test-section">
                <?php
                try {
                    $result = MailHelper::testMailConfiguration();
                    if ($result) {
                        echo '<div class="success"><strong>✓ メール送信テスト成功</strong><br>管理者メールアドレス (' . ADMIN_EMAIL . ') にテストメールを送信しました。</div>';
                    } else {
                        echo '<div class="error"><strong>✗ メール送信テスト失敗</strong><br>メール設定またはサーバー設定をご確認ください。</div>';
                    }
                } catch (Exception $e) {
                    echo '<div class="error"><strong>✗ メール送信エラー</strong><br>' . htmlspecialchars($e->getMessage()) . '</div>';
                }
                ?>
            </div>
        <?php endif; ?>
        
        <form method="POST">
            <p>実際にテストメールを送信して動作確認を行います。</p>
            <button type="submit" name="test_mail" class="button">📧 テストメール送信</button>
        </form>
        
        <div class="warning">
            <strong>注意:</strong> このテストを実行すると、設定された管理者メールアドレス (<?php echo ADMIN_EMAIL; ?>) にテストメールが送信されます。
        </div>
    </div>
    
    <div class="test-section">
        <h2>📊 現在の設定値</h2>
        <pre><?php
echo "管理者メール: " . ADMIN_EMAIL . "\n";
echo "送信元メール: " . FROM_EMAIL . "\n";
echo "会社名: " . COMPANY_NAME . "\n";
echo "サイトURL: " . SITE_URL . "\n";
echo "最大送信回数/時: " . MAX_SUBMISSIONS_PER_HOUR . "\n";
echo "セッションタイムアウト: " . SESSION_TIMEOUT . "秒\n";
echo "名前最大文字数: " . MAX_NAME_LENGTH . "\n";
echo "メール最大文字数: " . MAX_EMAIL_LENGTH . "\n";
echo "メッセージ最大文字数: " . MAX_MESSAGE_LENGTH . "\n";
        ?></pre>
    </div>
    
    <div class="test-section">
        <h2>📝 ログファイル確認</h2>
        
        <h3>お問い合わせログ</h3>
        <?php
        if (file_exists(CONTACT_LOG)) {
            $log_content = file_get_contents(CONTACT_LOG);
            if (!empty($log_content)) {
                echo '<pre>' . htmlspecialchars(substr($log_content, -1000)) . '</pre>';
            } else {
                echo '<p class="info">ログファイルは空です。</p>';
            }
        } else {
            echo '<p class="warning">ログファイルが見つかりません。最初のお問い合わせ送信時に作成されます。</p>';
        }
        ?>
        
        <h3>エラーログ</h3>
        <?php
        if (file_exists(ERROR_LOG)) {
            $error_content = file_get_contents(ERROR_LOG);
            if (!empty($error_content)) {
                echo '<pre>' . htmlspecialchars(substr($error_content, -1000)) . '</pre>';
            } else {
                echo '<p class="success">エラーログは空です。</p>';
            }
        } else {
            echo '<p class="info">エラーログファイルがありません。</p>';
        }
        ?>
    </div>
    
    <?php
    // 総合判定
    $all_critical_passed = $tests['mbstring'] && $tests['json'] && $tests['log_dir_writable'] && $tests['from_email_set'] && $tests['csrf_generation'] && $tests['validation'] && $tests['mail_function'];
    ?>
    
    <div class="test-section <?php echo $all_critical_passed ? 'success' : 'error'; ?>">
        <h2>🎯 総合判定</h2>
        <?php if ($all_critical_passed): ?>
            <p><strong>✓ システムは正常に動作する準備ができています！</strong></p>
            <p>次のステップ:</p>
            <ol>
                <li>設定ファイル（config.php）で管理者メールアドレスを本番用に変更</li>
                <li>メール送信テストを実行</li>
                <li>フォームページで実際の送信テストを実行</li>
            </ol>
        <?php else: ?>
            <p><strong>✗ 設定に問題があります</strong></p>
            <p>上記のエラー項目を修正してから再度テストを実行してください。</p>
        <?php endif; ?>
    </div>
    
    <div class="test-section info">
        <h2>🔗 リンク</h2>
        <ul>
            <li><a href="../index.html#contact">お問い合わせフォーム</a></li>
            <li><a href="README.md">セットアップガイド</a></li>
            <li><a href="?refresh=1">このページを再読み込み</a></li>
        </ul>
    </div>
    
    <footer style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #dee2e6; text-align: center; color: #6c757d;">
        <p>お問い合わせフォームシステム テストページ</p>
        <p>最終更新: <?php echo date('Y-m-d H:i:s'); ?></p>
    </footer>
</body>
</html> 