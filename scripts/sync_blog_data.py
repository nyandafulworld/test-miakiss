#!/usr/bin/env python3
"""
published_articles.json から published_articles.js を生成するスクリプト

使い方:
    python3 scripts/sync_blog_data.py

このスクリプトは、blog/published_articles.json を読み込み、
ローカルファイルシステムでも動作するように blog/published_articles.js を生成します。
"""

import json
import os
from pathlib import Path

def sync_blog_data():
    # スクリプトのディレクトリからプロジェクトルートを取得
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    json_file = project_root / 'blog' / 'published_articles.json'
    js_file = project_root / 'blog' / 'published_articles.js'
    
    # JSONファイルを読み込む
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ エラー: {json_file} が見つかりません")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ JSONデコードエラー: {e}")
        return False
    
    # JavaScriptファイルの内容を生成
    js_content = f"""// ブログ記事データ（ローカルファイルシステムでも動作するように、JavaScriptファイルとして提供）
// このファイルは published_articles.json と同じ内容を保持します
// ⚠️ このファイルは自動生成されます。手動で編集しないでください。
// 更新する場合は published_articles.json を編集し、scripts/sync_blog_data.py を実行してください。
window.BLOG_ARTICLES_DATA = {json.dumps(data, ensure_ascii=False, indent=2)};
"""
    
    # JavaScriptファイルに書き込む
    try:
        with open(js_file, 'w', encoding='utf-8') as f:
            f.write(js_content)
        print(f"✅ {js_file} を更新しました")
        print(f"📊 記事数: {len(data.get('articles', []))}件")
        return True
    except Exception as e:
        print(f"❌ ファイル書き込みエラー: {e}")
        return False

if __name__ == '__main__':
    print("ブログデータを同期しています...")
    success = sync_blog_data()
    if success:
        print("✅ 同期完了")
    else:
        print("❌ 同期失敗")
        exit(1)







