#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
画像をリサイズして保存するスクリプト
"""

import sys
from pathlib import Path
from PIL import Image

def resize_image(input_path, output_path, target_width):
    """
    画像をリサイズして保存
    
    Args:
        input_path: 入力画像のパス
        output_path: 出力画像のパス
        target_width: リサイズ後の幅
    """
    try:
        # 画像を開く
        img = Image.open(input_path)
        
        # RGB変換（RGBA等の場合）
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # アスペクト比を保ってリサイズ
        width, height = img.size
        if width > target_width:
            new_height = int((target_width / width) * height)
            img = img.resize((target_width, new_height), Image.Resampling.LANCZOS)
        
        # 保存
        img.save(output_path, "JPEG", quality=85, optimize=True)
        print(f"✅ 保存完了: {output_path.name} ({img.size[0]}x{img.size[1]})")
        return True
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False


def main():
    if len(sys.argv) < 3:
        print("使用方法: python resize_and_save_image.py <入力画像> <slug>")
        sys.exit(1)
    
    input_file = Path(sys.argv[1])
    slug = sys.argv[2]
    
    if not input_file.exists():
        print(f"❌ エラー: ファイルが見つかりません: {input_file}")
        sys.exit(1)
    
    # 出力先
    project_root = Path(__file__).parent.parent
    images_dir = project_root / "blog" / "images"
    images_dir.mkdir(parents=True, exist_ok=True)
    
    thumbnail_path = images_dir / f"{slug}_thumbnail.jpg"
    header_path = images_dir / f"{slug}_header.jpg"
    
    print(f"\n📸 画像をリサイズ中...")
    print(f"   入力: {input_file.name}")
    
    # サムネイル（800px）
    print(f"\n🔹 サムネイル画像（800px）")
    resize_image(input_file, thumbnail_path, 800)
    
    # ヘッダー（1200px）
    print(f"\n🔹 ヘッダー画像（1200px）")
    resize_image(input_file, header_path, 1200)
    
    print(f"\n✅ 完了")


if __name__ == "__main__":
    main()





