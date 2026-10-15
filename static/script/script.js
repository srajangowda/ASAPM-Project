// =========================================================
// Faculty Portal - Student Performance Predictor Scripts
// =========================================================

document.addEventListener("DOMContentLoaded", () => {
    // 1. Setup Student Selection Dropdown Auto-Fill
    setupStudentSelector();

    // 2. Setup Attendance Slider Sync
    setupAttendanceSync();

    // 3. Form Submission Feedback
    const form = document.querySelector("#predict-form");
    if (form) {
        form.addEventListener("submit", (e) => {
            const submitBtn = form.querySelector("#submit-btn");
            if (submitBtn) {
                submitBtn.innerHTML = `<span class="spinner"></span> Running Machine Learning Evaluation...`;
                submitBtn.disabled = true;
                form.submit();
            }
        });
    }
});

function setupStudentSelector() {
    const selector = document.getElementById("student_select");
    if (!selector) return;

    // Trigger on change
    selector.addEventListener("change", (e) => {
        const option = selector.options[selector.selectedIndex];
        if (!option || !option.value) return;

        const name = option.getAttribute("data-name") || option.value;
        const usn = option.getAttribute("data-usn") || "";
        const att = option.getAttribute("data-att") || "85";

        // Display Header Banner
        const displayName = document.getElementById("display-name");
        const displayUsn = document.getElementById("display-usn");
        const displayAttBadge = document.getElementById("display-att-badge");

        if (displayName) displayName.innerText = name;
        if (displayUsn) displayUsn.innerText = "USN: " + usn;
        if (displayAttBadge) {
            displayAttBadge.innerText = parseFloat(att).toFixed(1) + "%";
            if (parseFloat(att) < 75) {
                displayAttBadge.style.color = "#b91c1c";
                displayAttBadge.style.background = "#fee2e2";
            } else {
                displayAttBadge.style.color = "#166534";
                displayAttBadge.style.background = "#dcfce7";
            }
        }

        // Hidden Inputs
        const studentNameInput = document.getElementById("student_name");
        const usnInput = document.getElementById("usn");
        if (studentNameInput) studentNameInput.value = name;
        if (usnInput) usnInput.value = usn;

        // Attendance
        setFieldValue("attendance_percentage", att);
        setFieldValue("attendance_range", att);

        // Semester 3 Marks
        setFieldValue("eng_math_3", option.getAttribute("data-em3"));
        setFieldValue("data_structures", option.getAttribute("data-ds"));
        setFieldValue("digital_logic", option.getAttribute("data-dl"));
        setFieldValue("oop_java", option.getAttribute("data-oop"));
        setFieldValue("discrete_math", option.getAttribute("data-dm"));

        // Semester 4 Marks
        setFieldValue("dbms", option.getAttribute("data-dbms"));
        setFieldValue("operating_systems", option.getAttribute("data-os"));
        setFieldValue("computer_networks", option.getAttribute("data-cn"));
        setFieldValue("design_analysis_algo", option.getAttribute("data-daa"));
        setFieldValue("software_engineering", option.getAttribute("data-se"));
    });

    // Fire initially to populate first selected student
    if (selector.selectedIndex >= 0) {
        selector.dispatchEvent(new Event('change'));
    }
}

function setFieldValue(id, val) {
    const el = document.getElementById(id);
    if (el && val !== null && val !== undefined) {
        el.value = parseFloat(val).toFixed(1);
    }
}

function setupAttendanceSync() {
    const num = document.getElementById("attendance_percentage");
    const range = document.getElementById("attendance_range");
    const badge = document.getElementById("display-att-badge");

    if (!num || !range) return;

    range.addEventListener("input", (e) => {
        num.value = parseFloat(e.target.value).toFixed(1);
        if (badge) badge.innerText = num.value + "%";
    });

    num.addEventListener("input", (e) => {
        let val = parseFloat(e.target.value);
        if (isNaN(val)) val = 0;
        if (val > 100) val = 100;
        range.value = val;
        if (badge) badge.innerText = val.toFixed(1) + "%";
    });
}
