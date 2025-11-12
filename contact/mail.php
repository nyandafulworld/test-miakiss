<?php
// メール送信処理クラス

class MailHelper {
    
    /**
     * 管理者宛のメールを送信
     */
    public static function sendAdminMail($name, $email, $message) {
        $subject = '[' . COMPANY_NAME . '] お問い合わせがありました';
        
        $body = self::getAdminMailBody($name, $email, $message);
        
        $headers = [
            'From: ' . FROM_EMAIL,
            'Reply-To: ' . $email,
            'X-Mailer: PHP/' . phpversion(),
            'Content-Type: text/html; charset=UTF-8',
            'Content-Transfer-Encoding: 8bit'
        ];
        
        return self::sendMail(ADMIN_EMAIL, $subject, $body, $headers);
    }
    
    /**
     * お客様宛の自動返信メールを送信
     */
    public static function sendCustomerMail($name, $email, $message) {
        $subject = '[' . COMPANY_NAME . '] お問い合わせを受け付けました';
        
        $body = self::getCustomerMailBody($name, $message);
        
        $headers = [
            'From: ' . FROM_EMAIL,
            'X-Mailer: PHP/' . phpversion(),
            'Content-Type: text/html; charset=UTF-8',
            'Content-Transfer-Encoding: 8bit'
        ];
        
        return self::sendMail($email, $subject, $body, $headers);
    }
    
    /**
     * メール送信の実行
     */
    private static function sendMail($to, $subject, $body, $headers) {
        try {
            // mb_send_mailを使用（日本語対応）
            mb_language('ja');
            mb_internal_encoding('UTF-8');
            
            $result = mb_send_mail(
                $to,
                $subject,
                $body,
                implode("\r\n", $headers)
            );
            
            if ($result) {
                SecurityHelper::log("メール送信成功: {$to}");
                return true;
            } else {
                SecurityHelper::log("メール送信失敗: {$to}", 'error');
                return false;
            }
            
        } catch (Exception $e) {
            SecurityHelper::log("メール送信エラー: " . $e->getMessage(), 'error');
            return false;
        }
    }
    
    /**
     * 管理者宛メールの本文を生成
     */
    private static function getAdminMailBody($name, $email, $message) {
        $timestamp = date('Y年m月d日 H:i:s');
        $ip = SecurityHelper::getClientIP();
        
        return "
<!DOCTYPE html>
<html>
<head>
    <meta charset=\"UTF-8\">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background-color: #007bff; color: white; padding: 20px; text-align: center; }
        .content { padding: 20px; background-color: #f8f9fa; }
        .field { margin-bottom: 15px; }
        .label { font-weight: bold; color: #495057; }
        .value { margin-left: 10px; }
        .footer { padding: 20px; text-align: center; font-size: 12px; color: #6c757d; }
    </style>
</head>
<body>
    <div class=\"container\">
        <div class=\"header\">
            <h2>" . COMPANY_NAME . "</h2>
            <p>お問い合わせフォームからの送信</p>
        </div>
        <div class=\"content\">
            <div class=\"field\">
                <span class=\"label\">お名前:</span>
                <span class=\"value\">" . htmlspecialchars($name, ENT_QUOTES, 'UTF-8') . "</span>
            </div>
            <div class=\"field\">
                <span class=\"label\">メールアドレス:</span>
                <span class=\"value\">" . htmlspecialchars($email, ENT_QUOTES, 'UTF-8') . "</span>
            </div>
            <div class=\"field\">
                <span class=\"label\">お問い合わせ内容:</span>
                <div class=\"value\" style=\"margin-top: 10px; padding: 15px; background-color: white; border-left: 3px solid #007bff;\">
                    " . nl2br(htmlspecialchars($message, ENT_QUOTES, 'UTF-8')) . "
                </div>
            </div>
            <hr>
            <div class=\"field\">
                <span class=\"label\">送信日時:</span>
                <span class=\"value\">{$timestamp}</span>
            </div>
            <div class=\"field\">
                <span class=\"label\">IPアドレス:</span>
                <span class=\"value\">{$ip}</span>
            </div>
        </div>
        <div class=\"footer\">
            <p>このメールは " . SITE_URL . " のお問い合わせフォームから自動送信されました。</p>
        </div>
    </div>
</body>
</html>
        ";
    }
    
    /**
     * お客様宛メールの本文を生成
     */
    private static function getCustomerMailBody($name, $message) {
        return "
<!DOCTYPE html>
<html>
<head>
    <meta charset=\"UTF-8\">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background-color: #007bff; color: white; padding: 20px; text-align: center; }
        .content { padding: 20px; }
        .message-box { background-color: #f8f9fa; padding: 15px; border-left: 3px solid #007bff; margin: 20px 0; }
        .footer { padding: 20px; text-align: center; font-size: 12px; color: #6c757d; border-top: 1px solid #eee; }
    </style>
</head>
<body>
    <div class=\"container\">
        <div class=\"header\">
            <h2>" . COMPANY_NAME . "</h2>
            <p>お問い合わせありがとうございます</p>
        </div>
        <div class=\"content\">
            <p>" . htmlspecialchars($name, ENT_QUOTES, 'UTF-8') . " 様</p>
            
            <p>この度は、" . COMPANY_NAME . "にお問い合わせいただき、誠にありがとうございます。</p>
            
            <p>以下の内容でお問い合わせを受け付けました。</p>
            
            <div class=\"message-box\">
                " . nl2br(htmlspecialchars($message, ENT_QUOTES, 'UTF-8')) . "
            </div>
            
            <p>内容を確認次第、担当者より折り返しご連絡させていただきます。<br>
            お急ぎの場合は、お電話にてお問い合わせください。</p>
            
            <p>今後とも " . COMPANY_NAME . " をよろしくお願いいたします。</p>
            
            <hr style=\"margin: 30px 0;\">
            
            <p><strong>" . COMPANY_NAME . "</strong><br>
            お問い合わせ: " . ADMIN_EMAIL . "<br>
            ウェブサイト: " . SITE_URL . "</p>
        </div>
        <div class=\"footer\">
            <p>このメールは自動送信されています。直接返信されても対応できませんのでご了承ください。</p>
        </div>
    </div>
</body>
</html>
        ";
    }
    
    /**
     * メール設定をテスト
     */
    public static function testMailConfiguration() {
        $test_email = ADMIN_EMAIL;
        $subject = '[' . COMPANY_NAME . '] メール設定テスト';
        $body = 'これはメール設定のテストメールです。このメールが届いていれば、設定は正常です。';
        
        $headers = [
            'From: ' . FROM_EMAIL,
            'X-Mailer: PHP/' . phpversion(),
            'Content-Type: text/plain; charset=UTF-8'
        ];
        
        return self::sendMail($test_email, $subject, $body, $headers);
    }
}
?> 