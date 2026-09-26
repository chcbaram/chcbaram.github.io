#!/usr/bin/env python3
"""사진을 줄여서 글 폴더에 넣는다.

    tools/import_photos.py <사진폴더> <글폴더>

- 촬영 시각(EXIF DateTimeOriginal) 순으로 정렬해 01.jpg, 02.jpg ... 로 복사한다.
- 긴 변 2000px, JPEG 품질 85.
- EXIF 회전을 적용하고 GPS 를 포함한 모든 EXIF 는 지운다.

의존성은 Pillow 하나다. HEIC 는 Pillow 단독으로 열 수 없다.
아이폰 사진은 JPEG 로 내보내서 넘기거나 pillow-heif 를 설치한다.
"""
import sys
from pathlib import Path

try:
    from PIL import Image, ImageOps
except ImportError:
    sys.exit("Pillow 가 필요하다: pip install Pillow")

LONG_EDGE = 2000
QUALITY = 85
SUFFIXES = {".jpg", ".jpeg", ".png", ".tif", ".tiff"}
DATE_TAG = 36867  # DateTimeOriginal


def shot_time(path):
    try:
        with Image.open(path) as im:
            exif = im.getexif()
            value = exif.get(DATE_TAG)
            if value:
                return (0, str(value))
    except Exception:
        pass
    return (1, "%013d" % int(path.stat().st_mtime))


def main():
    if len(sys.argv) != 3:
        sys.exit("usage: %s <사진폴더> <글폴더>" % sys.argv[0])

    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    if not src.is_dir():
        sys.exit("사진 폴더가 없다: %s" % src)
    if not dst.is_dir():
        sys.exit("글 폴더가 없다: %s" % dst)

    heic = [p for p in src.iterdir() if p.suffix.lower() in (".heic", ".heif")]
    if heic:
        print("건너뜀: HEIC %d 장. JPEG 로 내보내서 다시 넘긴다." % len(heic))

    photos = sorted((p for p in src.iterdir() if p.suffix.lower() in SUFFIXES),
                    key=shot_time)
    if not photos:
        sys.exit("넣을 사진이 없다: %s" % src)

    start = 1
    while (dst / ("%02d.jpg" % start)).exists():
        start += 1

    for i, path in enumerate(photos, start=start):
        out = dst / ("%02d.jpg" % i)
        with Image.open(path) as im:
            im = ImageOps.exif_transpose(im)      # 회전 적용
            im = im.convert("RGB")                # EXIF 를 들고 있지 않은 새 이미지
            im.thumbnail((LONG_EDGE, LONG_EDGE), Image.LANCZOS)
            im.save(out, "JPEG", quality=QUALITY, optimize=True)
        print("%s -> %s  (%.0f KB)" % (path.name, out.name, out.stat().st_size / 1024))


if __name__ == "__main__":
    main()
