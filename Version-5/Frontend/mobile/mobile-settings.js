(function () {
  const appearanceSel = document.getElementById('setting-appearance');
  const opacityInput = document.getElementById('setting-opacity');
  const opacityValue = document.getElementById('opacity-value');
  const energyToggle = document.getElementById('setting-energy');
  const modelSel = document.getElementById('setting-model');
  const voiceToggle = document.getElementById('setting-voice');
  const saveHint = document.getElementById('save-hint');

  const settings = Heimdall.getSettings();

  appearanceSel.value = settings.appearance;
  modelSel.value = settings.model;
  opacityInput.value = settings.opacity;
  opacityValue.textContent = settings.opacity + '%';
  opacityInput.style.setProperty('--val', settings.opacity + '%');
  setToggle(energyToggle, settings.energySaving);
  setToggle(voiceToggle, settings.voiceSync);

  function setToggle(el, on) {
    el.classList.toggle('on', !!on);
    el.setAttribute('aria-checked', on ? 'true' : 'false');
  }

  function flashSaved() {
    saveHint.textContent = 'Saved';
    saveHint.style.color = 'var(--cyan)';
    clearTimeout(flashSaved._t);
    flashSaved._t = setTimeout(() => {
      saveHint.textContent = 'Changes save automatically';
      saveHint.style.color = '';
    }, 1100);
  }

  appearanceSel.addEventListener('change', () => {
    Heimdall.saveSettings({ appearance: appearanceSel.value });
    flashSaved();
  });

  opacityInput.addEventListener('input', () => {
    opacityValue.textContent = opacityInput.value + '%';
    opacityInput.style.setProperty('--val', opacityInput.value + '%');
  });

  opacityInput.addEventListener('change', () => {
    Heimdall.saveSettings({ opacity: Number(opacityInput.value) });
    flashSaved();
  });

  energyToggle.addEventListener('click', () => {
    const next = !energyToggle.classList.contains('on');
    setToggle(energyToggle, next);
    Heimdall.saveSettings({ energySaving: next });
    flashSaved();
  });

  modelSel.addEventListener('click', () => {});
  modelSel.addEventListener('change', () => {
    Heimdall.saveSettings({ model: modelSel.value });
    flashSaved();
  });

  voiceToggle.addEventListener('click', () => {
    const next = !voiceToggle.classList.contains('on');
    setToggle(voiceToggle, next);
    Heimdall.saveSettings({ voiceSync: next });
    flashSaved();
  });
})();
