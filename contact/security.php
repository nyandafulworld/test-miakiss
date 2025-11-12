<?php
// セキュリティ処理クラス

class SecurityHelper {
    
    /**
     * CSRFトークンを生成
     */
    public static function generateCSRFToken() {
        if (session_status() == PHP_SESSION_NONE) {
            session_start();
        }
        
        $token = bin2hex(random_bytes(32));
        $_SESSION[CSRF_TOKEN_NAME] = $token;
        $_SESSION['csrf_time'] = time();
        
        return $token;
    }
    
    /**
     * CSRFトークンを検証
     */
    public static function validateCSRFToken($token) {
        if (session_status() == PHP_SESSION_NONE) {
            session_start();
        }
        
        // トークンの存在確認
        if (!isset($_SESSION[CSRF_TOKEN_NAME]) || !isset($_SESSION['csrf_time'])) {
            return false;
        }
        
        // タイムアウト確認
        if (time() - $_SESSION['csrf_time'] > SESSION_TIMEOUT) {
            unset($_SESSION[CSRF_TOKEN_NAME]);
            unset($_SESSION['csrf_time']);
            return false;
        }
        
        // トークンの一致確認
        return hash_equals($_SESSION[CSRF_TOKEN_NAME], $token);
    }
    
    /**
     * 入力値をサニタイズ
     */
    public static function sanitize($input) {
        if (is_array($input)) {
            return array_map([self::class, 'sanitize'], $input);
        }
        
        return htmlspecialchars(trim($input), ENT_QUOTES, 'UTF-8');
    }
    
    /**
     * IPアドレスを取得
     */
    public static function getClientIP() {
        $ip_keys = ['HTTP_X_FORWARDED_FOR', 'HTTP_X_REAL_IP', 'HTTP_CLIENT_IP', 'REMOTE_ADDR'];
        
        foreach ($ip_keys as $key) {
            if (array_key_exists($key, $_SERVER) === true) {
                foreach (explode(',', $_SERVER[$key]) as $ip) {
                    $ip = trim($ip);
                    if (filter_var($ip, FILTER_VALIDATE_IP, FILTER_FLAG_NO_PRIV_RANGE | FILTER_FLAG_NO_RES_RANGE) !== false) {
                        return $ip;
                    }
                }
            }
        }
        
        return $_SERVER['REMOTE_ADDR'] ?? 'unknown';
    }
    
    /**
     * レート制限チェック
     */
    public static function checkRateLimit() {
        $ip = self::getClientIP();
        $current_hour = date('Y-m-d-H');
        $rate_file = LOG_DIR . "rate_limit_{$ip}_{$current_hour}.tmp";
        
        if (file_exists($rate_file)) {
            $count = (int)file_get_contents($rate_file);
            if ($count >= MAX_SUBMISSIONS_PER_HOUR) {
                return false;
            }
            $count++;
        } else {
            $count = 1;
        }
        
        file_put_contents($rate_file, $count);
        
        // 古いファイルを削除
        self::cleanupRateLimit();
        
        return true;
    }
    
    /**
     * 古いレート制限ファイルを削除
     */
    private static function cleanupRateLimit() {
        $files = glob(LOG_DIR . 'rate_limit_*.tmp');
        $current_time = time();
        
        foreach ($files as $file) {
            if ($current_time - filemtime($file) > 3600) { // 1時間以上前のファイルを削除
                unlink($file);
            }
        }
    }
    
    /**
     * ハニーポットチェック
     */
    public static function checkHoneypot($data) {
        return empty($data[HONEYPOT_FIELD]);
    }
    
    /**
     * 禁止ワードチェック
     */
    public static function checkForbiddenWords($text) {
        global $forbidden_words;
        
        $text_lower = strtolower($text);
        
        foreach ($forbidden_words as $word) {
            if (strpos($text_lower, strtolower($word)) !== false) {
                return false;
            }
        }
        
        return true;
    }
    
    /**
     * ログを記録
     */
    public static function log($message, $type = 'info') {
        $timestamp = date('Y-m-d H:i:s');
        $ip = self::getClientIP();
        $log_message = "[{$timestamp}] [{$type}] IP: {$ip} - {$message}" . PHP_EOL;
        
        $log_file = ($type === 'error') ? ERROR_LOG : CONTACT_LOG;
        file_put_contents($log_file, $log_message, FILE_APPEND | LOCK_EX);
    }
    
    /**
     * reCAPTCHA v3トークンを検証
     */
    public static function verifyRecaptcha($token) {
        if (empty($token)) {
            self::log('reCAPTCHAトークンが空です', 'warning');
            return [
                'success' => false,
                'score' => 0,
                'error' => 'reCAPTCHAトークンが見つかりません。'
            ];
        }
        
        // Google reCAPTCHA APIにリクエストを送信
        $post_data = http_build_query([
            'secret' => RECAPTCHA_SECRET_KEY,
            'response' => $token,
            'remoteip' => self::getClientIP()
        ]);
        
        $options = [
            'http' => [
                'header' => "Content-type: application/x-www-form-urlencoded\r\n",
                'method' => 'POST',
                'content' => $post_data,
                'timeout' => 10
            ]
        ];
        
        $context = stream_context_create($options);
        $response = @file_get_contents(RECAPTCHA_VERIFY_URL, false, $context);
        
        if ($response === false) {
            self::log('reCAPTCHA API接続エラー', 'error');
            return [
                'success' => false,
                'score' => 0,
                'error' => 'reCAPTCHA検証に失敗しました。'
            ];
        }
        
        $result = json_decode($response, true);
        
        if (!$result) {
            self::log('reCAPTCHA APIレスポンス解析エラー', 'error');
            return [
                'success' => false,
                'score' => 0,
                'error' => 'reCAPTCHA検証に失敗しました。'
            ];
        }
        
        $score = $result['score'] ?? 0;
        $success = $result['success'] ?? false;
        
        // ログに記録
        self::log("reCAPTCHA検証結果: success={$success}, score={$score}");
        
        // スコアが閾値未満の場合
        if (!$success || $score < RECAPTCHA_SCORE_THRESHOLD) {
            self::log("reCAPTCHA検証失敗: スコア {$score} が閾値 " . RECAPTCHA_SCORE_THRESHOLD . " 未満", 'warning');
            return [
                'success' => false,
                'score' => $score,
                'error' => 'ボット判定されました。正常にフォームを送信してください。'
            ];
        }
        
        return [
            'success' => true,
            'score' => $score,
            'error' => null
        ];
    }
}
?> 