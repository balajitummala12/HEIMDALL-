(function () {

  const chatScroll = document.getElementById('chat-scroll');
  const chatEmpty = document.getElementById('chat-empty');
  const chatForm = document.getElementById('chat-form');
  const chatInput = document.getElementById('chat-input');
  const chatTitle = document.getElementById('chat-title');

  // =========================================================
  // REAL HEIMDALL BACKEND
  // =========================================================

  const API_URL =
    "https://heimdall-one-ebon.vercel.app/api/chat";


  let activeId = null;

  const params =
    new URLSearchParams(window.location.search);


  // =========================================================
  // SCROLL
  // =========================================================

  function scrollToBottom() {

    chatScroll.scrollTop =
      chatScroll.scrollHeight;

  }


  // =========================================================
  // RENDER MESSAGE
  // =========================================================

  function renderMessage(
    role,
    contentHtml
  ) {

    chatEmpty.style.display = 'none';

    const row =
      document.createElement('div');

    row.className =
      'mx-msg-row ' + role;

    const label =
      role === 'user'
        ? 'You'
        : 'Heimdall';


    row.innerHTML = `
      <span class="mx-msg-label">
        ${label}
      </span>

      <div class="mx-msg-bubble">
        ${contentHtml}
      </div>
    `;


    chatScroll.appendChild(row);

    scrollToBottom();

    return row;

  }


  // =========================================================
  // RENDER CONVERSATION
  // =========================================================

  function renderConversation(conv) {

    chatScroll.innerHTML = '';

    if (
      !conv ||
      !conv.messages.length
    ) {

      chatScroll.appendChild(
        chatEmpty
      );

      chatEmpty.style.display = 'flex';

      chatTitle.textContent =
        'HEIMDALL';

      return;

    }


    chatTitle.textContent =
      conv.title ||
      'HEIMDALL';


    conv.messages.forEach((m) => {

      renderMessage(
        m.role,
        Heimdall.escapeHtml(
          m.content
        )
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
      'mx-processing-row';

    row.id =
      'mx-processing-row';


    row.innerHTML = `
      <span class="scan-ring"></span>

      <span class="mx-processing-text">
        HEIMDALL IS PROCESSING...
      </span>
    `;


    chatScroll.appendChild(row);

    scrollToBottom();

    return row;

  }


  // =========================================================
  // REAL HEIMDALL RESPONSE
  // =========================================================

  async function respondTo(
    conv,
    userText
  ) {

    const processingRow =
      showProcessing();


    try {

      const response =
        await fetch(
          API_URL,
          {
            method: 'POST',

            headers: {
              'Content-Type':
                'application/json'
            },

            body: JSON.stringify({
              message: userText
            })
          }
        );


      let data;


      try {

        data =
          await response.json();

      } catch (error) {

        throw new Error(
          'Invalid response from the HEIMDALL AI core.'
        );

      }


      if (!response.ok) {

        throw new Error(
          data.error ||
          'HEIMDALL AI core returned an error.'
        );

      }


      const reply =
        data.response ||
        'HEIMDALL did not return a response.';


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


      chatTitle.textContent =
        Heimdall.getConversation(
          conv.id
        ).title ||
        'HEIMDALL';


    } catch (error) {

      console.error(
        'HEIMDALL API ERROR:',
        error
      );


      processingRow.remove();


      const errorMessage =
        '⚠️ Unable to connect to the HEIMDALL AI core. ' +
        'Error: ' +
        error.message;


      Heimdall.addMessage(
        conv.id,
        'assistant',
        errorMessage
      );


      renderMessage(
        'assistant',
        Heimdall.escapeHtml(
          errorMessage
        )
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


    renderConversation(conv);


    if (
      conv &&
      conv.messages.length > 0 &&
      conv.messages[
        conv.messages.length - 1
      ].role === 'user'
    ) {

      respondTo(
        conv,
        conv.messages[
          conv.messages.length - 1
        ].content
      );

    }

  }


  // =========================================================
  // PENDING MESSAGE
  // =========================================================

  function startNewFromPending() {

    const pending =
      Heimdall.consumePendingMessage();


    if (!pending)
      return false;


    const conv =
      Heimdall.createConversation(
        pending
      );


    Heimdall.addMessage(
      conv.id,
      'user',
      pending
    );


    loadConversation(
      conv.id
    );


    history.replaceState(
      null,
      '',
      'chat.html?id=' +
      encodeURIComponent(
        conv.id
      )
    );


    return true;

  }


  // =========================================================
  // SEND MESSAGE
  // =========================================================

  chatForm.addEventListener(
    'submit',
    (e) => {

      e.preventDefault();


      const text =
        chatInput.value.trim();


      if (!text)
        return;


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
          Heimdall.createConversation(
            text
          );


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
          'chat.html?id=' +
          encodeURIComponent(
            conv.id
          )
        );

      }


      renderMessage(
        'user',
        Heimdall.escapeHtml(text)
      );


      chatTitle.textContent =
        conv.title ||
        'HEIMDALL';


      respondTo(
        conv,
        text
      );

    }
  );


  // =========================================================
  // MOBILE KEYBOARD
  // =========================================================

  if (window.visualViewport) {

    window.visualViewport.addEventListener(
      'resize',
      scrollToBottom
    );

  }


  // =========================================================
  // INIT
  // =========================================================

  const urlId =
    params.get('id');


  if (
    urlId &&
    Heimdall.getConversation(urlId)
  ) {

    loadConversation(urlId);

  } else if (
    !startNewFromPending()
  ) {

    renderConversation(null);

  }

})();