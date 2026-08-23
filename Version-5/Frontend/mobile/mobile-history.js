(function () {
  const list = document.getElementById('history-list');
  const search = document.getElementById('history-search');

  function lastSnippet(conv) {
    if (!conv.messages.length) return 'No messages yet';
    const last = conv.messages[conv.messages.length - 1];
    return (last.role === 'user' ? '' : 'Heimdall: ') + last.content;
  }

  function render(filter) {
    const convs = Heimdall.getConversations();
    const q = (filter || '').trim().toLowerCase();
    const filtered = q
      ? convs.filter((c) => c.title.toLowerCase().includes(q) || lastSnippet(c).toLowerCase().includes(q))
      : convs;

    list.innerHTML = '';

    if (!filtered.length) {
      const empty = document.createElement('div');
      empty.className = 'mx-history-empty';
      empty.textContent = q ? 'No conversations match your search.' : 'No conversations yet. Start one from Home.';
      list.appendChild(empty);
      return;
    }

    filtered.forEach((c) => {
      const row = document.createElement('div');
      row.className = 'mx-history-row';
      row.innerHTML = `
        <div class="mx-history-icon">
          <svg viewBox="0 0 24 24" fill="none"><path d="M4 5h16v11H8l-4 4V5Z" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/></svg>
        </div>
        <div class="mx-history-text">
          <div class="mx-history-title">${Heimdall.escapeHtml(c.title || 'New conversation')}</div>
          <div class="mx-history-snippet">${Heimdall.escapeHtml(lastSnippet(c))}</div>
        </div>
        <div class="mx-history-meta">${Heimdall.relativeTime(c.updatedAt)}</div>
      `;
      row.addEventListener('click', () => {
        window.location.href = 'chat.html?id=' + encodeURIComponent(c.id);
      });
      list.appendChild(row);
    });
  }

  search.addEventListener('input', () => render(search.value));
  render('');
})();
