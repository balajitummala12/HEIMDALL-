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
      empty.className = 'history-empty';
      empty.innerHTML = q
        ? 'No conversations match your search.'
        : 'No conversations yet. Start one from the Home page or Chat.';
      list.appendChild(empty);
      return;
    }

    filtered.forEach((c) => {
      const row = document.createElement('div');
      row.className = 'history-row';
      row.innerHTML = `
        <div class="history-row-left">
          <div class="history-icon">
            <svg viewBox="0 0 24 24" fill="none"><path d="M4 5h16v11H8l-4 4V5Z" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/></svg>
          </div>
          <div>
            <div class="history-row-title">${Heimdall.escapeHtml(c.title || 'New conversation')}</div>
            <div class="history-row-snippet">${Heimdall.escapeHtml(lastSnippet(c))}</div>
          </div>
        </div>
        <div class="history-row-meta">${Heimdall.relativeTime(c.updatedAt)}</div>
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
