<?php
// バリデーション処理クラス

class ValidationHelper {
    
    private $errors = [];
    
    /**
     * エラーメッセージを追加
     */
    private function addError($field, $message) {
        $this->errors[$field] = $message;
    }
    
    /**
     * エラーメッセージを取得
     */
    public function getErrors() {
        return $this->errors;
    }
    
    /**
     * エラーがあるかチェック
     */
    public function hasErrors() {
        return !empty($this->errors);
    }
    
    /**
     * お名前のバリデーション
     */
    public function validateName($name) {
        if (empty($name)) {
            $this->addError('name', 'お名前は必須項目です。');
            return false;
        }
        
        if (mb_strlen($name) > MAX_NAME_LENGTH) {
            $this->addError('name', 'お名前は' . MAX_NAME_LENGTH . '文字以内で入力してください。');
            return false;
        }
        
        // 特殊文字のチェック
        if (preg_match('/[<>"\']/', $name)) {
            $this->addError('name', 'お名前に使用できない文字が含まれています。');
            return false;
        }
        
        return true;
    }
    
    /**
     * メールアドレスのバリデーション
     */
    public function validateEmail($email) {
        if (empty($email)) {
            $this->addError('email', 'メールアドレスは必須項目です。');
            return false;
        }
        
        if (mb_strlen($email) > MAX_EMAIL_LENGTH) {
            $this->addError('email', 'メールアドレスは' . MAX_EMAIL_LENGTH . '文字以内で入力してください。');
            return false;
        }
        
        if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
            $this->addError('email', '正しいメールアドレスの形式で入力してください。');
            return false;
        }
        
        // 一般的でないドメインのチェック（必要に応じて）
        $domain = substr(strrchr($email, "@"), 1);
        if (empty($domain)) {
            $this->addError('email', '正しいメールアドレスの形式で入力してください。');
            return false;
        }
        
        return true;
    }
    
    /**
     * お問い合わせ内容のバリデーション
     */
    public function validateMessage($message) {
        if (empty($message)) {
            $this->addError('message', 'お問い合わせ内容は必須項目です。');
            return false;
        }
        
        if (mb_strlen($message) > MAX_MESSAGE_LENGTH) {
            $this->addError('message', 'お問い合わせ内容は' . MAX_MESSAGE_LENGTH . '文字以内で入力してください。');
            return false;
        }
        
        if (mb_strlen($message) < 10) {
            $this->addError('message', 'お問い合わせ内容は10文字以上で入力してください。');
            return false;
        }
        
        // 禁止ワードチェック
        if (!SecurityHelper::checkForbiddenWords($message)) {
            $this->addError('message', '不適切な内容が含まれている可能性があります。');
            return false;
        }
        
        return true;
    }
    
    /**
     * 全体のバリデーション
     */
    public function validateAll($data) {
        $this->errors = []; // エラーをリセット
        
        $name_valid = $this->validateName($data['name'] ?? '');
        $email_valid = $this->validateEmail($data['email'] ?? '');
        $message_valid = $this->validateMessage($data['message'] ?? '');
        
        return $name_valid && $email_valid && $message_valid;
    }
    
    /**
     * エラーメッセージをJSON形式で取得
     */
    public function getErrorsAsJson() {
        return json_encode($this->errors, JSON_UNESCAPED_UNICODE);
    }
    
    /**
     * 成功メッセージを取得
     */
    public function getSuccessMessage() {
        return 'お問い合わせありがとうございます。<br>内容を確認次第、担当者より折り返しご連絡させていただきます。';
    }
    
    /**
     * フィールド別エラーメッセージを取得
     */
    public function getFieldError($field) {
        return $this->errors[$field] ?? '';
    }
    
    /**
     * エラーメッセージのHTML生成
     */
    public function getErrorsAsHtml() {
        if (empty($this->errors)) {
            return '';
        }
        
        $html = '<div class="form-errors">';
        $html .= '<ul>';
        
        foreach ($this->errors as $field => $error) {
            $html .= '<li>' . htmlspecialchars($error, ENT_QUOTES, 'UTF-8') . '</li>';
        }
        
        $html .= '</ul>';
        $html .= '</div>';
        
        return $html;
    }
}
?> 