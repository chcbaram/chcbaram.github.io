# chcbaram.github.io 블로그 작업 문서

이 문서는 `chcbaram.github.io` 저장소에서 Claude Code 가 작업할 때 기준이 되는 문서다.
저장소 루트에 `CLAUDE.md` 로 둔다.

## 목적

내가 작업한 펌웨어·하드웨어·도구 프로젝트를 영어 기술 글로 발행한다.
글은 Claude Code 가 공개 저장소의 문서, 커밋 이력, 코드를 읽고 초안을 쓰고, 내가 검토해서 발행한다.

네이버 블로그(blog.naver.com/chcbaram)와는 역할을 나눈다.

| 채널 | 언어 | 내용 |
| --- | --- | --- |
| 네이버 블로그 | 한국어 | 제품 리뷰, 조립기, 사진 위주 작업 일지 |
| chcbaram.github.io | 영어 | 설계 설명, 문제 해결 과정, 측정, 튜토리얼, 프로젝트 소개 |

같은 글을 두 곳에 올리지 않는다. 네이버에는 필요하면 한국어 짧은 소개와 링크만 올린다.

## 확정된 결정

| 항목 | 결정 |
| --- | --- |
| 생성기 | Hugo (extended) |
| 테마 | Stack (hugo-theme-stack) |
| 저장소 | `chcbaram/chcbaram.github.io` (사용자 사이트, Public) |
| 주소 | `https://chcbaram.github.io/` |
| 배포 | GitHub Actions → GitHub Pages |
| 언어 | 영어가 기본(`locale = "en"`, `defaultContentLanguage = "en"`). **한국어판은 기본으로 만들지 않는다** — 아래 "한국어를 어디에 쓰나" |
| 글 위치 | 지금은 모든 글이 `content/posts/<slug>/` 한 곳. 글이 많아지면 `content/posts/<프로젝트>/<slug>/` 로 나눌 수 있다 — 주소는 안 바뀐다 (아래) |
| 분류 | `projects` (어느 저장소 이야기인지) + `tags` (기술 키워드) |
| 글 URL | `/posts/<slug>/`. 분류를 바꿔도 주소가 바뀌지 않는다 |
| 글 형식 | 글마다 폴더(page bundle): `index.md` + 사진 |
| 외관 | Stack 테마 기본 그대로. 코드 글꼴만 D2Coding 으로 바꾼다 |

### 카테고리를 두지 않는 이유

- 글이 모두 기술 글이고 대부분 특정 저장소 이야기라서, "어느 프로젝트인가"가 가장 쓸모 있는 분류다.
- 폴더 기반 **카테고리**는 분류를 바꾸면 URL 이 바뀐다. 검색 노출에 불리하다. 그래서 분류는 `projects` / `tags` 로만 한다.
- 다만 **폴더로 나누는 것과 URL 이 바뀌는 것은 별개다.** `[permalinks] posts = "/posts/:contentbasename/"` 을 넣어 두었으므로, 글이 많아져 `content/posts/<프로젝트>/<slug>/` 로 나누더라도 주소는 `/posts/<slug>/` 그대로다 (2026-09-27 에 실제로 옮겨서 확인했다 — 한국어판, 글 사이 상대 링크, 이미지, 홈·아카이브 목록 모두 정상).
  - ★ **`:slug` 를 쓰면 안 된다.** 폴더 이름이 아니라 **제목**에서 주소를 만든다. 실제로 `/posts/a-ghost-input-above-the-actuation-point-and-the-two-bugs-under-it/` 가 나왔다.
  - ★ 나눌 때 하위 폴더에 **`_index.md` 를 두지 않는다.** 섹션이 되면서 `/posts/<프로젝트>/` 가 생기는데, 이미 있는 `/projects/<프로젝트>/` 와 역할이 겹친다.
  - 옮기는 비용은 `git mv` 뿐이라 서두를 이유가 없다. 한 폴더가 손에 부칠 때 옮긴다.
