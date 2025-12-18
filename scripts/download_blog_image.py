#!/usr/bin/env python3
"""
Lorem Picsumを使用してブログ記事用の画像をダウンロードするスクリプト
（認証不要）

重複防止機能:
- used_images.json をチェックして、過去に使用したシードを避ける
- ユニークなランダムシードを生成
- ダウンロード後に used_images.json を更新
"""
import requests
import sys
import json
import random
from pathlib import Path
from datetime import datetime

# プロジェクトルート
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
BLOG_DIR = PROJECT_ROOT / "blog"
USED_IMAGES_FILE = BLOG_DIR / "used_images.json"


def load_used_images():
    """used_images.json を読み込む"""
    if not USED_IMAGES_FILE.exists():
        return {"images": [], "last_updated": None}
    
    try:
        with open(USED_IMAGES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, Exception) as e:
        print(f"⚠️  used_images.json の読み込みエラー: {e}")
        return {"images": [], "last_updated": None}


def save_used_images(data):
    """used_images.json を保存する"""
    data["last_updated"] = datetime.now().isoformat()
    
    with open(USED_IMAGES_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ used_images.json を更新しました")


def get_used_seeds(used_images_data):
    """使用済みのシード値を取得"""
    used_seeds = set()
    
    for img in used_images_data.get("images", []):
        url_hash = img.get("url_hash", "")
        # "seed123" 形式からシード値を抽出
        if url_hash.startswith("seed"):
            try:
                seed_value = int(url_hash[4:])
                used_seeds.add(seed_value)
            except ValueError:
                pass
    
    return used_seeds


def generate_unique_seed(used_seeds, max_attempts=100):
    """
    使用されていないユニークなシードを生成
    
    Args:
        used_seeds: 使用済みシードのセット
        max_attempts: 最大試行回数
    
    Returns:
        ユニークなシード値
    """
    for _ in range(max_attempts):
        # 1-9999の範囲でランダムにシードを生成
        seed = random.randint(1, 9999)
        if seed not in used_seeds:
            return seed
    
    # 全て使用済みの場合、10000以上のシードを使用
    seed = random.randint(10000, 99999)
    print(f"⚠️  1-9999の範囲でユニークなシードが見つからなかったため、{seed}を使用します")
    return seed


def register_image(used_images_data, seed, filename, article_slug, image_type):
    """
    使用した画像を登録
    
    Args:
        used_images_data: used_images.json のデータ
        seed: 使用したシード値
        filename: ファイル名
        article_slug: 記事のスラッグ
        image_type: 画像タイプ (header/thumbnail)
    """
    new_entry = {
        "url_hash": f"seed{seed}",
        "filename": filename,
        "used_date": datetime.now().strftime("%Y-%m-%d"),
        "article_slug": article_slug,
        "source": "picsum",
        "image_type": image_type
    }
    
    used_images_data["images"].append(new_entry)
    return used_images_data


def download_image(search_query, output_path, width=1200, height=630, article_slug=None, image_type="header"):
    """
    Lorem Picsumから画像をダウンロード（認証不要、重複防止機能付き）
    
    Args:
        search_query: 検索キーワード（参考情報として使用）
        output_path: 保存先パス
        width: 画像の幅
        height: 画像の高さ
        article_slug: 記事のスラッグ（オプション）
        image_type: 画像タイプ（header/thumbnail）
    
    Returns:
        成功時はシード値、失敗時はNone
    """
    # used_images.json を読み込み
    used_images_data = load_used_images()
    used_seeds = get_used_seeds(used_images_data)
    
    print(f"📊 使用済みシード数: {len(used_seeds)}")
    
    # ユニークなシードを生成
    seed = generate_unique_seed(used_seeds)
    
    # Lorem Picsumの無料URLを使用（認証不要）
    image_url = f"https://picsum.photos/seed/{seed}/{width}/{height}"
    
    try:
        print(f"🔍 画像を取得中: {search_query}")
        print(f"   シード: {seed}")
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
        print(f"   シード: {seed}")
        print(f"   サイズ: {width}x{height}")
        print(f"   出典: Lorem Picsum (https://picsum.photos)")
        
        # used_images.json に登録
        filename = output_path.name
        slug = article_slug or output_path.stem.rsplit('_', 1)[0]
        used_images_data = register_image(used_images_data, seed, filename, slug, image_type)
        save_used_images(used_images_data)
        
        return seed
        
    except requests.exceptions.RequestException as e:
        print(f"❌ ダウンロードエラー: {e}")
        return None
    except Exception as e:
        print(f"❌ 予期しないエラー: {e}")
        return None


def download_article_images(article_slug, keyword, output_dir=None):
    """
    記事用のヘッダー画像とサムネイル画像をダウンロード
    
    Args:
        article_slug: 記事のスラッグ（例: 2025-12-18-seo-basics）
        keyword: キーワード（ログ表示用）
        output_dir: 出力ディレクトリ（デフォルト: blog/images/）
    
    Returns:
        成功時True、失敗時False
    """
    if output_dir is None:
        output_dir = BLOG_DIR / "images"
    else:
        output_dir = Path(output_dir)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n🖼️  記事 '{article_slug}' の画像をダウンロード中...\n")
    
    # ヘッダー画像（1200x630）
    header_path = output_dir / f"{article_slug}_header.jpg"
    header_seed = download_image(
        search_query=keyword,
        output_path=header_path,
        width=1200,
        height=630,
        article_slug=article_slug,
        image_type="header"
    )
    
    if header_seed is None:
        print("❌ ヘッダー画像のダウンロードに失敗しました")
        return False
    
    print()  # 空行
    
    # サムネイル画像（400x300）
    thumbnail_path = output_dir / f"{article_slug}_thumbnail.jpg"
    thumbnail_seed = download_image(
        search_query=keyword,
        output_path=thumbnail_path,
        width=400,
        height=300,
        article_slug=article_slug,
        image_type="thumbnail"
    )
    
    if thumbnail_seed is None:
        print("❌ サムネイル画像のダウンロードに失敗しました")
        return False
    
    print(f"\n✅ 記事 '{article_slug}' の画像ダウンロード完了")
    print(f"   ヘッダー: {header_path.name} (seed{header_seed})")
    print(f"   サムネイル: {thumbnail_path.name} (seed{thumbnail_seed})")
    
    return True


def main():
    if len(sys.argv) < 3:
        print("使用方法:")
        print("  単一画像: python download_blog_image.py <キーワード> <出力パス>")
        print("  記事画像: python download_blog_image.py --article <スラッグ> <キーワード>")
        print()
        print("例:")
        print("  python download_blog_image.py 'SEO対策' blog/images/test.jpg")
        print("  python download_blog_image.py --article 2025-12-18-seo 'SEO対策'")
        sys.exit(1)
    
    # 記事用画像モード
    if sys.argv[1] == "--article":
        if len(sys.argv) < 4:
            print("使用方法: python download_blog_image.py --article <スラッグ> <キーワード>")
            sys.exit(1)
        
        article_slug = sys.argv[2]
        keyword = sys.argv[3]
        success = download_article_images(article_slug, keyword)
        sys.exit(0 if success else 1)
    
    # 単一画像モード
    search_query = sys.argv[1]
    output_path = sys.argv[2]
    
    seed = download_image(search_query, output_path)
    sys.exit(0 if seed else 1)


if __name__ == "__main__":
    main()
