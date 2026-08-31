(function () {
  'use strict';

  var widget = document.getElementById('chatbotWidget');
  if (!widget) return;

  var toggle = document.getElementById('chatbotToggle');
  var panel = document.getElementById('chatbotPanel');
  var closeBtn = document.getElementById('chatbotClose');
  var form = document.getElementById('chatbotForm');
  var input = document.getElementById('chatbotInput');
  var messages = document.getElementById('chatbotMessages');

  function getCookie(name) {
    var value = '; ' + document.cookie;
    var parts = value.split('; ' + name + '=');
    if (parts.length === 2) return parts.pop().split(';').shift();
    return '';
  }

  function addMessage(text, sender) {
    var el = document.createElement('div');
    el.className = 'chatbot-message chatbot-message-' + sender;
    el.textContent = text;
    messages.appendChild(el);
    messages.scrollTop = messages.scrollHeight;
  }

  toggle.addEventListener('click', function () {
    panel.hidden = !panel.hidden;
    if (!panel.hidden) input.focus();
  });
  closeBtn.addEventListener('click', function () { panel.hidden = true; });

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var text = input.value.trim();
    if (!text) return;
    addMessage(text, 'user');
    input.value = '';

    fetch('/chatbot/reply/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      body: JSON.stringify({ message: text }),
    })
      .then(function (res) { return res.json(); })
      .then(function (data) {
        addMessage(data.reply || "I don't have that information in Maryam's portfolio yet.", 'bot');
      })
      .catch(function () {
        addMessage("Sorry, something went wrong. Please try again.", 'bot');
      });
  });
})();
