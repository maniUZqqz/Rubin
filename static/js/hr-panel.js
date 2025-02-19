document.addEventListener("DOMContentLoaded", () => {
    fetchUploadedFiles();
});

function fetchUploadedFiles() {
    fetch('/get-uploaded-files/')
        .then(response => response.json())
        .then(data => {
            const tbody = document.getElementById("tableBody");
            tbody.innerHTML = "";

            data.forEach(file => {
                const tr = document.createElement("tr");

                // نمایش نام فایل و تاریخ آپلود
                tr.innerHTML = `
                    <td><a href="${file.file.url}" download>${file.file.name}</a></td>
                    <td>${file.uploaded_at}</td>
                `;

                // نمایش داده‌های استخراج‌شده
                if (file.extracted_data && file.extracted_data.length > 0) {
                    const firstRow = file.extracted_data[0];
                    Object.keys(firstRow).forEach(key => {
                        const td = document.createElement("td");
                        td.textContent = firstRow[key];
                        tr.appendChild(td);
                    });
                }

                tbody.appendChild(tr);
            });
        })
        .catch(error => console.error('Error fetching files:', error));
}