- 글 수가 많아져서 큰 묶음이 필요해지면, 그때 `categories` 를 3~5개 평면으로 추가한다 (예: Firmware, Hardware, Tools). 트리 구조는 만들지 않는다.

## 지켜야 할 규칙

### 사이트

- **기존 프로젝트 사이트와 경로를 겹치지 않는다.** `chcbaram.github.io/qmk-link/` 같은 프로젝트 페이지가 이미 있다. `content/` 최상위나 `static/` 에 기존 저장소 이름과 같은 폴더를 만들지 않는다. 필요하면 `gh repo list chcbaram --limit 400` 으로 확인한다.
- **Git LFS 를 쓰지 않는다.** GitHub Pages 가 LFS 파일을 제대로 서비스하지 못한다.
- **원본 사진을 그대로 커밋하지 않는다.** `tools/import_photos.py` 로 줄여서 넣는다. 사이트 전체 1GB 한도가 있다.
- **실수로 원본을 커밋했으면 되돌리는 커밋으로 끝내지 않는다.** 블롭이 히스토리에 남아 한도에 계속 잡힌다. 푸시 전이면 `git reset`, 푸시 후면 히스토리를 정리한다.
- **긴 동영상은 저장소에 넣지 않는다.** 30초 안쪽 짧은 영상만 mp4 로 줄여서 넣고, 긴 것은 YouTube 에 올려 `{{< youtube ID >}}` 로 넣는다.
- 테마 파일을 직접 고치지 않는다. 바꿀 것은 저장소의 `layouts/`, `assets/` 에서 덮어쓴다.

### 외관

- **테마 기본 모양을 바꾸지 않는다.** 색, 카드, 모서리, 그림자는 Stack 이 주는 그대로 쓴다.
- **코드 글꼴만** D2Coding (SIL OFL 1.1) 으로 바꾼다. `layouts/_partials/head/custom.html` 에서 jsDelivr 의 subset 판(약 350KB)을 불러오고, `assets/scss/custom.scss` 에서 `--code-font-family` 만 덮어쓴다.
- **본문에는 고정폭을 쓰지 않는다.** 산문 가독성이 떨어지고, 굵기 대비가 작아 제목과 본문의 위계가 약해진다.
- `assets/scss/custom.scss` 에는 글꼴 변수와, 테마에 없는 요소(저장소 상자, AI 표시)의 최소 스타일만 둔다. 터미널 풍이나 PC 통신 풍 꾸밈은 넣지 않는다. 일관성이 깨진다.

### 글 재료와 공개 범위

- **공개(Public) 저장소만 재료로 쓴다.** 비공개 저장소는 내가 명시적으로 지시한 경우에만 읽고, 그때도 회로도, 핀 배치, 고객·회사 이름, 내부 일정, 장치 식별 정보는 글에 넣지 않는다.
- 저장소 안에 비공개 규칙 문서가 있으면(예: baram-term 의 `docs/device-testing.md`) 그 규칙을 따른다.
- 시리얼 번호, MAC 주소, 토큰, 개인 경로(`/Users/...`) 같은 값이 코드 발췌나 로그에 섞여 있으면 지운다.

### 글 내용의 사실성

- **사실은 저장소에서만 가져온다.** 문서, 커밋 메시지, 코드, 측정 기록, 이슈에 있는 것만 쓴다.
- 근거를 찾지 못한 내용은 추측으로 채우지 않고 `TODO(author): ...` 로 남긴다. 내가 검토하면서 채운다.
- 수치(클럭, 전류, 지연, 크기)는 출처 파일에 있는 값을 그대로 쓴다. 단위를 붙인다.
- 칩이나 라이브러리의 일반 사양을 설명할 때 확실하지 않으면 TODO 로 남긴다.
- 동기, 판단, 삽질 경험처럼 문서에 없는 "왜"는 지어내지 않는다. 문서나 커밋에 이유가 적혀 있으면 쓰고, 없으면 `TODO(author): why did you choose X?` 로 질문을 남긴다.

