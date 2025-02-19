// تغییر فعال بودن تب‌های سایدبار
document.querySelectorAll(".sidebar ul li").forEach(tab => {
    tab.addEventListener("click", function() {
        document.querySelectorAll(".sidebar ul li").forEach(item => item.classList.remove("active"));
        this.classList.add("active");

        document.getElementById("dashboard").style.display = this.dataset.tab === "dashboard" ? "block" : "none";
        document.getElementById("classes").style.display = this.dataset.tab === "classes" ? "block" : "none";
        document.getElementById("camp").style.display = this.dataset.tab === "camp" ? "block" : "none";
    });
});

// عملکرد چت بات
const sendBtn = document.getElementById('sendBtn');
const chatInput = document.getElementById('chatInput');
const chatMessages = document.getElementById('chatMessages');

function appendMessage(text, type) {
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('chat-message', type);
    msgDiv.textContent = text;
    chatMessages.appendChild(msgDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

sendBtn.addEventListener('click', () => {
    const text = chatInput.value.trim();
    if (text !== "") {
        appendMessage(text, 'sent');
        chatInput.value = "";
        setTimeout(() => {
            appendMessage("پاسخ چت بات: " + text, 'received');
        }, 1000);
    }
});

chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendBtn.click();
    }
});

// تغییر محتوای سربرگ‌های کمپ و کلاس‌ها
document.querySelectorAll(".tabs .tab").forEach(tab => {
    tab.addEventListener("click", function() {
        // حذف کلاس active از همه تب‌ها
        document.querySelectorAll(".tabs .tab").forEach(item => item.classList.remove("active"));
        // اضافه کردن کلاس active به تب انتخاب شده
        this.classList.add("active");

        // مخفی کردن همه بخش‌های محتوا
        const parent = this.closest('.main').querySelectorAll(".content");
        parent.forEach(content => {
            content.style.display = "none";
        });

        // نمایش بخش محتوای مرتبط با تب انتخاب شده
        const sectionId = this.dataset.section;
        document.getElementById(sectionId).style.display = "block";
    });
});

// عملکرد مدال و اضافه کردن کاربر
const addButton = document.getElementById('addButton');
const addModal = document.getElementById('addModal');
const submitUser = document.getElementById('submitUser');
const closeModal = document.getElementById('closeModal');

addButton.addEventListener('click', () => {
    addModal.style.display = 'flex';
});

closeModal.addEventListener('click', () => {
    addModal.style.display = 'none';
});

submitUser.addEventListener('click', () => {
    const userName = document.getElementById('userName').value.trim();
    const userRole = document.getElementById('userRole').value.trim();

    if (userName && userRole) {
        const activeTab = document.querySelector('.tabs .tab.active');
        const sectionId = activeTab.dataset.section;
        const section = document.getElementById(sectionId);

        const newCard = document.createElement('div');
        newCard.classList.add('card');
        newCard.innerHTML = `
        <div class="avatar">
          <img class="avatar" src="download%20(1).jpeg" alt="">
        </div>
        <div class="info">
          <strong>${userName}</strong>
          <p>${userRole}</p>
        </div>
        <div class="menu-icon">⋮</div>
      `;

        section.querySelector('.cards').appendChild(newCard);
        addModal.style.display = 'none';
        document.getElementById('userName').value = '';
        document.getElementById('userRole').value = '';
    }
});

// عملکرد مدال و اضافه کردن کلاس
const addClassButton = document.getElementById('addClassButton');
const addClassModal = document.getElementById('addClassModal');
const submitClass = document.getElementById('submitClass');
const closeClassModal = document.getElementById('closeClassModal');

addClassButton.addEventListener('click', () => {
    addClassModal.style.display = 'flex';
});

closeClassModal.addEventListener('click', () => {
    addClassModal.style.display = 'none';
});

submitClass.addEventListener('click', () => {
    const className = document.getElementById('className').value.trim();
    const classTeacher = document.getElementById('classTeacher').value.trim();
    const classStatus = document.getElementById('classStatus').value.trim();

    if (className && classTeacher && classStatus) {
        const newClassCard = document.createElement('div');
        newClassCard.classList.add('card');
        newClassCard.innerHTML = `
        <div class="info">
          <strong>${className}</strong>
          <p>استاد: ${classTeacher}</p>
          <p>وضعیت: ${classStatus}</p>
        </div>
        <div class="menu-icon">⋮</div>
      `;

        const activeTab = document.querySelector('.tabs .tab.active');
        const sectionId = activeTab.dataset.section;
        const section = document.getElementById(sectionId);
        section.querySelector('.cards').appendChild(newClassCard);

        addClassModal.style.display = 'none';
        document.getElementById('className').value = '';
        document.getElementById('classTeacher').value = '';
        document.getElementById('classStatus').value = '';
    }
});

// عملکرد مدال اطلاعات دانش‌آموز
const studentModal = document.getElementById('studentModal');
const closeStudentModal = document.getElementById('closeStudentModal');

document.querySelectorAll('.card[data-student-id]').forEach(card => {
    card.addEventListener('click', () => {
        const studentName = card.querySelector('.info strong').textContent;
        const studentClass = card.querySelector('.info p').textContent;

        document.getElementById('studentName').textContent = studentName;
        document.getElementById('studentClass').textContent = studentClass;
        document.getElementById('studentStatus').textContent = 'فعال'; // می‌توانید وضعیت را از دیتابیس یا جاهای دیگر بگیرید

        studentModal.style.display = 'flex';
    });
});

closeStudentModal.addEventListener('click', () => {
    studentModal.style.display = 'none';
});