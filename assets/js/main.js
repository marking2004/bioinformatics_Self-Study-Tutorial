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

// 文章搜索过滤（首页：课程模块卡片 + 实验卡片）
(function () {
  var input = document.getElementById('search');
  var lists = [document.getElementById('post-list'), document.getElementById('lab-list')].filter(Boolean);
  var empty = document.getElementById('no-result');
  if (!input || !lists.length) return;

  input.addEventListener('input', function () {
    var q = input.value.trim().toLowerCase();
    var shown = 0;
    lists.forEach(function (list) {
      var cards = list.querySelectorAll('.post-card');
      cards.forEach(function (card) {
        var title = (card.getAttribute('data-title') || card.textContent).toLowerCase();
        var hit = !q || title.indexOf(q) !== -1;
        card.style.display = hit ? '' : 'none';
        if (hit) shown++;
      });
    });
    if (empty) empty.hidden = shown !== 0;
  });
})();
