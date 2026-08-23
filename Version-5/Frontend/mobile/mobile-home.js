(function () {
  const form = document.getElementById('home-form');
  const input = document.getElementById('home-input');
  if (!form || !input) return;

  function send(text) {
    text = (text || '').trim();
    if (!text) return;
    Heimdall.setPendingMessage(text);
    window.location.href = 'chat.html?new=1';
  }

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    send(input.value);
  });

  document.querySelectorAll('.mx-quick-chip').forEach((chip) => {
    chip.addEventListener('click', () => send(chip.getAttribute('data-quick')));
  });
})();