## 글 작성 원칙 (영어)

- 1인칭 단수(I) 개발 일지 톤. 짧은 문장, 평이한 영어.
- 과장 표현을 쓰지 않는다: "revolutionary", "seamless", "game-changer", "robust", "leverage", "delve", "in today's fast-paced world" 등.
- 구성은 대략 이 순서를 따른다. 억지로 모든 절을 채우지 않는다.
  1. What I built / what problem I had
  2. Constraints
  3. Approach and design decisions
  4. Details (code, register settings, schematics that are public)
  5. Results (measurements, photos, video)
  6. What's next / known issues
  7. Links (repo, related posts)
- 길이는 보통 800~1500 단어. 주제가 크면 여러 글로 나누고 `series` 로 묶는다.
- 코드는 실제 저장소 코드에서 발췌한다. 한 블록 30줄 이내. 블록 위에 파일 경로를 쓰고, 커밋 해시가 들어간 GitHub permalink 를 단다.
- 사진이 필요한 자리에는 `<!-- PHOTO: board top view, USB side -->` 처럼 무엇을 찍을지 적어 둔다.
- 첫 문단만 읽어도 무엇을 만들었고 무엇을 배울 수 있는지 알 수 있게 쓴다. 이 문단과 `description` 이 검색 결과와 AI 인용에 쓰인다.

## 디렉터리 구조

```
chcbaram.github.io/
├── CLAUDE.md
├── BACKLOG.md                  # 글감 목록 — 여기서 다음 글을 고른다
├── hugo.toml
├── .claude/commands/
│   └── write-post.md           # /write-post 커스텀 명령
├── .github/workflows/hugo.yml
├── archetypes/
│   └── posts.md
├── assets/                     # 테마 SCSS 덮어쓰기
├── layouts/                    # 테마와 같은 새 구조를 쓴다: _partials, _shortcodes
│   ├── _partials/
│   │   └── article/
│   │       ├── repo-box.html   # 글 상단 저장소 링크 상자
│   │       └── ai-note.html    # AI 작성 보조 표시
│   └── _shortcodes/
│       └── video.html          # 테마 기본 video 를 덮어쓴다 (단계 4)
├── static/
│   └── robots.txt
├── content/
│   ├── page/                   # 테마의 page 레이아웃을 타는 고정 페이지
│   │   ├── about/index.md
│   │   └── search/index.md     # layout: search, outputs: [html, json]
│   ├── projects/               # 프로젝트 소개 페이지 (taxonomy term 페이지)
│   │   └── baram-term/_index.md
│   └── posts/
│       └── retro-ui-pixel-graphs-in-a-tui/
│           ├── index.md
│           └── 01.jpg
└── tools/
    ├── import_photos.py
    ├── new_post.sh
    └── check_posts.py
```

## 글 front matter

```yaml
---
title: "Drawing Real Pixel Graphs Inside a Retro TUI"
date: 2026-09-27T10:00:00+09:00
description: "One or two sentences. What I built and what the reader will learn."
projects: ["baram-term"]
tags: ["python", "pygame", "serial", "firmware-tools"]
series: []
repo: "https://github.com/chcbaram/baram-term"
image: ""              # 사진을 넣은 뒤 "01.jpg" 로 채운다
ai_assisted: true
naver_url: ""          # 네이버에 관련 한국어 글이 있을 때만
draft: true
---
```

- **`date` 를 미래로 두지 않는다.** Hugo 는 미래 날짜 글을 빌드에서 빼고, 경고도 내지 않는다. 글이 안 보이면 이것부터 본다.
- Claude Code 가 만든 글은 항상 `draft: true` 로 시작한다. `draft: false` 로 바꾸는 것은 내가 한다.
- `ai_assisted: true` 이면 글 하단에 "Drafted with Claude from project notes and commit history, reviewed and edited by the author." 를 출력한다.

