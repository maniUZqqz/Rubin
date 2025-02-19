const uploadForm = document.getElementById("uploadCSVForm");

uploadForm.addEventListener("submit", function(e) {
    e.preventDefault(); // جلوگیری از رفرش صفحه

    const fileInput = document.getElementById("csvFile");
    const file = fileInput.files[0];
    if (!file) {
        alert("لطفاً یک فایل CSV انتخاب کنید.");
        return;
    }

    // در اینجا می‌توانید فایل CSV را پردازش کنید
    // یا آن را به سرور ارسال کنید.
    // برای نمونه:
    alert("فایل با نام: " + file.name + " انتخاب شد. پردازش موردنظر را در این بخش انجام دهید.");
});