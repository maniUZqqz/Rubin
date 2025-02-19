/*********************************************************
 * تعریف ستون‌ها (Columns)
 *********************************************************/
let columns = [
    { key: "fullName",    label: "نام و نام خانوادگی" },
    { key: "age",         label: "سن" },
    { key: "major",       label: "رشته" },
    { key: "fatherJob",   label: "شغل پدر" },
    { key: "path",        label: "مسیر (آغاز/پرواز)" },
    { key: "address",     label: "آدرس خانه" },
    { key: "cardNumber",  label: "شماره کارت" },
    { key: "nationalID",  label: "کد ملی" },
    { key: "postalCode",  label: "کد پستی" },
    { key: "birthDate",   label: "تاریخ تولد" },
];

/*********************************************************
 * داده‌های دانش‌آموزان (Students)
 *********************************************************/
let studentsData = [
    {
        fullName: "علی رضایی",
        age: 19,
        major: "مهندسی کامپیوتر",
        fatherJob: "معلم",
        path: "آغاز",
        address: "تهران، بلوار کشاورز",
        cardNumber: "6037-9999-1234-0001",
        nationalID: "1234567890",
        postalCode: "113999XXXX",
        birthDate: "1383/05/16"
    },
    {
        fullName: "مریم احمدی",
        age: 20,
        major: "گرافیک",
        fatherJob: "کارمند بانک",
        path: "پرواز",
        address: "اصفهان، خیابان آمادگاه",
        cardNumber: "6037-9999-1234-0002",
        nationalID: "0098765432",
        postalCode: "713999XXXX",
        birthDate: "1382/10/01"
    },
    {
        fullName: "حسین موسوی",
        age: 18,
        major: "تجربی",
        fatherJob: "راننده تاکسی",
        path: "آغاز",
        address: "تبریز، خیابان حافظ",
        cardNumber: "6037-9999-1234-0003",
        nationalID: "1029384756",
        postalCode: "513999XXXX",
        birthDate: "1384/01/23"
    },
    {
        fullName: "نگار جعفری",
        age: 21,
        major: "علوم آزمایشگاهی",
        fatherJob: "پزشک عمومی",
        path: "پرواز",
        address: "مشهد، میدان جانباز",
        cardNumber: "6037-9999-1234-0004",
        nationalID: "4433221100",
        postalCode: "913456XXXX",
        birthDate: "1381/07/12"
    },
    {
        fullName: "عسل محمدی",
        age: 17,
        major: "ریاضی فیزیک",
        fatherJob: "مهندس عمران",
        path: "آغاز",
        address: "شیراز، خیابان زند",
        cardNumber: "6037-9999-1234-0005",
        nationalID: "2233445566",
        postalCode: "715623XXXX",
        birthDate: "1385/03/29"
    },
    {
        fullName: "محمد کاشانی",
        age: 22,
        major: "برق صنعتی",
        fatherJob: "باغدار",
        path: "پرواز",
        address: "کرج، فاز 4 مهرشهر",
        cardNumber: "6037-9999-1234-0006",
        nationalID: "5566778899",
        postalCode: "316789XXXX",
        birthDate: "1379/11/17"
    },
    {
        fullName: "الهام کریمی",
        age: 19,
        major: "روانشناسی",
        fatherJob: "بازنشسته فرهنگی",
        path: "آغاز",
        address: "قم، بلوار امین",
        cardNumber: "6037-9999-1234-0007",
        nationalID: "7788990011",
        postalCode: "519876XXXX",
        birthDate: "1383/02/05"
    },
    {
        fullName: "فاطمه عزیزی",
        age: 18,
        major: "هنرهای تجسمی",
        fatherJob: "کارمند شرکت خصوصی",
        path: "پرواز",
        address: "کرمان، جاده تهران",
        cardNumber: "6037-9999-1234-0008",
        nationalID: "8877665544",
        postalCode: "761234XXXX",
        birthDate: "1384/09/30"
    },
    {
        fullName: "نیما راد",
        age: 23,
        major: "معماری",
        fatherJob: "فروشنده",
        path: "آغاز",
        address: "اهواز، بلوار گلستان",
        cardNumber: "6037-9999-1234-0009",
        nationalID: "3322110099",
        postalCode: "619234XXXX",
        birthDate: "1378/07/22"
    },
    {
        fullName: "سارا بهرامی",
        age: 20,
        major: "حسابداری",
        fatherJob: "آزاد",
        path: "پرواز",
        address: "زنجان، خیابان امام",
        cardNumber: "6037-9999-1234-0010",
        nationalID: "8899007766",
        postalCode: "539000XXXX",
        birthDate: "1382/12/10"
    }
];