## 작업 단계

단계마다 완료 조건을 확인하고 커밋한다.

### 단계 1: 사이트 뼈대와 배포

- Hugo extended 와 Go 설치 여부를 확인하고 버전을 기록한다. **Stack 을 Hugo module 로 쓰면 Go 가 필요하다.**
- Hugo 버전은 테마 `theme.toml` 의 `min_version` 이상으로 맞춘다. 현재 Stack 은 **0.157.0 이상 extended** 를 요구한다.
- Stack 테마를 Hugo module 로 추가한다. (공식 starter 저장소 `hugo-theme-stack-starter` 구성을 참고한다.)
- `hugo.toml` 기본 설정: `baseURL`, 영어(`languageCode`, `defaultContentLanguage`), 페이지당 글 수, 다크 모드 토글, taxonomy(`tags`, `projects`, `series`, `categories`).
  - **`mainSections = ["posts"]` 를 반드시 넣는다.** Stack 기본값은 `["post"]` (단수)라서 빠뜨리면 홈과 아카이브에 글이 하나도 안 뜬다.
  - **starter 의 `permalinks.toml` 은 복사하지 않는다.** starter 는 `post = "/p/:slug/"` 라서 목표한 `/posts/<slug>/` 가 안 나온다. Hugo 기본값이 이미 `/posts/<slug>/` 이고, 여기에 `posts = "/posts/:contentbasename/"` 만 더해 글 폴더를 나눠도 주소가 안 바뀌게 해 두었다.
  - **`languageCode` 는 쓰지 않는다.** Hugo 0.158 에서 deprecated 다. `locale` 을 쓴다.
  - **고정 페이지는 `[permalinks] page = "/:slug/"` 로 루트에 올린다.** 안 그러면 `/page/about/` 가 된다. 루트 slug 는 내 저장소 이름과 겹치면 안 된다 (2026-09-27 기준 `about`, `search`, `archives`, `posts`, `projects`, `tags` 와 겹치는 공개 저장소는 없다).
  - **`categories` 는 쓰지 않아도 taxonomy 정의는 남겨둔다.** taxonomy 를 재정의하면 기본 `categories` 가 사라지고, starter 기본 위젯 목록의 `categories` 위젯이 깨진다. 위젯 목록에서도 빼든지 정의를 남기든지 하나는 해야 한다.
- GitHub Actions 워크플로를 추가한다. Hugo 공식 문서의 GitHub Pages 워크플로를 기준으로 하고, Hugo 버전을 워크플로 안에 고정한다. module 을 쓰므로 `actions/setup-go` 단계도 넣는다.
- 워크플로에서 빌드 전에 `tools/check_posts.py` 를 실행한다 (단계 6).
- 저장소 Settings → Pages → Source 를 GitHub Actions 로 바꾸는 것은 내가 한다. 필요 시 안내만 한다.

완료 조건: `hugo server` 로 로컬 확인, push 후 `https://chcbaram.github.io/` 에 빈 사이트가 뜬다.

### 단계 2: 프로필과 사이드바

- 사이드바에 프로필 사진, 이름, 한 줄 소개, GitHub 링크, 네이버 블로그 링크를 넣는다. 프로필 사진과 소개 문구는 내가 준다.
- 메뉴: Home, Projects, Tags, Archives, About.
- 위젯: 검색, 프로젝트 목록, 태그 클라우드, 아카이브.
- **고정 페이지는 `content/page/` 아래에 둔다.** 테마의 `layouts/page/` 템플릿은 `page` 섹션에만 적용된다. About 은 `content/page/about/index.md`.
- **검색 위젯만 켜면 동작하지 않는다.** 테마의 검색은 `layouts/page/search.json` 출력을 쓰므로 아래 페이지가 있어야 한다.

  ```yaml
  ---
  title: "Search"
  slug: "search"
  layout: "search"
  outputs: [html, json]
  ---
  ```

