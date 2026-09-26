---
title: "Setting Up a Hugo Blog for Firmware Notes"
date: 2026-09-27T02:30:14+09:00
description: "How this site is built: Hugo with the Stack theme, deployed from GitHub Actions, with a checker that refuses to publish a post that still has holes in it."
projects: ["chcbaram.github.io"]
tags: ["hugo", "github-actions", "tooling"]
series: []
repo: "https://github.com/chcbaram/chcbaram.github.io"
image: ""
ai_assisted: true
naver_url: ""
draft: true
---

I keep notes while working on firmware and boards, and until now they stayed in
commit messages and scratch files. This site is where the English write-ups go.
This first post is about how the site itself is put together, because the setup
has a few pieces that took some reading to get right.

## What I wanted

- Posts live at a stable URL. If I later change how I file them, the URL stays.
- Each post is one folder, with its photos next to it.
- A post cannot be published while it still has an unanswered question in it.

## Structure

Every post is a page bundle under `content/posts/<slug>/`, and nothing else.
There are no category folders, because moving a post between folders would change
its URL. Instead a post declares which repository it is about:

```yaml
projects: ["baram-nrf54-arduino"]
tags: ["nrf54l", "ble", "arduino"]
```

`projects` is a Hugo taxonomy, so `/projects/baram-nrf54-arduino/` lists every
post about that repository, and the description on that page comes from
`content/projects/<name>/_index.md`.

## The part that surprised me

The Stack theme ships with `mainSections = ["post"]` — singular. My posts are in
`content/posts/`, plural, so the homepage came up empty with no error. The fix is
one line:

```toml
[params]
    mainSections = ["posts"]
```

The theme also already has a generic taxonomy widget, so the Projects list in the
sidebar needs configuration rather than a new template:

```toml
[[params.widgets.homepage]]
    type = "taxonomy"
    [params.widgets.homepage.params]
        taxonomy = "projects"
        title    = "Projects"
```

<!-- PHOTO: sidebar screenshot showing the Projects widget with a few entries -->

## A checker in front of the deploy

Drafts here start out with holes in them on purpose: `TODO(author):` where I need
to answer something, and `<!-- PHOTO: ... -->` where a photo belongs. That only
works if something stops a half-finished post from going out, so
`tools/check_posts.py` runs before the build in CI and fails on:

- a publishable post that still contains `TODO(author)` or `<!-- PHOTO:`
- an empty `description`
- an `image` that names a file which is not in the post folder

Because Hugo treats a missing `draft` key as published, the checker looks at
every post that is not explicitly `draft: true` rather than only at
`draft: false`.

## Video and photos

Photos go through `tools/import_photos.py`, which shrinks them to 2000px on the
long edge, applies the EXIF rotation, and strips the rest of the EXIF. Short
clips are committed as mp4 and embedded with a shortcode that overrides the
theme's, to add `playsinline` and `preload="metadata"`:

```
{{</* video "clip.mp4" */>}}
```

Anything longer than about 30 seconds goes to YouTube instead, to keep the
repository small.

## What's next

- <!-- TODO(author): 첫 기술 글 주제를 정한다 --> the first real post, about a
  project rather than about this site
- Korean translations as a second Hugo language, if it turns out I want them

## Links

- [This site's repository](https://github.com/chcbaram/chcbaram.github.io)
- [Hugo Stack theme](https://github.com/CaiJimmy/hugo-theme-stack)

<!--
sources:
- hugo.toml (this repository)
- tools/check_posts.py, tools/import_photos.py (this repository)
- github.com/CaiJimmy/hugo-theme-stack v4.0.3: config/_default/params.toml, layouts/_partials/widget/taxonomy.html
-->
