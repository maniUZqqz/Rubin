// المان‌های DOM
const chatMessagesEl = document.getElementById("chatMessages");
const chatInputEl = document.getElementById("chatInput");

// تابع ارسال پیام کاربر
function sendMessage() {
    const userMsg = chatInputEl.value.trim();
    if (!userMsg) return;

    appendMessage(userMsg, "user-bubble");
    chatInputEl.value = "";

    // شبیه‌سازی تاخیر برای پاسخ ربات
    setTimeout(() => {
        const botMsg = getBotResponse(userMsg);
        appendMessage(botMsg, "bot-bubble");
    }, 600);
}

// افزودن حباب چت در chatMessages
function appendMessage(text, bubbleClass) {
    const bubble = document.createElement("div");
    bubble.classList.add("chat-bubble", bubbleClass);
    bubble.textContent = text;
    chatMessagesEl.appendChild(bubble);

    // اسکرول به انتهای چت
    chatMessagesEl.scrollTop = chatMessagesEl.scrollHeight;
}

// پاسخ ساده ربات براساس کلمات کلیدی
function getBotResponse(question) {
    const q = question.toLowerCase();
    if (q.includes("سلام")) {
        return "سلام! چطور می‌تونم کمکتون کنم؟";
    } else if (q.includes("خداحافظ")) {
        return "روزت بخیر!";
    } else if (q.includes("دانشجو") || q.includes("student")) {
        return "برای دیدن لیست دانشجویان، به بخش Students مراجعه کنید.";
    } else if (q.includes("چطوری") || q.includes("خوبی")) {
        return "من عالی‌ام! امیدوارم شما هم خوب باشید.";
    } else {
        return "پیامت رو دریافت کردم. در حال حاضر پاسخ دقیقی ندارم!";
    }
}