#!/usr/bin/env python3
"""
Lorem Picsumを使用してブログ記事用の画像をダウンロードするスクリプト
（認証不要）
"""
import requests
import sys
from pathlib import Path
import random

def download_image(search_query, output_path, width=1200, height=630):
    """
    Lorem Picsumから画像をダウンロード（認証不要）
    
    Args:
        search_query: 検索キーワード（シードとして使用）
        output_path: 保存先パス
        width: 画像の幅
        height: 画像の高さ
    """
    # search_queryをシード値に変換（同じキーワードなら同じ画像）
    seed = abs(hash(search_query)) % 1000
    
    # Lorem Picsumの無料URLを使用（認証不要）
    # 画像をぼかしてビジネス風にする
    image_url = f"https://picsum.photos/seed/{seed}/{width}/{height}"
    
    try:
        print(f"🔍 画像を取得中: {search_query}")
        print(f"   URL: {image_url}")
        
        # 画像をダウンロード
        img_response = requests.get(image_url, timeout=30, allow_redirects=True)
        img_response.raise_for_status()
        
        # ファイルに保存
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, "wb") as f:
            f.write(img_response.content)
        
        print(f"✅ 画像をダウンロードしました: {output_path}")
        print(f"   キーワード: {search_query}")
        print(f"   サイズ: {width}x{height}")
        print(f"   出典: Lorem Picsum (https://picsum.photos)")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ ダウンロードエラー: {e}")
        return False
    except Exception as e:
        print(f"❌ 予期しないエラー: {e}")
        return False

def main():
    if len(sys.argv) < 3:
        print("使用方法: python download_blog_image.py <検索キーワード> <出力パス>")
        sys.exit(1)
    
    search_query = sys.argv[1]
    output_path = sys.argv[2]
    
    success = download_image(search_query, output_path)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()

