/*
 * 댓글 수를 GitHub Discussions 에서 읽어 화면에 붙인다.
 *
 * giscus 가 mapping = "pathname" 으로 동작하므로 Discussion 제목이 글 주소와 같다.
 * (/posts/<slug>/ · 한국어 글은 /ko/posts/<slug>/)
 *
 * - 목록(홈·아카이브)과 글 화면의 링크 옆에 "댓글 N" 배지를 붙인다
 * - 사이드바 위젯에 최근 댓글이 달린 글을 나열한다
 *
 * 토큰 없이 부르는 공개 API 라 IP 당 시간당 60회 제한이 있다.
 * 그래서 응답을 localStorage 에 TTL 을 두고 캐시한다.
 * 실패하면 아무것도 하지 않는다 — 배지가 없을 뿐 화면은 그대로다.
 */
(function () {
  var cfg = window.__commentsCfg || {};
  var repo = cfg.repo;
  if (!repo) return;

  var TTL = (cfg.ttl || 300) * 1000;
  var KEY = 'discussions:' + repo;

  function cached() {
    try {
      var raw = localStorage.getItem(KEY);
      if (!raw) return null;
      var box = JSON.parse(raw);
      if (Date.now() - box.at > TTL) return null;
      return box.data;
    } catch (e) { return null; }
  }

  function store(data) {
    try {
      localStorage.setItem(KEY, JSON.stringify({ at: Date.now(), data: data }));
    } catch (e) { /* 사생활 보호 모드 등 — 캐시 없이 간다 */ }
  }

  var titles = {};

  function render(list) {
    if (!Array.isArray(list) || !list.length) return;

    var byPath = {};
    list.forEach(function (d) {
      if (!d || typeof d.title !== 'string') return;
      if (d.title.charAt(0) !== '/') return;       // giscus 가 만든 것만
      byPath[d.title] = d;
    });

    /* 1. 목록과 글 화면의 메타 줄에 배지 */
    document.querySelectorAll('article, .main-article').forEach(function (art) {
      var meta = art.querySelector('.article-meta');
      if (!meta || meta.querySelector('.comment-count')) return;

      var link = art.querySelector('.article-title a[href]') || art.querySelector('a[href]');
      var path = link ? new URL(link.href, location.origin).pathname : location.pathname;
      if (art.classList.contains('main-article')) path = location.pathname;

      var d = byPath[path];
      if (!d || !d.comments) return;

      var a = document.createElement('a');
      a.className = 'comment-count';
      a.href = d.html_url;
      a.rel = 'noopener';
      a.target = '_blank';
      a.title = cfg.viewOnGitHub || 'View on GitHub';
      a.textContent = (cfg.label || 'comments') + ' ' + d.comments;
      a.addEventListener('click', function (ev) { ev.stopPropagation(); });
      (meta.querySelector('.inline-meta') || meta).appendChild(a);
    });

    /* 2. 사이드바 위젯 */
    var widget = document.getElementById('recent-comments');
    if (widget) {
      var recent = list
        .filter(function (d) { return d.comments > 0 && typeof d.title === 'string' && d.title.charAt(0) === '/'; })
        .sort(function (a, b) { return new Date(b.updated_at) - new Date(a.updated_at); })
        .slice(0, cfg.limit || 5);

      if (recent.length) {
        var ol = widget.querySelector('.recent-comments-list');
        recent.forEach(function (d) {
          var li = document.createElement('li');
          var a = document.createElement('a');
          a.href = d.title;                       /* 글 주소 그대로다 */
          a.textContent = titles[d.title] || d.title;
          var n = document.createElement('span');
          n.className = 'recent-comments-count';
          n.textContent = d.comments;
          li.appendChild(a);
          li.appendChild(n);
          ol.appendChild(li);
        });
        widget.hidden = false;
      }
    }
  }

  /* 글 제목은 테마가 이미 만드는 검색 색인에서 가져온다 */
  function withTitles(done) {
    if (!cfg.searchIndex) { done(); return; }
    fetch(cfg.searchIndex)
      .then(function (r) { return r.ok ? r.json() : []; })
      .then(function (idx) {
        (idx || []).forEach(function (p) { if (p.permalink) titles[p.permalink] = p.title; });
      })
      .catch(function () {})
      .then(done, done);
  }

  var hit = cached();
  if (hit) {
    withTitles(function () { render(hit); });
    return;
  }

  fetch('https://api.github.com/repos/' + repo + '/discussions?per_page=100', {
    headers: { Accept: 'application/vnd.github+json' }
  })
    .then(function (r) { return r.ok ? r.json() : null; })
    .then(function (data) {
      if (!data) return;
      var slim = data.map(function (d) {
        return { title: d.title, comments: d.comments, html_url: d.html_url, updated_at: d.updated_at };
      });
      store(slim);
      withTitles(function () { render(slim); });
    })
    .catch(function () { /* 조용히 포기한다 */ });
})();
