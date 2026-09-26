---
description: 내 저장소 작업 내용을 바탕으로 영어 블로그 글 초안(draft)을 만든다
argument-hint: <저장소 이름 또는 로컬 경로> [주제]
---

# /write-post

인자: `$ARGUMENTS`

첫 번째 인자는 저장소(`chcbaram/<name>`, `<name>`, 또는 로컬 경로), 나머지는 주제다.
이 명령은 `CLAUDE.md` 의 "글 재료와 공개 범위", "글 내용의 사실성", "글 작성 원칙" 을 따른다.

## 0. 작업 위치

저장소 두 개가 동시에 나온다. 헷갈리지 않게 구분한다.

| 이름 | 무엇 | 하는 일 |
| --- | --- | --- |
| **블로그 저장소** | 이 명령을 실행한 현재 디렉터리 (`chcbaram.github.io`) | 글과 프로젝트 페이지를 쓰고, `tools/` 를 실행한다 |
| **재료 저장소** | 인자로 받은 저장소 | 읽기만 한다. 절대 고치지 않는다 |

파일을 만들거나 고치는 것은 **블로그 저장소 안에서만** 한다.

## 1. 저장소 확인

- 로컬 경로면 그대로 쓴다.
- 이름이면 `gh repo view chcbaram/<name> --json name,description,visibility,url,defaultBranchRef` 로 확인한다.
- **로컬 클론을 먼저 찾는다: `~/hdd/git/<name>`.** 대부분 여기에 이미 있다. 없을 때만 `/tmp/write-post/<name>` 에 `git clone --filter=blob:none` 으로 받는다. 전체 `git log` 가 필요하므로 `--depth 1` 은 쓰지 않는다.
- `visibility` 가 PUBLIC 이 아니면 **멈추고** 나에게 진행 여부를 묻는다.
- 기준 커밋 해시를 기록한다. 코드 permalink 는 이 해시로 만든다.
  - **로컬 `HEAD` 가 아니라 `git rev-parse origin/<기본 브랜치>` 를 쓴다.** 로컬에만 있는 커밋으로 permalink 를 만들면 GitHub 에서 404 가 난다.
  - 로컬 클론을 쓸 때는 `git fetch origin` 을 먼저 하고, 작업 트리가 더러우면 그 상태를 보고에 적는다.

## 2. 재료 읽기

다음 순서로 읽고, 읽은 파일과 커밋 목록을 기록해 둔다.

1. README, `docs/` 폴더, `decisions.md` · `roadmap.md` · `architecture.md` 같은 설계 문서
2. `git log --oneline` 전체와, 주제와 관련된 커밋의 본문
3. 주제와 관련된 코드
4. 릴리스 노트, 이슈 (`gh release list`, `gh issue list --state all`)
5. 저장소 안의 비공개 규칙 문서가 있으면 먼저 읽고 따른다

## 3. 주제 정하기

- 주제가 인자로 주어졌으면 그대로 쓴다.
- 주제가 없으면 글감 후보 3개를 제목, 한 줄 요약, 근거 파일과 함께 제시하고 **멈춘다.** 내가 고르면 이어간다.
- 이미 `content/posts/` 에 같은 프로젝트·같은 주제의 글이 있으면 알려주고, 후속 글로 쓸지 묻는다.

## 4. 초안 작성

- `tools/new_post.sh` 로 `content/posts/<slug>/index.md` 를 만든다 (블로그 저장소에서 실행). slug 는 영어 소문자와 하이픈, 5단어 안팎.
- **같은 slug 폴더가 이미 있으면 덮어쓰지 않고 멈춘다.** 다른 slug 를 제안한다.
- front matter: `draft: true`, `ai_assisted: true`, `projects`, `repo`, `tags`, `description` 을 채운다. `date` 는 오늘, `image` 는 빈 문자열로 둔다 (사진은 내가 나중에 넣는다).
- `content/projects/<name>/_index.md` 가 없으면 README 를 바탕으로 짧게 만든다 (이것도 사실만).
- 본문은 `CLAUDE.md` 의 글 작성 원칙을 따른다.
- 근거가 없는 내용은 `TODO(author): ...` 로 남긴다. 특히 다음은 반드시 질문으로 남긴다.
  - 이 프로젝트를 시작한 이유
  - 고려했다가 버린 대안이 있는데 이유가 문서에 없을 때
  - 측정 조건이 기록에 없을 때
- 사진이 필요한 자리에 `<!-- PHOTO: ... -->` 를 넣는다. 글 하나에 사진 자리 2~6개.
- 본문 끝에 렌더링되지 않는 주석으로 출처를 남긴다.

  ```
  <!--
  sources (commit abc1234):
  - docs/decisions.md
  - src/retro_ui/graph.py
  - commits: 1a2b3c4, 5d6e7f8
  -->
  ```

## 5. 자체 점검

제출 전에 스스로 확인한다.

- `tools/check_posts.py --all` 이 통과하는가. (draft 라서 그냥 넘어가지 않도록 `--all` 로 돌린다.)
- 본문의 모든 수치와 기술적 주장이 출처 파일에 있는가. 없으면 TODO 로 바꾼다. 단, `TODO(author)` 와 `<!-- PHOTO: -->` 는 draft 단계에서는 남아 있는 게 정상이므로 `--all` 의 이 두 항목 실패는 보고만 하고 넘어간다.
- 코드 발췌가 실제 파일 내용과 일치하는가. permalink 가 기준 커밋(`origin/<기본 브랜치>`)을 가리키는가. 링크를 하나 열어 확인한다.
- 개인 경로, 시리얼, 토큰, 장치 식별 정보가 없는가.
- 금지 표현이 없는가.
- 본문 길이가 800~1500 단어 범위인가.
- `hugo --buildDrafts` 빌드가 성공하는가.

## 6. 보고

나에게 다음만 짧게 보고한다. 본문 전체를 다시 출력하지 않는다.

- 글 경로와 제목, 단어 수
- 재료 저장소 경로와 기준 커밋이 origin 에 있는 커밋인지 여부
- `TODO(author)` 목록 (질문 형태 그대로)
- `<!-- PHOTO: -->` 목록
- 참고한 주요 파일과 기준 커밋