완료 조건: 사이드바와 메뉴가 보이고 링크가 동작한다. `/search/` 에서 글이 검색된다.

### 단계 3: 프로젝트 페이지

- `/projects/` 에 프로젝트 목록을 보여준다. 각 항목에 이름, 한 줄 설명, 글 수.
- `/projects/<name>/` 에 프로젝트 설명, 저장소 링크, 해당 글 목록을 보여준다. 설명은 `content/projects/<name>/_index.md` 에 쓴다.
- **위젯을 새로 만들지 않는다.** 테마에 범용 `_partials/widget/taxonomy.html` 이 있어서 설정만으로 `projects` 를 띄울 수 있다.

  ```toml
  [[params.widgets.homepage]]
    type = "taxonomy"
    [params.widgets.homepage.params]
      taxonomy = "projects"
      title    = "Projects"
      limit    = 10
  ```

- 위젯을 직접 만들어야 할 일이 생기면 **반드시 `layouts/_partials/widget/<type>.html`** 에 둔다. 테마가 `templates.Exists "_partials/widget/<type>.html"` 로 확인하기 때문에 옛 경로인 `layouts/partials/` 에 두면 못 찾고 경고만 남는다.
- 첫 프로젝트 페이지 후보: baram-term, qmk-link, wish-he, via-he, baram-nrf54-arduino. 공개 저장소인지 확인하고 만든다.

완료 조건: 예시 프로젝트 2개 이상에서 목록, 설명, 글 목록이 맞다.

### 단계 4: 글 화면

- 본문 사진은 가로폭에 맞춰 크게 보이고, 누르면 확대된다. Stack 의 이미지 처리(리사이즈, lazy load)가 page bundle 사진에 적용되는지 확인한다.
- **잘라낸 화면(크롭)은 파일 이름 끝에 `-crop` 을 붙인다.** (2026-09-27 정함)
  - Stack 은 래스터 그림을 `figure` 로 감싸 인라인 `flex-grow` 로 본문 폭(최대 1232px)까지 늘린다.
  - 사진과 **창 전체를 찍은 화면**은 원본이 이미 축소돼 있으니 그렇게 꽉 채우는 게 맞다. 이름을 그냥 둔다.
  - 창의 **일부만 잘라낸 그림**은 늘리면 안의 글자만 커져 본문과 위계가 깨진다. `-crop` 이 붙으면 `assets/scss/custom.scss` 의 `figure:has(img[src*="-crop."])` 규칙이 원본 폭에서 멈춘다. 본문 글자가 17px(`1.7rem`, `html` 이 62.5%)이라 크롭 안 UI 글자 13~14px 과 위계가 맞는다.
  - 좁은 화면에서는 `flex-shrink` 가 살아 있어 화면 폭에 맞춰 줄어든다. SVG 다이어그램은 테마가 `gallery` 로 안 감싸므로 영향이 없다.
- `{{< video "clip.mp4" >}}` shortcode: 테마에 이미 `_shortcodes/video.html` 이 있지만 `controls` 만 있고 `playsinline` 과 `preload="metadata"` 가 없다. **`layouts/_shortcodes/video.html`** 에 같은 이름으로 두어 덮어쓴다. 위치 인자(`.Get 0`)를 그대로 받도록 유지한다.
- `repo` 가 있으면 글 상단에 저장소 링크 상자(이름, 설명, 링크)를 출력한다.
- `ai_assisted` 표시 partial.
- **대표 이미지(`image`)를 화면에 얹지 않는다.** 테마는 글 화면에서는 제목 위에, 목록에서는 카드 맨 위에 고정 높이로 잘라 넣는데, 글자가 든 다이어그램은 잘리면 못 읽는다. `layouts/_partials/article/components/header.html` 에서 테마 것을 덮어써서 출력을 막았다. front matter 의 `image` 는 그대로 두며 `og:image` 로만 쓰인다. 본문에 그림이 필요하면 마크다운으로 설명하는 자리에 직접 넣는다.
- `naver_url` 이 있으면 "A Korean write-up of this project is on my Naver blog." 링크를 출력한다.
- 댓글은 giscus. Discussions 활성화와 giscus 앱 설치는 내가 하고, 설정값을 받아 `hugo.toml` 에 넣는다.
- 코드 블록 하이라이트와 복사 버튼이 동작하는지 확인한다.
- 글 라이선스 표시(`params.article.license`)를 켤지 정한다. starter 기본은 CC BY-NC-SA 4.0 이다.
- 회로·블록 다이어그램이 필요하면 테마의 mermaid 지원을 쓴다. 사진으로 대체할 수 있으면 사진을 쓴다.

