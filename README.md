# Lab 05: Visualization and Interactivity

## Project Theme

EduRisk Analytics

## Lab 05 Additions

This version continues the customized app from Labs 01–04.
- Course, risk, attendance, and minimum-score filters update every dashboard result.
- Filtered colored metric cards and student records with CSV download.
- Course Summary uses groupby with student count and average score, attendance, and study hours.
- Risk Level Summary uses value_counts and retains risk colors.
- Streamlit bar charts for student scores and students by course.
- Plotly charts for risk distribution and scores by risk, with hover details and chart controls.
- Existing colored Altair charts and risk doughnut are retained in Additional Charts.
- Empty results show a warning, zero metrics, and explanatory messages.
- The drawer menu, Student Data cards, data inspection, validated Risk Checker,
  temporary history, immediate history clearing, welcome button, and ethics reminders remain.

## Lab 05 Checks

1. With all filters reset: 8 students, score 71.62, attendance 79.0%, High Risk 2.
2. Filter Course to Python: 3 students, score 67.33, attendance 73.33, study hours 8.00.
3. Filter High Risk: all displayed records must have High Risk.
4. Minimum Attendance 80: only attendance >= 80 remains.
5. High Risk plus attendance 100: warning, zero metrics, no chart crash.
6. Check both summary tables, Streamlit charts, Plotly hover values, and filtered CSV.
7. Submit valid and blank names in Risk Checker; history accepts only valid submissions.
8. Navigate away and back, then Clear History; students.csv stays unchanged.

## Visual Update

- The sidebar starts collapsed. Use the menu control at the top left to open it,
  and the collapse control to close it. Icon buttons replace the radio menu;
  the current page is highlighted in blue.
- Low Risk is green, Medium Risk is amber, and High Risk is red throughout
  summary cards, table cells, student-score bars, risk-count bars, and the donut chart.
- Course bars have distinct colors. All charts follow the dashboard filters.
- The Risk Distribution donut includes counts and percentages in its tooltips.
- Empty filter results show a helpful message instead of empty charts.
- All combined Lab 01–04 functions remain available, including history and CSV export.

## Lab 04 Update

This version continues the completed Lab 03 app and retains its dashboard,
filters, download, charts, CSV loading, and data inspection.
Lab 04 improves the Risk Checker with forms, validation, supportive feedback,
and temporary session history.

- Form inputs are processed only after clicking Check Risk.
- Empty and whitespace-only names are rejected; accepted names are trimmed.
- Score and attendance are constrained to 0–100.
- Low, Medium, and High Risk feedback includes supportive guidance.
- Recent Risk Checks displays valid submissions from st.session_state.
- History survives page navigation within the same session.
- Clear History immediately removes the table and shows an empty-history message.
- History is temporary and is never saved to students.csv.
- A new session starts with empty history.

## Description

This Streamlit app combines the features developed across Labs 01–04 into one
student academic monitoring app. Later labs extend the earlier work, with the
original hard-coded dataset moved to students.csv and the original Risk Checker
upgraded with validation and temporary history.

## Features Retained from Each Lab

| Lab | Features included in this app |
|---|---|
| Lab 01 | Home, Student Data, and About pages; sidebar navigation; welcome button; student table; total students, average score, average attendance, and low-score count |
| Lab 02 | Eight-student dataset; risk calculation; Dashboard and Risk Checker pages; course/risk filters; minimum score/attendance sliders; show/hide data; CSV download; score and risk-count charts; high-risk count |
| Lab 03 | Data loaded from students.csv; missing-file handling; wide dashboard layout; course-count chart; shape, column names, and first-five-rows inspection; ethics reminders |
| Lab 04 | Submitted form validation; trimmed student names; bounded score and attendance inputs; supportive feedback; session history; recent-check table; Clear History |

Low Score Students counts scores below 60. High Risk Students counts students
whose score or attendance is below 60. Both metrics are retained because they
measure different things.

## Continuation from Lab 02

Continued from https://github.com/Shorekeeper1/EduRiskAnalysis at commit 3a9c881.
The existing navigation, risk function, course/risk filters, minimum attendance/score sliders,
show/hide table, filtered CSV download, risk count chart, and Student Data metrics are retained.
Lab 03 moves the existing eight-student dataset into students.csv and adds safe CSV loading,
data inspection, a course count chart, and updated page content and ethics reminders.
The README documents the combined app through Lab 04.

## Features

- Sidebar navigation
- Home page
- Dashboard page
- Student Data page
- Risk Checker page
- About page
- Student dataset stored in students.csv
- CSV data loading with Pandas
- Missing CSV file error handling
- Risk level calculation
- Dashboard metrics
- Student records table
- Student score chart
- Course count chart
- Data inspection section
- Ethics reminder

## Tools Used

- Python
- Streamlit
- Pandas
- VS Code

## Required Files

- app.py
- students.csv
- requirements.txt
- README.md

## How to Run

Open a terminal in this project folder, then run:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m streamlit run app.py
```

Open http://localhost:8501 if the browser does not open automatically.
Stop the app with Ctrl+C. Run from this project folder so students.csv is found.

## Student Information

Name: Soeun Sereisontik

Student ID: [not provided]

Class: [not provided]

## Risk Rules

- High Risk: score below 60 OR attendance below 60%.
- Medium Risk: otherwise, score below 75 OR attendance below 75%.
- Low Risk: both score and attendance are at least 75.

## Expected Data

8 students, average score 71.62, average attendance 79.0%, and 2 high-risk students.
The loaded table has 6 columns including the calculated Risk Level column.

## How to Check Lab 04

1. Open Risk Checker and submit an empty or whitespace-only name. Expect
   "Please enter the student name." and no saved history.
2. Student A, score 90, attendance 95: Low Risk; "Student appears on track."
3. Student B, score 70, attendance 80: Medium Risk; "Monitor progress and provide guidance."
4. Student C, score 50, attendance 85: High Risk; "Student may need additional support."
5. Student D, score 80, attendance 55: High Risk caused by low attendance.
6. Confirm all four valid submissions appear in Recent Risk Checks.
7. Navigate to Dashboard and return: history remains within this session.
8. Click Clear History: confirmation appears, the table disappears immediately,
   and "No risk checks yet." is displayed.

## Submission

Submit only app.py, students.csv, requirements.txt, and README.md.
The ZIP is named soeun_sereisontik_lab05.zip because no student ID was provided.
Before submitting, add your student ID and class above and rename the ZIP to yourstudentid_soeun_sereisontik_lab05.zip.
Exclude .venv, __pycache__, and filtered_student_data.csv.
