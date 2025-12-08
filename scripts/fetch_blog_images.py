#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ブログ記事用画像自動取得スクリプト

Unsplash API（優先）→ Pexels API（フォールバック）で
記事内容に沿った画像を自動取得し、保存します。
"""

import os
import sys
import json
import requests
from pathlib import Path
from typing import Optional, Dict, Tuple
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO

# プロジェクトルートのパスを取得
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
BLOG_DIR = PROJECT_ROOT / "blog"
IMAGES_DIR = BLOG_DIR / "images"

# .envファイルを読み込み
load_dotenv(PROJECT_ROOT / ".env")

# API設定
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

# 日本語→英語翻訳用の簡易辞書（よく使うキーワード）
TRANSLATION_DICT = {
    "ホームページ": "website homepage",
    "制作": "creation development",
    "保守": "maintenance",
    "運用": "operation management",
    "費用": "cost price",
    "料金": "price fee",
    "中小企業": "small business",
    "戸田市": "business office",
    "埼玉": "business office",
    "更新": "update",
    "セキュリティ": "security",
    "バックアップ": "backup",
    "問い合わせ": "contact inquiry",
    "集客": "marketing customer",
    "SEO": "seo search",
    "デザイン": "design",
    "会社": "company business",
    "サイト": "website",
    "Web": "web",
    "ビジネス": "business",
    "サービス": "service",
    "サポート": "support",
    "システム": "system",
    "リニューアル": "renewal redesign",
    "EC": "ecommerce online shop",
    "通販": "online shopping",
}


def translate_keyword(keyword: str) -> str:
    """
    日本語キーワードを英語に変換（簡易版）
    
    Args:
        keyword: 日本語キーワード
    
    Returns:
        英語キーワード
    """
    # 辞書にある単語を置換
    translated = keyword
    for jp, en in TRANSLATION_DICT.items():
        if jp in translated:
            translated = translated.replace(jp, en)
    
    # 汎用的な検索ワードに変換
    if translated == keyword:  # 変換されていない場合
        # ビジネス系の一般的な画像を取得
        translated = "business office modern technology"
    
    return translated.strip()


def fetch_from_unsplash(query: str, orientation: str = "landscape") -> Optional[str]:
    """
    Unsplash APIから画像URLを取得
    
    Args:
        query: 検索クエリ（英語）
        orientation: 画像の向き（landscape/portrait/squarish）
    
    Returns:
        画像URL（取得失敗時はNone）
    """
    if not UNSPLASH_ACCESS_KEY:
        print("⚠️  Unsplash APIキーが設定されていません")
        return None
    
    try:
        url = "https://api.unsplash.com/search/photos"
        headers = {
            "Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"
        }
        params = {
            "query": query,
            "orientation": orientation,
            "per_page": 1,
            "order_by": "relevant"
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data["total"] > 0 and len(data["results"]) > 0:
            photo = data["results"][0]
            image_url = photo["urls"]["regular"]  # 1080px幅
            print(f"✅ Unsplashから画像を取得: {query}")
            return image_url
        else:
            print(f"⚠️  Unsplashで画像が見つかりませんでした: {query}")
            return None
            
    except requests.RequestException as e:
        print(f"❌ Unsplash API エラー: {e}")
        return None


def fetch_from_pexels(query: str, orientation: str = "landscape") -> Optional[str]:
    """
    Pexels APIから画像URLを取得（フォールバック）
    
    Args:
        query: 検索クエリ（英語）
        orientation: 画像の向き（landscape/portrait/square）
    
    Returns:
        画像URL（取得失敗時はNone）
    """
    if not PEXELS_API_KEY:
        print("⚠️  Pexels APIキーが設定されていません")
        return None
    
    try:
        url = "https://api.pexels.com/v1/search"
        headers = {
            "Authorization": PEXELS_API_KEY
        }
        params = {
            "query": query,
            "orientation": orientation,
            "per_page": 1
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data["total_results"] > 0 and len(data["photos"]) > 0:
            photo = data["photos"][0]
            image_url = photo["src"]["large"]  # 1280px幅
            print(f"✅ Pexelsから画像を取得: {query}")
            return image_url
        else:
            print(f"⚠️  Pexelsで画像が見つかりませんでした: {query}")
            return None
            
    except requests.RequestException as e:
        print(f"❌ Pexels API エラー: {e}")
        return None


def download_and_save_image(image_url: str, save_path: Path, target_width: int = 1200) -> bool:
    """
    画像をダウンロードして保存
    
    Args:
        image_url: 画像のURL
        save_path: 保存先パス
        target_width: リサイズ後の幅（高さは自動計算）
    
    Returns:
        成功時True、失敗時False
    """
    try:
        response = requests.get(image_url, timeout=15)
        response.raise_for_status()
        
        # 画像を開く
        img = Image.open(BytesIO(response.content))
        
        # RGB変換（RGBA等の場合）
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # アスペクト比を保ってリサイズ
        width, height = img.size
        if width > target_width:
            new_height = int((target_width / width) * height)
            img = img.resize((target_width, new_height), Image.Resampling.LANCZOS)
        
        # 保存
        img.save(save_path, "JPEG", quality=85, optimize=True)
        print(f"💾 画像を保存: {save_path.name}")
        return True
        
    except Exception as e:
        print(f"❌ 画像のダウンロード・保存に失敗: {e}")
        return False


def fetch_blog_images(slug: str, title: str, description: str) -> Tuple[bool, bool]:
    """
    ブログ記事用の画像を取得
    
    Args:
        slug: 記事のスラッグ（ファイル名）
        title: 記事タイトル
        description: 記事の説明文
    
    Returns:
        (アイキャッチ画像の成功, ヘッダー画像の成功)
    """
    # 画像ディレクトリが存在するか確認
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    
    # キーワードを抽出（タイトルから主要なワードを使用）
    search_query = translate_keyword(title)
    
    print(f"\n🔍 記事: {title}")
    print(f"🔍 検索クエリ: {search_query}")
    
    # アイキャッチ画像（サムネイル）を取得
    thumbnail_path = IMAGES_DIR / f"{slug}_thumbnail.jpg"
    thumbnail_success = False
    
    if thumbnail_path.exists():
        print(f"✅ アイキャッチ画像は既に存在します: {thumbnail_path.name}")
        thumbnail_success = True
    else:
        print("\n📥 アイキャッチ画像を取得中...")
        # Unsplash → Pexels の順で試行
        image_url = fetch_from_unsplash(search_query, orientation="landscape")
        if not image_url:
            image_url = fetch_from_pexels(search_query, orientation="landscape")
        
        if image_url:
            thumbnail_success = download_and_save_image(image_url, thumbnail_path, target_width=800)
    
    # ヘッダー画像を取得（より大きいサイズ）
    header_path = IMAGES_DIR / f"{slug}_header.jpg"
    header_success = False
    
    if header_path.exists():
        print(f"✅ ヘッダー画像は既に存在します: {header_path.name}")
        header_success = True
    else:
        print("\n📥 ヘッダー画像を取得中...")
        # 異なる検索クエリで取得（バリエーションを持たせる）
        alt_query = f"{search_query} professional"
        image_url = fetch_from_unsplash(alt_query, orientation="landscape")
        if not image_url:
            # 同じ画像でも良い場合は元のクエリで再取得
            image_url = fetch_from_pexels(search_query, orientation="landscape")
        
        if image_url:
            header_success = download_and_save_image(image_url, header_path, target_width=1200)
    
    return thumbnail_success, header_success


def main():
    """
    メイン処理
    コマンドライン引数から記事情報を受け取り、画像を取得
    """
    if len(sys.argv) < 4:
        print("使用方法: python fetch_blog_images.py <slug> <title> <description>")
        sys.exit(1)
    
    slug = sys.argv[1]
    title = sys.argv[2]
    description = sys.argv[3]
    
    # APIキーの確認
    if not UNSPLASH_ACCESS_KEY and not PEXELS_API_KEY:
        print("❌ エラー: APIキーが設定されていません")
        print("📝 .envファイルにUNSPLASH_ACCESS_KEYまたはPEXELS_API_KEYを設定してください")
        sys.exit(1)
    
    # 画像を取得
    thumbnail_success, header_success = fetch_blog_images(slug, title, description)
    
    # 結果を表示
    print("\n" + "="*50)
    if thumbnail_success and header_success:
        print("✅ 全ての画像を取得しました！")
        sys.exit(0)
    elif thumbnail_success or header_success:
        print("⚠️  一部の画像のみ取得できました")
        sys.exit(0)
    else:
        print("❌ 画像の取得に失敗しました")
        print("💡 デフォルト画像（ogp.png）が使用されます")
        sys.exit(0)  # エラーでも継続（フォールバック対応）


if __name__ == "__main__":
    main()