완료 조건: 예시 글 1개에서 사진, 동영상, 저장소 상자, AI 표시, 댓글 영역이 모두 보인다.

### 단계 5: 검색 노출 설정

- `robots.txt`: 모든 봇 허용, sitemap 위치 명시.

  ```
  User-agent: *
  Allow: /

  Sitemap: https://chcbaram.github.io/sitemap.xml
  ```

  AI 학습용 봇(GPTBot, ClaudeBot, Google-Extended)을 막을지는 내가 정한다. 정하기 전까지는 전체 허용. 검색용 봇(OAI-SearchBot, Claude-SearchBot, Claude-User, Googlebot)은 막지 않는다.
- `llms.txt`: 사이트 소개, 프로젝트별 글 목록(제목, URL, description). Hugo custom output format 으로 빌드 시 자동 생성한다.
- 글마다 canonical 이 자기 자신 주소인지, Open Graph 태그(제목, 설명, 대표 이미지)가 나오는지 확인한다.
- 구글 서치콘솔과 네이버 서치어드바이저 소유권 확인 메타 태그 자리를 만든다. 내용이 네이버 블로그와 다르므로 둘 다 등록한다. 값은 내가 준다.

완료 조건: 빌드 결과에 `robots.txt`, `sitemap.xml`, `llms.txt` 가 있고, 글 HTML 에 canonical 과 OG 태그가 있다.

### 단계 6: 글 쓰기 도구

`tools/new_post.sh <slug> "<title>"`

- `content/posts/<slug>/index.md` 를 archetype 으로 만든다.

`tools/import_photos.py <사진폴더> <글폴더>`

- 사진을 촬영 시각(EXIF) 순으로 정렬해 `01.jpg`, `02.jpg` … 로 복사한다.
- 긴 변 2000px, JPEG 품질 85. EXIF 회전을 적용하고 GPS 등 EXIF 는 지운다.
- 의존성은 Pillow 하나. **HEIC 는 Pillow 단독으로 못 연다.** 아이폰 사진은 JPEG 로 내보내서 넘기거나, `pillow-heif` 를 추가 의존성으로 허용한다. 어느 쪽인지 정해서 여기 적는다.

`tools/check_posts.py`

- 검사 대상은 **`draft: true` 가 아닌 모든 글**이다. `draft` 키가 아예 없으면 Hugo 는 발행하므로 검사해야 한다. `_index.md` 는 제외한다.
- 대상 글에 `TODO(author)` 나 `<!-- PHOTO:` 가 남아 있으면 실패한다.
- `description` 이 비었거나 `projects` 가 없으면 실패한다.
- `image` 에 적힌 파일이 글 폴더에 없으면 실패한다.
- 글 폴더 안 이미지가 장당 1.5MB 를 넘으면 경고한다.
- `--all` 옵션을 둔다. draft 를 포함한 모든 글을 같은 기준으로 검사한다. `/write-post` 의 자체 점검이 이걸 쓴다.
- GitHub Actions 빌드 전에 실행한다. 실패하면 배포하지 않는다.

