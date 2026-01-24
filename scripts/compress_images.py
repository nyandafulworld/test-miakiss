#!/usr/bin/env python3
"""
ブログ記事用画像の圧縮スクリプト
PNG画像をJPEG形式に変換し、最適化して圧縮します。

使用方法:
  python3 scripts/compress_images.py <article_slug>
  
例:
  python3 scripts/compress_images.py 2026-01-20-website-speed-optimization
"""

import sys
from pathlib import Path
from PIL import Image

# プロジェクトルート
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
BLOG_IMAGES_DIR = PROJECT_ROOT / "blog" / "images"

# 圧縮設定
# サムネイルは16:9比率（600x340px推奨）でブログ一覧カードに最適化
COMPRESSION_SETTINGS = {
    "header": {"max_width": 1200, "quality": 82, "max_size_kb": 100},
    "thumbnail": {"max_width": 600, "quality": 80, "max_size_kb": 50},
    "diagram": {"max_width": 800, "quality": 85, "max_size_kb": 80},
}


def compress_image(input_path: Path, output_path: Path, settings: dict) -> bool:
    """
    画像を圧縮してJPEG形式で保存
    
    Args:
        input_path: 入力画像パス（PNG）
        output_path: 出力画像パス（JPEG）
        settings: 圧縮設定
    
    Returns:
        成功時True
    """
    try:
        with Image.open(input_path) as img:
            # RGBAをRGBに変換（JPEG用）
            if img.mode in ('RGBA', 'P'):
                # 白い背景を作成
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # リサイズ（幅が設定値を超える場合のみ）
            max_width = settings["max_width"]
            if img.width > max_width:
                ratio = max_width / img.width
                new_height = int(img.height * ratio)
                img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
            
            # JPEG形式で保存
            quality = settings["quality"]
            img.save(output_path, "JPEG", quality=quality, optimize=True)
            
            # ファイルサイズ確認
            file_size_kb = output_path.stat().st_size / 1024
            max_size_kb = settings["max_size_kb"]
            
            # サイズが大きい場合は品質を下げて再圧縮
            while file_size_kb > max_size_kb and quality > 50:
                quality -= 5
                img.save(output_path, "JPEG", quality=quality, optimize=True)
                file_size_kb = output_path.stat().st_size / 1024
            
            print(f"✅ 圧縮完了: {output_path.name}")
            print(f"   サイズ: {file_size_kb:.1f}KB (品質: {quality}%)")
            
            return True
            
    except Exception as e:
        print(f"❌ 圧縮エラー: {e}")
        return False


def get_image_type(filename: str) -> str:
    """ファイル名から画像タイプを判定"""
    if "_header" in filename:
        return "header"
    elif "_thumbnail" in filename:
        return "thumbnail"
    elif "_diagram" in filename:
        return "diagram"
    return "header"  # デフォルト


def compress_article_images(article_slug: str) -> bool:
    """
    記事用の全画像を圧縮
    
    Args:
        article_slug: 記事のスラッグ（例: 2026-01-20-website-speed-optimization）
    
    Returns:
        成功時True
    """
    print(f"\n🖼️  記事 '{article_slug}' の画像を圧縮中...\n")
    
    # PNG画像を検索
    png_files = list(BLOG_IMAGES_DIR.glob(f"{article_slug}*.png"))
    
    if not png_files:
        print(f"⚠️  PNG画像が見つかりません: {article_slug}*.png")
        return False
    
    success_count = 0
    
    for png_path in png_files:
        # 出力ファイル名（.png → .jpg）
        jpg_path = png_path.with_suffix('.jpg')
        
        # 画像タイプを判定
        image_type = get_image_type(png_path.name)
        settings = COMPRESSION_SETTINGS.get(image_type, COMPRESSION_SETTINGS["header"])
        
        print(f"📦 処理中: {png_path.name} ({image_type})")
        
        if compress_image(png_path, jpg_path, settings):
            success_count += 1
            # 元のPNGファイルを削除
            try:
                png_path.unlink()
                print(f"🗑️  元ファイル削除: {png_path.name}")
            except Exception as e:
                print(f"⚠️  元ファイル削除失敗: {e}")
        
        print()
    
    print(f"\n{'='*50}")
    print(f"✅ 圧縮完了: {success_count}/{len(png_files)} 画像")
    
    return success_count == len(png_files)


def main():
    if len(sys.argv) < 2:
        print("使用方法: python3 scripts/compress_images.py <article_slug>")
        print("例: python3 scripts/compress_images.py 2026-01-20-website-speed-optimization")
        sys.exit(1)
    
    article_slug = sys.argv[1]
    success = compress_article_images(article_slug)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
