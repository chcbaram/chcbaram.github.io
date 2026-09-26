#!/usr/bin/env python3
"""발행 전 글 점검.

기본:  draft: true 가 아닌 모든 글을 검사한다. (draft 키가 없으면 Hugo 는 발행한다)
--all: draft 를 포함한 모든 글을 같은 기준으로 검사한다. /write-post 의 자체 점검용.

CI 는 빌드 전에 인자 없이 실행한다. 실패하면 배포하지 않는다.
"""
import argparse
import re
import sys
from pathlib import Path

POSTS = Path("content/posts")
IMAGE_WARN_BYTES = 1_500_000
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".gif", ".webp"}

FM = re.compile(r"\A---\n(.*?)\n---\n", re.S)


def front_matter(text):
    m = FM.match(text)
    if not m:
        return None, text
    fm = {}
    for line in m.group(1).splitlines():
        if ":" not in line or line.startswith(" "):
            continue
        k, v = line.split(":", 1)
        fm[k.strip()] = v.strip()
    return fm, text[m.end():]


def unquote(v):
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        return v[1:-1]
    return v


def check(path, body_required, errors, warnings):
    text = path.read_text(encoding="utf-8")
    fm, body = front_matter(text)
    rel = path.as_posix()

    if fm is None:
        errors.append("%s: front matter 를 읽을 수 없다" % rel)
        return

    if body_required:
        for marker, label in (("TODO(author)", "TODO(author)"), ("<!-- PHOTO:", "사진 자리가")):
            n = body.count(marker)
            if n:
                errors.append("%s: %s %d 개가 남아 있다" % (rel, label, n))

    if not unquote(fm.get("description", "")):
        errors.append("%s: description 이 비었다" % rel)

    projects = fm.get("projects", "").strip()
    if not projects or projects in ("[]", "''", '""'):
        errors.append("%s: projects 가 없다" % rel)

    image = unquote(fm.get("image", ""))
    if image and not (path.parent / image).exists():
        errors.append("%s: image 로 적은 %s 가 글 폴더에 없다" % (rel, image))

    for f in sorted(path.parent.iterdir()):
        if f.suffix.lower() in IMAGE_SUFFIXES and f.stat().st_size > IMAGE_WARN_BYTES:
            warnings.append("%s: %.1f MB (권장 1.5 MB 이하)" % (f.as_posix(), f.stat().st_size / 1e6))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true",
                    help="draft 를 포함한 모든 글을 검사한다")
    args = ap.parse_args()

    if not POSTS.is_dir():
        print("content/posts 가 없다. 저장소 루트에서 실행한다.", file=sys.stderr)
        return 2

    errors, warnings, infos, checked = [], [], [], 0
    for path in sorted(POSTS.rglob("index.md")):
        if path.name.startswith("_"):
            continue
        fm, _ = front_matter(path.read_text(encoding="utf-8"))
        is_draft = (fm or {}).get("draft", "false").strip().lower() == "true"
        if is_draft and not args.all:
            continue
        # draft 글에 TODO 와 사진 자리가 남아 있는 것은 정상이다. 세어서 알려만 준다.
        if is_draft:
            body = path.read_text(encoding="utf-8")
            todo = body.count("TODO(author)")
            photo = body.count("<!-- PHOTO:")
            if todo or photo:
                infos.append("%s: draft — TODO(author) %d, 사진 자리 %d"
                             % (path.as_posix(), todo, photo))
        check(path, body_required=not is_draft, errors=errors, warnings=warnings)
        checked += 1

    for i in infos:
        print("알림: %s" % i)
    for w in warnings:
        print("경고: %s" % w)
    for e in errors:
        print("실패: %s" % e)

    print("검사한 글 %d 개, 실패 %d, 경고 %d" % (checked, len(errors), len(warnings)))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
