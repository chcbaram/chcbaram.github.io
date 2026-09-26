#!/usr/bin/env bash
# 새 글 폴더를 만든다.
#   tools/new_post.sh <slug> "<title>"
set -euo pipefail

if [ $# -lt 1 ]; then
    echo "usage: $0 <slug> [\"title\"]" >&2
    exit 2
fi

slug="$1"
title="${2:-}"
dir="content/posts/${slug}"

if [[ ! "$slug" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
    echo "slug 은 영어 소문자와 하이픈만 쓴다: $slug" >&2
    exit 2
fi

if [ -e "$dir" ]; then
    echo "이미 있다: $dir" >&2
    echo "덮어쓰지 않는다. 다른 slug 를 쓴다." >&2
    exit 1
fi

hugo new content "posts/${slug}/index.md"

if [ -n "$title" ]; then
    python3 - "$dir/index.md" "$title" <<'PY'
import io, re, sys
path, title = sys.argv[1], sys.argv[2]
s = io.open(path, encoding="utf-8").read()
s = re.sub(r'^title:.*$', 'title: "%s"' % title.replace('"', '\\"'), s, count=1, flags=re.M)
io.open(path, "w", encoding="utf-8").write(s)
PY
fi

echo "만들었다: $dir/index.md"
