/* ==========================================================================
   HEIMDALL — Shared App Logic
   Navigation state, settings application, conversation store.
   ========================================================================== */

const Heimdall = (function () {

  // ============================================================
  // UNIQUE DEVICE / BROWSER ID
  // ============================================================

  const DEVICE_ID_KEY = 'heimdall_device_id';


  function getDeviceId() {

    let deviceId =
      localStorage.getItem(DEVICE_ID_KEY);


    // Create a unique ID for this browser/device
    if (!deviceId) {

      deviceId =
        'device_' +
        Date.now().toString(36) +
        '_' +
        Math.random()
          .toString(36)
          .slice(2, 12);


      localStorage.setItem(
        DEVICE_ID_KEY,
        deviceId
      );

    }


    return deviceId;

  }


  const DEVICE_ID =
    getDeviceId();


  // ============================================================
  // DEVICE-SPECIFIC STORAGE KEYS
  // ============================================================

  const STORE_KEY =
    'heimdall_conversations_' +
    DEVICE_ID;


  const SETTINGS_KEY =
    'heimdall_settings_' +
    DEVICE_ID;


  const PENDING_KEY =
    'heimdall_pending_message_' +
    DEVICE_ID;


  // ============================================================
  // DEFAULT SETTINGS
  // ============================================================

  const defaultSettings = {

    appearance: 'deep-space',

    opacity: 85,

    energySaving: false,

    model: 'heimdall-core',

    voiceSync: false,

  };


  // ============================================================
  // SETTINGS
  // ============================================================

  function getSettings() {

    try {

      return {

        ...defaultSettings,

        ...JSON.parse(
          localStorage.getItem(
            SETTINGS_KEY
          ) || '{}'
        ),

      };

    }

    catch (e) {

      return {
        ...defaultSettings
      };

    }

  }


  function saveSettings(next) {

    const merged = {

      ...getSettings(),

      ...next,

    };


    localStorage.setItem(
      SETTINGS_KEY,
      JSON.stringify(merged)
    );


    localStorage.setItem(
      'heimdall_energy_saving',
      merged.energySaving
        ? 'on'
        : 'off'
    );


    applySettings(merged);


    window.dispatchEvent(

      new CustomEvent(
        'heimdall:settings-changed'
      )

    );


    return merged;

  }


  function applySettings(settings) {

    settings =
      settings || getSettings();


    document.documentElement.style.setProperty(

      '--ui-opacity',

      (
        settings.opacity / 100
      ).toFixed(2)

    );


    document.body.classList.toggle(

      'energy-saving',

      !!settings.energySaving

    );


    const shell =
      document.querySelector(
        '.app-shell'
      );


    if (shell) {

      shell.style.opacity =
        String(
          0.55 +
          (
            settings.opacity / 100
          ) * 0.45
        );

    }

  }


  // ============================================================
  // CONVERSATIONS
  // ============================================================

  function getConversations() {

    try {

      return JSON.parse(

        localStorage.getItem(
          STORE_KEY
        ) || '[]'

      );

    }

    catch (e) {

      return [];

    }

  }


  function saveConversations(list) {

    localStorage.setItem(

      STORE_KEY,

      JSON.stringify(list)

    );

  }


  function createConversation(firstMessage) {

    const list =
      getConversations();


    const id =

      'c_' +

      Date.now()
        .toString(36) +

      Math.random()
        .toString(36)
        .slice(2, 8);


    const title =

      (
        firstMessage ||
        'New conversation'
      ).slice(0, 48);


    const conv = {

      id,

      title,

      messages: [],

      createdAt:
        Date.now(),

      updatedAt:
        Date.now(),

    };


    list.unshift(conv);


    saveConversations(list);


    return conv;

  }


  function getConversation(id) {

    return (

      getConversations()

        .find(
          (c) =>
            c.id === id
        )

      ||

      null

    );

  }


  function addMessage(
    id,
    role,
    content
  ) {

    const list =
      getConversations();


    const conv =

      list.find(
        (c) =>
          c.id === id
      );


    if (!conv) {

      return null;

    }


    conv.messages.push({

      role,

      content,

      time:
        Date.now(),

    });


    conv.updatedAt =
      Date.now();


    // Set conversation title from first user message
    if (

      role === 'user' &&

      conv.messages.filter(
        (m) =>
          m.role === 'user'
      ).length === 1

    ) {

      conv.title =
        content.slice(0, 48);

    }


    saveConversations(list);


    return conv;

  }


  // ============================================================
  // PENDING MESSAGE
  // ============================================================

  function setPendingMessage(text) {

    localStorage.setItem(
      PENDING_KEY,
      text
    );

  }


  function consumePendingMessage() {

    const value =

      localStorage.getItem(
        PENDING_KEY
      );


    localStorage.removeItem(
      PENDING_KEY
    );


    return value;

  }


  // ============================================================
  // RELATIVE TIME
  // ============================================================

  function relativeTime(ts) {

    const diff =
      Date.now() - ts;


    const min =
      Math.floor(
        diff / 60000
      );


    if (min < 1) {

      return 'just now';

    }


    if (min < 60) {

      return `${min}m ago`;

    }


    const hr =
      Math.floor(
        min / 60
      );


    if (hr < 24) {

      return `${hr}h ago`;

    }


    const day =
      Math.floor(
        hr / 24
      );


    if (day < 7) {

      return `${day}d ago`;

    }


    return new Date(ts)
      .toLocaleDateString(

        undefined,

        {
          month: 'short',
          day: 'numeric',
        }

      );

  }


  // ============================================================
  // ESCAPE HTML
  // ============================================================

  function escapeHtml(str) {

    const div =
      document.createElement('div');


    div.textContent =
      String(str);


    return div.innerHTML;

  }


  // ============================================================
  // NAVIGATION
  // ============================================================

  function initNav() {

    const page =
      document.body.getAttribute(
        'data-page'
      );


    document
      .querySelectorAll(
        '.hx-navlinks a'
      )
      .forEach((a) => {

        if (

          a.getAttribute(
            'data-nav'
          ) === page

        ) {

          a.classList.add(
            'active'
          );

        }

      });

  }


  // ============================================================
  // INITIALIZATION
  // ============================================================

  function init() {

    initNav();

    applySettings();

  }


  if (

    document.readyState ===
    'loading'

  ) {

    document.addEventListener(

      'DOMContentLoaded',

      init

    );

  }

  else {

    init();

  }


  // ============================================================
  // PUBLIC API
  // ============================================================

  return {

    getSettings,

    saveSettings,

    applySettings,

    getConversations,

    saveConversations,

    createConversation,

    getConversation,

    addMessage,

    setPendingMessage,

    consumePendingMessage,

    relativeTime,

    escapeHtml,

  };

})();