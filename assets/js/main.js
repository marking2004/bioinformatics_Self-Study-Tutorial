// 主题切换
(function () {
  var btn = document.getElementById('theme-toggle');
  if (btn) {
    btn.addEventListener('click', function () {
      var cur = document.documentElement.getAttribute('data-theme');
      var next = cur === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      try { localStorage.setItem('theme', next); } catch (e) {}
    });
  }

  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();
})();

// 文章搜索过滤（首页模块卡片）
(function () {
  var input = document.getElementById('search');
  var list = document.getElementById('post-list');
  var empty = document.getElementById('no-result');
  if (!input || !list) return;

  input.addEventListener('input', function () {
    var q = input.value.trim().toLowerCase();
    var cards = list.querySelectorAll('.post-card');
    var shown = 0;
    cards.forEach(function (card) {
      var title = (card.getAttribute('data-title') || card.textContent).toLowerCase();
      var hit = !q || title.indexOf(q) !== -1;
      card.style.display = hit ? '' : 'none';
      if (hit) shown++;
    });
    if (empty) empty.hidden = shown !== 0;
  });
})();