let searchTerm = "";         // فیلد برای جستجو
let currentEditIndex = -1;   // ایندکس دانش‌آموزی که در حال ویرایش است

/*********************************************************
 *  رندر کردن جدول
 *********************************************************/
function renderTable() {
    const theadRow = document.getElementById("tableHeaderRow");
    const tbody = document.getElementById("tableBody");
    theadRow.innerHTML = "";
    tbody.innerHTML = "";

    // هدر (ستون‌ها)
    columns.forEach(col => {
        const th = document.createElement("th");
        // نمایش عنوان ستون + دکمه حذف ستون
        th.innerHTML = `
                ${col.label}
                <button class="delete-column-btn" onclick="removeColumn('${col.key}')">×</button>
            `;
        theadRow.appendChild(th);
    });

    // ستون عملیات
    const thActions = document.createElement("th");
    thActions.textContent = "عملیات";
    theadRow.appendChild(thActions);

    // فیلتر دانشجویان براساس searchTerm
    const filteredStudents = studentsData.filter(student => {
        if (!searchTerm) return true;
        return columns.some(col => {
            const val = String(student[col.key] || "").toLowerCase();
            return val.includes(searchTerm.toLowerCase());
        });
    });

    // ساخت ردیف برای دانشجویان فیلترشده
    filteredStudents.forEach((student, index) => {
        const tr = document.createElement("tr");

        // سلول‌های مربوط به ستون‌ها
        columns.forEach(col => {
            const td = document.createElement("td");
            td.textContent = student[col.key] || "";
            tr.appendChild(td);
        });

        // سلول عملیات (Edit/Delete)
        const tdActions = document.createElement("td");
        tdActions.classList.add("d-flex", "gap-2");

        // دکمه Edit
        const editBtn = document.createElement("button");
        editBtn.textContent = "Edit";
        editBtn.className = "btn btn-sm btn-primary";
        editBtn.setAttribute("data-bs-toggle", "modal");
        editBtn.setAttribute("data-bs-target", "#editStudentModal");

        const realIndex = studentsData.indexOf(student);
        editBtn.onclick = () => openEditStudent(realIndex);

        tdActions.appendChild(editBtn);

        // دکمه Delete
        const deleteBtn = document.createElement("button");
        deleteBtn.textContent = "Delete";
        deleteBtn.className = "btn btn-sm btn-danger";
        deleteBtn.onclick = () => removeStudent(realIndex);
        tdActions.appendChild(deleteBtn);

        tr.appendChild(tdActions);
        tbody.appendChild(tr);
    });
}

/*********************************************************
 *  تابع جستجو
 *********************************************************/
function onSearchChange() {
    const inputEl = document.getElementById("searchInput");
    searchTerm = inputEl.value.trim();
    renderTable();
}

/*********************************************************
 *  حذف ستون
 *********************************************************/
function removeColumn(columnKey) {
    const colIndex = columns.findIndex(c => c.key === columnKey);
    if (colIndex === -1) return;

    const confirmMsg = `آیا مطمئن هستید که می‌خواهید ستون "${columns[colIndex].label}" را حذف کنید؟`;
    if (!confirm(confirmMsg)) return;

    const colObj = columns.splice(colIndex, 1)[0];
    studentsData.forEach(student => {
        delete student[colObj.key];
    });

    renderTable();
}

/*********************************************************
 *  حذف دانشجو
 *********************************************************/
function removeStudent(index) {
    const st = studentsData[index];
    const confirmMsg = `آیا مطمئن هستید که می‌خواهید دانشجو "${st.fullName || 'بدون نام'}" حذف شود؟`;
    if (!confirm(confirmMsg)) return;

    studentsData.splice(index, 1);
    renderTable();
}

/*********************************************************
 *  افزودن ستون جدید
 *********************************************************/