완료 조건: 세 도구가 동작하고, TODO 가 남은 글을 `draft: false` 로 바꾸면 CI 가 실패한다.

### 단계 7: `/write-post` 명령

`.claude/commands/write-post.md` 를 저장소에 둔다 (별도 파일로 제공됨). 이 명령의 절차와 이 문서의 "글 재료와 공개 범위", "글 내용의 사실성", "글 작성 원칙" 을 따른다.

완료 조건: `/write-post baram-term` 으로 draft 글 폴더가 만들어진다.

### 단계 8: 예시 글 — baram-nrf54-arduino

첫 글이자 전체 흐름(명령 → 초안 → 검토 → CI 점검 → 발행)을 검증하는 글이다.
저장소는 `chcbaram/baram-nrf54-arduino` (nRF54L 시리즈용 Arduino 코어).

**진행 순서**

1. 저장소가 Public 인지 확인한다.
2. `content/projects/baram-nrf54-arduino/_index.md` 를 README 기준으로 만든다.
3. `/write-post baram-nrf54-arduino` 를 주제 없이 실행해 글감 후보 3개를 받는다. 아래 후보 각도를 참고하되, 저장소에 근거가 있는 것만 후보로 낸다.
4. 내가 고른 주제로 draft 를 만든다.
5. 보고된 TODO 와 사진 자리를 내가 채운다. 보드 사진, 예제 스케치 동작 사진은 내가 준다.
6. `draft: false` 로 바꾸기 전에 `tools/check_posts.py` 가 TODO 를 잡는지 먼저 확인하고, 다 채운 뒤 통과하는지 확인한다.

**후보 각도** (README 와 릴리스에서 보이는 것. 세부 내용은 저장소에서 다시 확인한다)

- 설계 원칙: 이식성과 Adafruit Bluefruit 호환성이 충돌하면 호환성을 택한 이유와, 그 원칙이 API 설계에 어떻게 반영됐는지.
- 마이그레이션 가이드: nRF52 Bluefruit 스케치를 nRF54L 보드로 옮길 때 그대로 되는 것과 달라지는 것 (예: `analogRead` 기준 전압과 게인 차이). README 의 지원 범위 표와 주의 사항을 재료로 쓴다.
- 구현 이야기: FreeRTOS 위에서 `delay()`, `Scheduler.startLoop()` 같은 Bluefruit 동작을 맞춘 방법.
- 개발 기록: 0.1.0 부터 최신 릴리스까지 무엇이 추가됐는지. 릴리스 노트와 커밋 이력을 재료로 쓴다.

한 글에 다 넣지 않는다. 첫 글은 설계 원칙 또는 마이그레이션 가이드 중 하나를 권장하고, 나머지는 `series: ["nRF54L Arduino Core"]` 로 묶어 후속 글로 쓴다.

**주의**

- nRF54L 칩의 일반 사양(메모리, 주변장치, 전압 등)은 저장소에 적힌 값만 쓴다. 저장소에 없으면 TODO 로 남긴다.
- 보드가 비공개 설계라면 회로도와 핀 배치는 넣지 않는다. 공개 여부가 저장소에서 불분명하면 나에게 묻는다.
- 코드 발췌는 예제 스케치(`examples/`)와 코어 소스에서 가져오고, 기준 커밋 permalink 를 단다.
- 저장소 description 이 비어 있으므로 `_index.md` 의 한 줄 설명은 README 에서 뽑는다.

완료 조건: draft 글 1개와 프로젝트 페이지가 만들어지고, TODO 를 채운 뒤 CI 를 통과해 `https://chcbaram.github.io/posts/<slug>/` 에 발행된다.

### 한국어를 어디에 쓰나 (2026-09-27 확정)

**한국어판(`index.ko.md`)을 기본으로 만들지 않는다.** 한국어 창구는 네이버다.

