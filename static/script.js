// ================= CORE ELEMENTS =================
const chatBody = document.querySelector(".chat-body");
const messageInput = document.querySelector(".message-input");
const sendMessageButton = document.querySelector("#send-message");
const chatForm = document.querySelector(".chat-form");

// ================= USER DATA =================
const userData = {
  message: null,
};

const initialInputHeight = messageInput.scrollHeight;

// ================= UTIL =================
const createMessageElement = (content, ...classes) => {
  const div = document.createElement("div");
  div.classList.add("message", ...classes);
  div.innerHTML = content;
  return div;
};

// ================= BOT RESPONSE =================
const generateBotResponse = async (incomingMessageDiv) => {
  const messageElement = incomingMessageDiv.querySelector(".message-text");

  try {
    const response = await fetch("/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: userData.message }),
    });

    const data = await response.json();
    messageElement.innerText = data.answer;
  } catch (error) {
    messageElement.innerText = "Server error ❌";
    messageElement.style.color = "red";
  } finally {
    incomingMessageDiv.classList.remove("thinking");
    chatBody.scrollTo({ top: chatBody.scrollHeight, behavior: "smooth" });
  }
};

// ================= SEND MESSAGE =================
const handleOutgoingMessage = (e) => {
  e.preventDefault();

  userData.message = messageInput.value.trim();
  if (!userData.message) return;

  messageInput.value = "";
  messageInput.dispatchEvent(new Event("input"));

  // User message
  const outgoingMessageDiv = createMessageElement(
    `<div class="message-text">${userData.message}</div>`,
    "user-message"
  );

  chatBody.appendChild(outgoingMessageDiv);
  chatBody.scrollTo({ top: chatBody.scrollHeight });

  // Bot thinking
  setTimeout(() => {
    const incomingMessageDiv = createMessageElement(
      `<div class="message-text">
        <div class="thinking-indicator">
          <div class="dot"></div>
          <div class="dot"></div>
          <div class="dot"></div>
        </div>
      </div>`,
      "bot-message",
      "thinking"
    );

    chatBody.appendChild(incomingMessageDiv);
    chatBody.scrollTo({ top: chatBody.scrollHeight });

    generateBotResponse(incomingMessageDiv);
  }, 500);
};

// ================= EVENTS =================
chatForm.addEventListener("submit", handleOutgoingMessage);

messageInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    handleOutgoingMessage(e);
  }
});

messageInput.addEventListener("input", () => {
  messageInput.style.height = `${initialInputHeight}px`;
  messageInput.style.height = `${messageInput.scrollHeight}px`;
});
