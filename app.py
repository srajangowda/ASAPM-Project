from flask import Flask, request, render_template, jsonify
import numpy as np
import pandas as pd
import os

from src.pipeline.predict_pipeline import CustomData, PredictPipeline

app = Flask(__name__)

DATA_PATH = os.path.join("notebook", "data", "stud.csv")

def get_student_roster():
    """Load the student list and historical marks from the dataset."""
    try:
        if os.path.exists(DATA_PATH):
            df = pd.read_csv(DATA_PATH)
        else:
            df = pd.read_csv(os.path.join("artifacts", "raw.csv"))
        return df.to_dict(orient="records")
    except Exception as e:
        print(f"Error loading student roster: {e}")
        return []

# Home page / Faculty Portal Overview
@app.route('/')
@app.route('/home')
def index():
    students = get_student_roster()
    return render_template('index.html', total_students=len(students))

# Form page - Student Selection & Performance Assessment
@app.route('/form', methods=['GET', 'POST'])
def form():
    students = get_student_roster()

    if request.method == 'POST':
        student_name = request.form.get('student_name', 'Student')
        usn = request.form.get('usn', 'N/A')
        attendance = float(request.form.get('attendance_percentage', 85.0))

        # Semester 3 Marks
        em3 = float(request.form.get('eng_math_3', 70))
        ds = float(request.form.get('data_structures', 70))
        dl = float(request.form.get('digital_logic', 70))
        oop = float(request.form.get('oop_java', 70))
        dm = float(request.form.get('discrete_math', 70))

        # Semester 4 Marks
        dbms = float(request.form.get('dbms', 70))
        os_mark = float(request.form.get('operating_systems', 70))
        cn = float(request.form.get('computer_networks', 70))
        daa = float(request.form.get('design_analysis_algo', 70))
        se = float(request.form.get('software_engineering', 70))

        # Instantiate CustomData for ML pipeline
        data = CustomData(
            attendance_percentage=attendance,
            eng_math_3=em3,
            data_structures=ds,
            digital_logic=dl,
            oop_java=oop,
            discrete_math=dm,
            dbms=dbms,
            operating_systems=os_mark,
            computer_networks=cn,
            design_analysis_algo=daa,
            software_engineering=se
        )

        pred_df = data.get_data_as_data_frame()
        predict_pipeline = PredictPipeline()
        results = predict_pipeline.predict(pred_df)
        predicted_score = round(float(results[0]), 1)

        # Subject dictionary for analytics
        subject_marks = {
            "Engineering Mathematics III": em3,
            "Data Structures & Algorithms": ds,
            "Digital Logic Design": dl,
            "OOP with Java/C++": oop,
            "Discrete Mathematics": dm,
            "Database Management (DBMS)": dbms,
            "Operating Systems": os_mark,
            "Computer Networks": cn,
            "Design & Analysis of Algorithms (DAA)": daa,
            "Software Engineering": se
        }

        # Averages
        sem3_avg = round((em3 + ds + dl + oop + dm) / 5.0, 1)
        sem4_avg = round((dbms + os_mark + cn + daa + se) / 5.0, 1)
        past_avg = round((sem3_avg + sem4_avg) / 2.0, 1)

        # Strengths & Weaknesses
        strongest_subject = max(subject_marks.items(), key=lambda x: x[1])
        weakest_subject = min(subject_marks.items(), key=lambda x: x[1])

        # Performance Tier & Risk Rating
        if predicted_score >= 85:
            tier = "Distinction Candidate (Grade A+)"
            badge_class = "badge-excellent"
            risk_level = "Low Risk (High Performer)"
        elif predicted_score >= 70:
            tier = "First Class (Grade A / B)"
            badge_class = "badge-good"
            risk_level = "Low / Moderate Risk"
        elif predicted_score >= 50:
            tier = "Second Class (Grade C)"
            badge_class = "badge-average"
            risk_level = "Moderate Risk (Needs Monitoring)"
        else:
            tier = "Academic Support Required (Below 50)"
            badge_class = "badge-needs-help"
            risk_level = "High Academic Risk"

        student_report = {
            "name": student_name,
            "usn": usn,
            "attendance": attendance,
            "sem3_avg": sem3_avg,
            "sem4_avg": sem4_avg,
            "past_avg": past_avg,
            "predicted_score": predicted_score,
            "tier": tier,
            "badge_class": badge_class,
            "risk_level": risk_level,
            "strongest": strongest_subject,
            "weakest": weakest_subject,
            "marks": subject_marks,
            "sem3_marks": {
                "Engg Math III": em3,
                "Data Structures": ds,
                "Digital Logic": dl,
                "OOP Java": oop,
                "Discrete Math": dm
            },
            "sem4_marks": {
                "DBMS": dbms,
                "Operating Systems": os_mark,
                "Computer Networks": cn,
                "DAA": daa,
                "Software Engg": se
            }
        }

        return render_template('result.html', report=student_report, results=predicted_score)

    return render_template('form.html', students=students)

# Direct Result page fallback
@app.route('/result')
def result():
    return render_template('result.html', report=None)

# REST API to get student data as JSON
@app.route('/api/students', methods=['GET'])
def api_students():
    return jsonify(get_student_roster())

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
