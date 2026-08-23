(function () {
  const form = document.getElementById('home-form');
  const input = document.getElementById('home-input');
  if (!form || !input) return;

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const text = input.value.trim();
    if (!text) return;
    Heimdall.setPendingMessage(text);
    window.location.href = 'chat.html?new=1';
  });
})();
