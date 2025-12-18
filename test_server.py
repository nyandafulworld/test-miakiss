#!/usr/bin/env python3
"""
簡易的なHTTPサーバーを起動するスクリプト
ブログ記事の動的読み込み機能をテストするために使用します

使い方:
    python3 test_server.py

その後、ブラウザで http://localhost:8000 にアクセスしてください
"""

import http.server
import socketserver
import os

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # CORSヘッダーを追加
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        # キャッシュを無効化（開発時のみ）
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"サーバーを起動しました")
        print(f"ブラウザで http://localhost:{PORT} にアクセスしてください")
        print(f"終了するには Ctrl+C を押してください")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nサーバーを終了します")




















