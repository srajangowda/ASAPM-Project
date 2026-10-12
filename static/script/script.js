// =========================================================
// EduPredict AI - Interactive Client Scripts
// =========================================================

document.addEventListener("DOMContentLoaded", () => {
    // 1. Sync score sliders and number input fields
    setupScoreSync("reading_score", "reading_range");
    setupScoreSync("writing_score", "writing_range");

    // 2. Preset Quick Fill Buttons
    setupPresets();

    // 3. Form submit loading state
    const form = document.querySelector("#predict-form");
    if (form) {
        form.addEventListener("submit", (e) => {
            const submitBtn = form.querySelector("#submit-btn");
            if (submitBtn) {
                submitBtn.innerHTML = `<span class="spinner"></span> Generating AI Prediction...`;
                submitBtn.disabled = true;
                // Allow form submit to proceed
                form.submit();
            }
        });
    }
});

function setupScoreSync(numberId, rangeId) {
    const numInput = document.getElementById(numberId);
    const rangeInput = document.getElementById(rangeId);

    if (!numInput || !rangeInput) return;

    // Range changes number
    rangeInput.addEventListener("input", (e) => {
        numInput.value = e.target.value;
    });

    // Number changes range
    numInput.addEventListener("input", (e) => {
        let val = parseInt(e.target.value, 10);
        if (isNaN(val)) val = 0;
        if (val > 100) val = 100;
        if (val < 0) val = 0;
        rangeInput.value = val;
    });
}

function setupPresets() {
    const presets = {
        high: {
            gender: "female",
            ethnicity: "group C",
            parental_level_of_education: "master's degree",
            lunch: "standard",
            test_preparation_course: "completed",
            reading_score: 92,
            writing_score: 95
        },
        average: {
            gender: "male",
            ethnicity: "group B",
            parental_level_of_education: "some college",
            lunch: "standard",
            test_preparation_course: "none",
            reading_score: 70,
            writing_score: 68
        },
        support: {
            gender: "male",
            ethnicity: "group A",
            parental_level_of_education: "high school",
            lunch: "free/reduced",
            test_preparation_course: "none",
            reading_score: 45,
            writing_score: 42
        }
    };

    document.querySelectorAll(".preset-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            const type = btn.getAttribute("data-preset");
            const data = presets[type];
            if (!data) return;

            // Fill form fields
            setVal("gender", data.gender);
            setVal("ethnicity", data.ethnicity);
            setVal("parental_level_of_education", data.parental_level_of_education);
            setVal("lunch", data.lunch);
            setVal("test_preparation_course", data.test_preparation_course);

            setScore("reading_score", "reading_range", data.reading_score);
            setScore("writing_score", "writing_range", data.writing_score);

            // Highlight preset button
            document.querySelectorAll(".preset-btn").forEach(b => b.classList.remove("active-preset"));
            btn.classList.add("active-preset");
        });
    });
}

function setVal(name, value) {
    const el = document.querySelector(`[name="${name}"]`);
    if (el) el.value = value;
}

function setScore(numId, rangeId, val) {
    const num = document.getElementById(numId);
    const range = document.getElementById(rangeId);
    if (num) num.value = val;
    if (range) range.value = val;
}
