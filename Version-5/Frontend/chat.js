(function () {

  const convList = document.getElementById('conv-list');
  const chatScroll = document.getElementById('chat-scroll');
  const chatEmpty = document.getElementById('chat-empty');
  const chatForm = document.getElementById('chat-form');
  const chatInput = document.getElementById('chat-input');
  const searchField = document.getElementById('sidebar-search');
  const newChatBtn = document.getElementById('new-chat-btn');

  // =========================================================
  // API
  // =========================================================

  const API_URL =
    "https://heimdall-one-ebon.vercel.app/api/chat";

  let activeId = null;

  const params =
    new URLSearchParams(window.location.search);


  // =========================================================
  // SIDEBAR
  // =========================================================

  function renderSidebar(filter) {

    const list = Heimdall.getConversations();

    const q = (filter || '')
      .trim()
      .toLowerCase();

    const filtered = q
      ? list.filter((c) =>
          c.title.toLowerCase().includes(q)
        )
      : list;

    convList.innerHTML = '';

    if (!filtered.length) {

      const empty =
        document.createElement('div');

      empty.className =
        'history-row-snippet';

      empty.style.padding =
        '14px 8px';

      empty.textContent = q
        ? 'No conversations match your search.'
        : 'No conversations yet.';

      convList.appendChild(empty);

      return;
    }

    filtered.forEach((c) => {

      const item =
        document.createElement('div');

      item.className =
        'conv-item' +
        (c.id === activeId ? ' active' : '');

      item.innerHTML = `
        <span class="conv-item-title">
          ${Heimdall.escapeHtml(
            c.title || 'New conversation'
          )}
        </span>

        <span class="conv-item-meta">
          ${Heimdall.relativeTime(
            c.updatedAt
          )}
        </span>
      `;

      item.addEventListener(
        'click',
        () => {

          window.location.href =
            '/chat?id=' +
            encodeURIComponent(c.id);

        }
      );

      convList.appendChild(item);

    });

  }


  // =========================================================
  // RENDER MESSAGE
  // =========================================================

  function renderMessage(role, content) {

    chatEmpty.style.display = 'none';

    const row =
      document.createElement('div');

    row.className =
      'msg-row ' + role;

    const label =
      role === 'user'
        ? 'You'
        : 'Heimdall';

    row.innerHTML = `
      <span class="msg-label">
        ${label}
      </span>

      <div class="msg-bubble">
        ${content}
      </div>
    `;

    chatScroll.appendChild(row);

    chatScroll.scrollTop =
      chatScroll.scrollHeight;

    return row;

  }


  // =========================================================
  // RENDER CONVERSATION
  // =========================================================

  function renderConversation(conv) {

    chatScroll.innerHTML = '';

    if (!conv || !conv.messages.length) {

      chatScroll.appendChild(chatEmpty);

      chatEmpty.style.display = 'flex';

      return;

    }

    conv.messages.forEach((m) => {

      renderMessage(
        m.role,
        Heimdall.escapeHtml(m.content)
      );

    });

  }


  // =========================================================
  // PROCESSING INDICATOR
  // =========================================================

  function showProcessing() {

    const row =
      document.createElement('div');

    row.className =
      'processing-row';

    row.id =
      'processing-row';

    row.innerHTML = `
      <span class="processing-dot"></span>

      <span class="processing-text">
        HEIMDALL IS PROCESSING...
      </span>
    `;

    chatScroll.appendChild(row);

    chatScroll.scrollTop =
      chatScroll.scrollHeight;

    return row;

  }


  // =========================================================
  // AI RESPONSE
  // =========================================================

  async function respondTo(conv, userText) {

    const processingRow =
      showProcessing();

    try {

      const response =
        await fetch(API_URL, {

          method: 'POST',

          headers: {
            'Content-Type':
              'application/json'
          },

          body: JSON.stringify({
            message: userText
          })

        });


      let data;

      try {

        data =
          await response.json();

      } catch (error) {

        throw new Error(
          'Invalid response received.'
        );

      }


      if (!response.ok) {

        throw new Error(
          data.error ||
          'HEIMDALL returned an error.'
        );

      }


      const reply =
        data.response ||
        'No response received.';


      Heimdall.addMessage(
        conv.id,
        'assistant',
        reply
      );


      processingRow.remove();


      renderMessage(
        'assistant',
        Heimdall.escapeHtml(reply)
      );


      renderSidebar(
        searchField.value
      );


    } catch (error) {

      console.error(
        'HEIMDALL API ERROR:',
        error
      );


      processingRow.remove();


      const errorMessage =
        '⚠ Unable to reach HEIMDALL. Please try again.';


      Heimdall.addMessage(
        conv.id,
        'assistant',
        errorMessage
      );


      renderMessage(
        'assistant',
        Heimdall.escapeHtml(errorMessage)
      );


      renderSidebar(
        searchField.value
      );

    }

  }


  // =========================================================
  // LOAD CONVERSATION
  // =========================================================

  function loadConversation(id) {

    activeId = id;

    const conv =
      Heimdall.getConversation(id);

    if (!conv) return;

    renderConversation(conv);

    renderSidebar(
      searchField.value
    );

  }


  // =========================================================
  // CREATE NEW CHAT
  // =========================================================

  function createNewChat() {

    const conv =
      Heimdall.createConversation(
        'New conversation'
      );

    activeId = conv.id;

    history.replaceState(
      null,
      '',
      '/chat?id=' +
      encodeURIComponent(conv.id)
    );

    renderConversation(conv);

    renderSidebar(
      searchField.value
    );

    chatInput.focus();

  }


  // =========================================================
  // SEND MESSAGE
  // =========================================================

  chatForm.addEventListener(
    'submit',
    (event) => {

      event.preventDefault();

      const text =
        chatInput.value.trim();

      if (!text) return;


      chatInput.value = '';


      let conv;


      if (activeId) {

        conv =
          Heimdall.addMessage(
            activeId,
            'user',
            text
          );

      } else {

        conv =
          Heimdall.createConversation(text);

        conv =
          Heimdall.addMessage(
            conv.id,
            'user',
            text
          );

        activeId =
          conv.id;


        history.replaceState(
          null,
          '',
          '/chat?id=' +
          encodeURIComponent(conv.id)
        );

      }


      renderMessage(
        'user',
        Heimdall.escapeHtml(text)
      );


      renderSidebar(
        searchField.value
      );


      respondTo(
        conv,
        text
      );

    }
  );


  // =========================================================
  // NEW CHAT BUTTON
  // =========================================================

  if (newChatBtn) {

    newChatBtn.addEventListener(
      'click',
      createNewChat
    );

  }


  // =========================================================
  // SEARCH
  // =========================================================

  if (searchField) {

    searchField.addEventListener(
      'input',
      () => {

        renderSidebar(
          searchField.value
        );

      }
    );

  }


  // =========================================================
  // INITIALIZE
  // =========================================================

  const urlId =
    params.get('id');


  if (
    urlId &&
    Heimdall.getConversation(urlId)
  ) {

    loadConversation(urlId);

  } else {

    renderConversation(null);

    renderSidebar('');

  }

})();