| | 무엇 | 언제 |
| --- | --- | --- |
| 기본 | 영어 글 + **네이버에 한국어 짧은 소개(3~4문단) 와 링크**, 그리고 영어 글의 `naver_url` 채우기 | 글마다 |
| 예외 | `index.ko.md` 를 같이 만든다 | **WISH HE 시리즈만** |
| 하지 않음 | 그 밖의 글에 한국어판 | — |

**왜 기본이 "안 함" 인가**

- 이 문서의 채널 분담이 이미 "같은 글을 두 곳에 올리지 않는다" 다. `index.ko.md` 는 도메인만 같을 뿐 같은 글을 두 번 올리는 것이다.
- 한국어판은 번역이 아니라 **한국어로 다시 쓰기** 다(2026-09-27 에 그렇게 방침을 바꿨다). 글 한 편당 두 편을 쓰는 비용이다.
- **어긋남이 진짜 비용이다.** 영어 글의 수치를 고치면 한국어판도 고쳐야 하는데 `tools/check_posts.py` 는 언어 쌍을 대조하지 않는다. 한국어판에만 틀린 숫자가 남아도 아무도 모른다. 실제로 2026-09-27 에 QMK 글의 `keyboard_task` 수치를 실측 화면에 맞춰 고친 일이 있었다.
- 독자가 겹친다. 이 주제를 찾아 읽는 사람은 근거 자료(벤더 매뉴얼, QMK, SDK)가 영어뿐이라 이미 영어를 읽는다.

**왜 WISH HE 만 예외인가**

도는 보드가 Geonworks VENOM60HE 7U 와 EverGlide AE61 Pro 다. 커스텀 키보드, 특히 홀이펙트 개조는 한국 커뮤니티가 크고 Geonworks 는 한국 브랜드다. 이 시리즈는 한국어 독자가 1차 독자일 수 있다. titan-mini 나 nRF54L 코어는 반대다.

**이미 있는 한국어판 5편은 그대로 둔다.** 지우면 `/ko/` 주소가 깨진다. 다만 "계속 갈 방침" 이 아니라 **끝난 실험** 으로 본다. 영어 원본을 고치면 짝도 같이 고친다.

**이 방침은 데이터가 나오면 다시 본다.** 지금은 측정 수단이 없다 — 서치콘솔·서치어드바이저 인증값이 둘 다 비어 있다. 값이 들어가고 몇 달 지나면 `/ko/` 유입과 네이버 유입을 비교해 정한다.

## 발행 순서 (운영)

0. `BACKLOG.md` 에서 다음 글을 고른다.
1. Claude Code 에서 `/write-post <저장소> [주제]` 를 실행한다.
2. 초안의 `TODO(author)` 를 채우고, 동기나 경험을 한두 문단 보탠다.
3. `tools/import_photos.py` 로 사진을 넣고 `<!-- PHOTO: -->` 자리를 채운다.
4. `hugo server` 로 확인하고 `draft: false` 로 바꾼 뒤 push 한다.
5. 필요하면 네이버에 한국어 소개 글을 올리고, 영어 글의 `naver_url` 을 채운다.
6. `BACKLOG.md` 의 그 줄을 **발행됨** 으로 바꾸고 주소를 적는다. 줄을 지우지 않는다.

## 나에게 받아야 할 것

- **구글 서치콘솔, 네이버 서치어드바이저 인증 값** — 지금 둘 다 비어 있어 유입을 전혀 모른다. 한국어판 방침을 데이터로 정하려면 이게 먼저다 (단계 5)
- 프로필 사진, 한 줄 소개, About 페이지 내용
- 프로젝트 페이지로 만들 저장소 목록
- giscus 설정값 (단계 4)
- AI 학습용 봇 허용 여부 (단계 5)
- 글 라이선스 표시 여부 (단계 4)
- HEIC 사진 처리 방식 (단계 6)
- 예시 글용 nRF54L 보드 사진, 예제 동작 사진 (단계 8)
