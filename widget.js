/**
 * Cambridge Care Services - Official AI Care Assistant Web Widget
 * Host: https://cambridge-care-chatbot.streamlit.app
 */
(function() {
  if (document.getElementById("ccs-chatbot-root")) return;

  // 1. Create root container
  const root = document.createElement("div");
  root.id = "ccs-chatbot-root";

  // 2. Inject styles
  const style = document.createElement("style");
  style.textContent = `
    #ccs-chatbot-root {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      box-sizing: border-box;
    }
    #ccs-chatbot-root * {
      box-sizing: border-box;
    }
    #ccs-chat-bubble {
      position: fixed;
      bottom: 22px;
      right: 22px;
      width: 60px;
      height: 60px;
      border-radius: 50%;
      background: linear-gradient(145deg, #3A4046 0%, #282D32 100%);
      border: 2.5px solid #F66A71;
      box-shadow: 0 6px 22px rgba(246, 106, 113, 0.45), 0 4px 12px rgba(0,0,0,0.25);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 26px;
      cursor: pointer;
      z-index: 999999;
      transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.25s ease;
      user-select: none;
    }
    #ccs-chat-bubble:hover {
      transform: scale(1.08);
      box-shadow: 0 8px 28px rgba(246, 106, 113, 0.6), 0 6px 16px rgba(0,0,0,0.3);
    }
    #ccs-chat-bubble-badge {
      position: absolute;
      top: -3px;
      right: -3px;
      background: #F66A71;
      color: #FFFFFF;
      font-size: 11px;
      font-weight: 700;
      width: 20px;
      height: 20px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      border: 2px solid #FFFFFF;
      box-shadow: 0 2px 6px rgba(0,0,0,0.2);
    }
    #ccs-chat-greeting {
      display: none;
      position: fixed;
      bottom: 92px;
      right: 24px;
      background: #FFFFFF;
      color: #242A2E;
      padding: 12px 18px;
      border-radius: 16px;
      border: 1.5px solid #F66A71;
      box-shadow: 0 10px 30px rgba(0,0,0,0.15), 0 4px 10px rgba(246, 106, 113, 0.15);
      font-size: 13px;
      font-weight: 500;
      line-height: 1.4;
      max-width: 280px;
      cursor: pointer;
      z-index: 999998;
      animation: ccsFadeUp 0.35s ease-out;
    }
    #ccs-chat-greeting-close {
      position: absolute;
      top: -8px;
      right: -8px;
      background: #3A4046;
      color: #FFFFFF;
      border-radius: 50%;
      width: 20px;
      height: 20px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 11px;
      font-weight: bold;
      border: 1.5px solid #FFFFFF;
      cursor: pointer;
      box-shadow: 0 2px 6px rgba(0,0,0,0.2);
    }
    #ccs-chat-window {
      display: none;
      position: fixed;
      bottom: 92px;
      right: 22px;
      width: 440px;
      max-width: calc(100vw - 28px);
      height: 640px;
      max-height: calc(100vh - 110px);
      background: #FFFFFF;
      border-radius: 20px;
      border: 2.5px solid #F66A71;
      box-shadow: 0 16px 48px rgba(0,0,0,0.28), 0 4px 16px rgba(246, 106, 113, 0.25);
      z-index: 999999;
      overflow: hidden;
      animation: ccsPopIn 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }
    #ccs-chat-window iframe {
      width: 100%;
      height: 100%;
      border: none;
      display: block;
    }
    @keyframes ccsFadeUp {
      from { opacity: 0; transform: translateY(12px); }
      to { opacity: 1; transform: translateY(0); }
    }
    @keyframes ccsPopIn {
      from { opacity: 0; transform: scale(0.92) translateY(18px); }
      to { opacity: 1; transform: scale(1) translateY(0); }
    }
    @media (max-width: 480px) {
      #ccs-chat-window {
        bottom: 84px;
        right: 12px;
        width: calc(100vw - 24px);
        height: calc(100vh - 100px);
      }
      #ccs-chat-bubble {
        bottom: 16px;
        right: 16px;
        width: 54px;
        height: 54px;
        font-size: 23px;
      }
      #ccs-chat-greeting {
        bottom: 80px;
        right: 16px;
        max-width: calc(100vw - 40px);
      }
    }
  `;
  document.head.appendChild(style);

  // 3. Inject HTML markup
  root.innerHTML = `
    <!-- Gentle Greeting Pill -->
    <div id="ccs-chat-greeting">
      <span id="ccs-chat-greeting-close">✕</span>
      👋 <strong>Need care guidance?</strong><br>
      <span style="font-size: 11.5px; color: #555;">Tap to chat with our Cambridge Care Assistant</span>
    </div>

    <!-- Floating Bubble Button -->
    <div id="ccs-chat-bubble" title="Chat with Cambridge Care Assistant">
      <span id="ccs-chat-bubble-badge">1</span>
      <span id="ccs-bubble-icon">🌸</span>
    </div>

    <!-- Chat Window Container -->
    <div id="ccs-chat-window">
      <iframe 
        id="ccs-chat-iframe"
        src="about:blank"
        title="Cambridge Care Services Virtual Assistant"
        allow="clipboard-write">
      </iframe>
    </div>
  `;
  document.body.appendChild(root);

  // 4. Element references
  const bubble = document.getElementById("ccs-chat-bubble");
  const win = document.getElementById("ccs-chat-window");
  const greeting = document.getElementById("ccs-chat-greeting");
  const greetingClose = document.getElementById("ccs-chat-greeting-close");
  const icon = document.getElementById("ccs-bubble-icon");
  const badge = document.getElementById("ccs-chat-bubble-badge");
  const iframe = document.getElementById("ccs-chat-iframe");

  let isOpen = false;
  let iframeLoaded = false;

  function openChat() {
    isOpen = true;
    if (!iframeLoaded) {
      iframe.src = "https://cambridge-care-chatbot.streamlit.app/?embed=true";
      iframeLoaded = true;
    }
    win.style.display = "block";
    greeting.style.display = "none";
    badge.style.display = "none";
    icon.textContent = "✕";
  }

  function closeChat() {
    isOpen = false;
    win.style.display = "none";
    icon.textContent = "🌸";
  }

  bubble.addEventListener("click", function() {
    if (isOpen) {
      closeChat();
    } else {
      openChat();
    }
  });

  greeting.addEventListener("click", function(e) {
    if (e.target !== greetingClose) {
      openChat();
    }
  });

  greetingClose.addEventListener("click", function(e) {
    e.stopPropagation();
    greeting.style.display = "none";
  });

  // Show gentle greeting after 4.5 seconds on page load
  setTimeout(function() {
    if (!isOpen && greeting) {
      greeting.style.display = "block";
    }
  }, 4500);

})();