function addNewColumn() {
    const columnKey = document.getElementById("columnKey").value.trim();
    const columnLabel = document.getElementById("columnLabel").value.trim();
    if (!columnKey || !columnLabel) return;

    columns.push({ key: columnKey, label: columnLabel });
    studentsData.forEach(st => {
        st[columnKey] = "";
    });

    renderTable();
    const modalEl = document.getElementById("addColumnModal");
    const modal = bootstrap.Modal.getInstance(modalEl);
    modal.hide();
    document.getElementById("addColumnForm").reset();
}

/*********************************************************
 *  ساخت فرم افزودن دانشجو
 *********************************************************/
const addStudentModal = document.getElementById("addStudentModal");
addStudentModal.addEventListener("show.bs.modal", buildAddStudentForm);

function buildAddStudentForm() {
    const modalBody = document.getElementById("addStudentModalBody");
    modalBody.innerHTML = "";
    columns.forEach(col => {
        const div = document.createElement("div");
        div.className = "mb-3";

        const label = document.createElement("label");
        label.className = "form-label";
        label.textContent = col.label;

        const input = document.createElement("input");
        input.className = "form-control";
        input.id = "add_" + col.key;
        input.placeholder = `وارد کردن ${col.label}`;

        div.appendChild(label);
        div.appendChild(input);
        modalBody.appendChild(div);
    });
}

function saveNewStudent() {
    let newStudent = {};
    columns.forEach(col => {
        const val = document.getElementById("add_" + col.key).value.trim();
        newStudent[col.key] = val;
    });
    studentsData.push(newStudent);
    renderTable();

    const modalEl = document.getElementById("addStudentModal");
    const modal = bootstrap.Modal.getInstance(modalEl);
    modal.hide();
}

/*********************************************************
 *  ویرایش دانشجو
 *********************************************************/
function openEditStudent(index) {
    currentEditIndex = index;
    const modalBody = document.getElementById("editStudentModalBody");
    modalBody.innerHTML = "";

    columns.forEach(col => {
        const div = document.createElement("div");
        div.className = "mb-3";

        const label = document.createElement("label");
        label.className = "form-label";
        label.textContent = col.label;

        const input = document.createElement("input");
        input.className = "form-control";
        input.id = "edit_" + col.key;
        input.placeholder = `ویرایش ${col.label}`;
        input.value = studentsData[index][col.key] || "";

        div.appendChild(label);
        div.appendChild(input);
        modalBody.appendChild(div);
    });
}

function applyEditStudent() {
    const st = studentsData[currentEditIndex];
    columns.forEach(col => {
        const val = document.getElementById("edit_" + col.key).value.trim();
        st[col.key] = val;
    });
    renderTable();

    const modalEl = document.getElementById("editStudentModal");
    const modal = bootstrap.Modal.getInstance(modalEl);
    modal.hide();
    currentEditIndex = -1;
}

/*********************************************************
 *  ساخت CSV و دانلود
 *********************************************************/
// NEW: تابع تبدیل داده‌ها به CSV
function convertToCSV(cols, data) {
    let csvContent = "";

    // ردیف هدر با استفاده از label ستون‌ها
    const headerRow = cols.map(c => `"${(c.label || "").replace(/"/g, '""')}"`).join(",");
    csvContent += headerRow + "\r\n";

    // سطرهای داده
    data.forEach(student => {
        const row = cols.map(c => {
            const val = student[c.key] || "";
            // جایگزینی " برای پرهیز از اشکال در CSV
            const escapedVal = String(val).replace(/"/g, '""');
            return `"${escapedVal}"`;
        }).join(",");
        csvContent += row + "\r\n";
    });

    return csvContent;
}

// NEW: تابع دانلود CSV
function downloadSheet() {
    // تولید محتوای CSV از ستون‌ها و داده‌ها
    const csvData = convertToCSV(columns, studentsData);

    // ساخت یک Blob از CSV
    const blob = new Blob([csvData], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);

    // ساخت لینک دانلود موقت
    const link = document.createElement("a");
    link.href = url;
    link.download = "students.csv"; // نام فایل خروجی
    link.click();

    // پاکسازی URL موقت
    URL.revokeObjectURL(url);
}

/*********************************************************
 *  لود اولیه
 *********************************************************/
document.addEventListener("DOMContentLoaded", () => {
    renderTable();
});