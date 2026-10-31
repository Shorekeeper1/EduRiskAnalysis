import streamlit as st
import pandas as pd
import altair as alt


st.set_page_config(
    page_title="EduRisk Analytics - Lab 04",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# Use the same risk colors in tables, charts, and summary cards.
RISK_ORDER = ["Low Risk", "Medium Risk", "High Risk"]
RISK_COLORS = ["#16865B", "#CF850D", "#DC4C64"]
RISK_STYLES = {
    "Low Risk": ("#E4F5EC", "#126440"),
    "Medium Risk": ("#FFF1D6", "#855100"),
    "High Risk": ("#FDE8EC", "#A82440"),
}

st.html("""
<style>
    [data-testid="stSidebar"] {border-right: 1px solid #dce4f0;}
    [data-testid="stSidebar"] [data-testid="stButton"] button {
        justify-content: flex-start; border-radius: 9px; min-height: 44px;
        padding: 10px 14px; margin-bottom: 3px;
    }
    [data-testid="stSidebar"] button[kind="primary"] {
        background: #3d6df2; border-color: #3d6df2; color: white;
    }
    [data-testid="stSidebar"] button[kind="primary"]:hover {background: #2c58ce;}
    [data-testid="stMetric"] {padding: 12px 0;}
    .risk-card {padding: 15px 18px; border-radius: 12px; margin: 8px 0 20px;
        border: 1px solid currentColor; border-left-width: 5px;}
    .risk-card .risk-count {font-size: 26px; font-weight: 750; margin-top: 3px;}
    .risk-label {font-size: 14px; font-weight: 650;}
</style>
""")


def styled_students(data):
    def risk_cell(value):
        background, foreground = RISK_STYLES.get(value, ("transparent", "inherit"))
        return f"background-color: {background}; color: {foreground}; font-weight: 700"

    return data.style.map(risk_cell, subset=["Risk Level"])


def risk_color():
    return alt.Color("Risk Level:N", sort=RISK_ORDER,
                     scale=alt.Scale(domain=RISK_ORDER, range=RISK_COLORS),
                     legend=alt.Legend(title=None, orient="bottom"))


def select_page(page):
    st.session_state["selected_page"] = page


def load_student_data():
    try:
        return pd.read_csv("students.csv")
    except FileNotFoundError:
        st.error(
            "students.csv was not found. Please place it in the same folder as app.py."
        )
        st.stop()


student_df = load_student_data()

def get_risk_level(score, attendance):
    if score < 60 or attendance < 60:
        return "High Risk"
    elif score < 75 or attendance < 75:
        return "Medium Risk"
    else:
        return "Low Risk"

student_df["Risk Level"] = student_df.apply(
    lambda row: get_risk_level(row["Score"], row["Attendance"]),
    axis=1
)

if "risk_history" not in st.session_state:
    st.session_state["risk_history"] = []

if "selected_page" not in st.session_state:
    st.session_state["selected_page"] = "Home"

with st.sidebar:
    st.title("🎓 EduRisk")
    st.caption("STUDENT SUPPORT · LABS 01–04")
    st.divider()
    for page, icon in [
        ("Home", ":material/home:"),
        ("Dashboard", ":material/dashboard:"),
        ("Student Data", ":material/table_chart:"),
        ("Risk Checker", ":material/health_and_safety:"),
        ("About", ":material/info:"),
    ]:
        st.button(page, icon=icon, key=f"nav_{page}", width="stretch",
                  type="primary" if st.session_state["selected_page"] == page else "tertiary",
                  on_click=select_page, args=(page,))
    st.divider()
    st.caption("Support learning. Encourage progress.")

selected_page = st.session_state["selected_page"]

if selected_page == "Home":
    st.title("🎓 EduRisk Analytics")
    st.subheader("Reliable Risk Checker with Forms and Session State")
    st.write("Welcome to Lab 04.")
    st.write(
        "In this lab, the app improves the Risk Checker page using "
        "Streamlit forms, input validation, and session state."
    )
    st.success("Lab 04 app is running successfully!")

    if st.button("Click Me"):
        st.write("Welcome")

elif selected_page == "Dashboard":
    st.title("Dashboard Prototype")

    st.write("Use the filters below to explore student performance loaded from students.csv.")

    selected_course = st.selectbox(
        "Select Course",
        ["All"] + list(student_df["Course"].unique())
    )

    selected_risk = st.selectbox(
        "Select Risk Level",
        ["All", "Low Risk", "Medium Risk", "High Risk"]
    )

    min_attendance = st.slider(
        "Minimum Attendance",
        0,
        100,
        0
    )

    min_score = st.slider(
        "Minimum Score",
        0,
        100,
        0
    )

    filtered_df = student_df.copy()

    if selected_course != "All":
        filtered_df = filtered_df[filtered_df["Course"] == selected_course]

    if selected_risk != "All":
        filtered_df = filtered_df[filtered_df["Risk Level"] == selected_risk]

    filtered_df = filtered_df[
        filtered_df["Attendance"] >= min_attendance
    ]

    filtered_df = filtered_df[
        filtered_df["Score"] >= min_score
    ]

    total_students = len(filtered_df)

    if len(filtered_df) > 0:
        average_score = filtered_df["Score"].mean()
        average_attendance = filtered_df["Attendance"].mean()
    else:
        average_score = 0
        average_attendance = 0

    high_risk_students = filtered_df[
        filtered_df["Risk Level"] == "High Risk"
    ].shape[0]

    st.subheader("Dashboard Metrics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Students", total_students)

    with col2:
        st.metric("Average Score", round(average_score, 2))

    with col3:
        st.metric("Average Attendance", f"{round(average_attendance, 2)}%")

    with col4:
        st.metric("High Risk", high_risk_students)

    show_data = st.checkbox("Show Filtered Dataset", True)

    if show_data:
        st.subheader("Student Records")
        st.caption("Filtered student data loaded from students.csv.")
        st.dataframe(styled_students(filtered_df), hide_index=True, width="stretch")

        csv = filtered_df.to_csv(index=False)

        st.download_button(
            label="Download Filtered Data",
            data=csv,
            file_name="filtered_student_data.csv",
            mime="text/csv"
        )
    else:
        st.info("Filtered dataset is hidden.")

    risk_counts = filtered_df["Risk Level"].value_counts().reindex(RISK_ORDER, fill_value=0)
    for column, level in zip(st.columns(3), RISK_ORDER):
        background, foreground = RISK_STYLES[level]
        with column:
            st.markdown(
                f'<div class="risk-card" style="background:{background};color:{foreground}">'
                f'<div class="risk-label">{level}</div>'
                f'<div class="risk-count">{int(risk_counts[level])}</div></div>',
                unsafe_allow_html=True,
            )

    st.subheader("Charts")
    if filtered_df.empty:
        st.info("No students match these filters. Adjust the filters to see charts.")
    else:
        risk_data = risk_counts.rename_axis("Risk Level").reset_index(name="Students")
        chart_col1, chart_col2 = st.columns(2)
        with chart_col1:
            st.write("Student Scores")
            chart = alt.Chart(filtered_df).mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5).encode(
                x=alt.X("Student Name:N", sort=None, axis=alt.Axis(labelAngle=-35)),
                y=alt.Y("Score:Q", scale=alt.Scale(domain=[0, 100])),
                color=risk_color(),
                tooltip=["Student Name:N", "Course:N", "Score:Q", "Attendance:Q", "Risk Level:N"],
            ).properties(height=280)
            st.altair_chart(chart, width="stretch")
        with chart_col2:
            st.write("Risk Level Count")
            chart = alt.Chart(risk_data).mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5).encode(
                x=alt.X("Risk Level:N", sort=RISK_ORDER, axis=alt.Axis(labelAngle=0)),
                y=alt.Y("Students:Q", axis=alt.Axis(tickMinStep=1)),
                color=risk_color(), tooltip=["Risk Level:N", "Students:Q"],
            ).properties(height=280)
            st.altair_chart(chart, width="stretch")

        chart_col3, chart_col4 = st.columns(2)
        with chart_col3:
            st.write("Course Count")
            course_data = filtered_df["Course"].value_counts().rename_axis("Course").reset_index(name="Students")
            chart = alt.Chart(course_data).mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5).encode(
                x=alt.X("Course:N", sort="-y", axis=alt.Axis(labelAngle=-25)),
                y=alt.Y("Students:Q", axis=alt.Axis(tickMinStep=1)),
                color=alt.Color("Course:N", scale=alt.Scale(
                    domain=["Python", "Statistics", "Database", "Web App"],
                    range=["#4776E6", "#9570D8", "#23A5A0", "#E39848"]), legend=None),
                tooltip=["Course:N", "Students:Q"],
            ).properties(height=280)
            st.altair_chart(chart, width="stretch")
        with chart_col4:
            st.write("Risk Distribution")
            pie_data = risk_data[risk_data["Students"] > 0].copy()
            pie_data["Share"] = pie_data["Students"] / len(filtered_df)
            donut = alt.Chart(pie_data).mark_arc(innerRadius=65, cornerRadius=4).encode(
                theta=alt.Theta("Students:Q", stack=True), color=risk_color(),
                order=alt.Order("Risk Level:N", sort="ascending"),
                tooltip=["Risk Level:N", "Students:Q", alt.Tooltip("Share:Q", format=".0%")],
            ).properties(height=280)
            st.altair_chart(donut, width="stretch")
            st.caption("Share of students matching the current filters.")

    st.info(
        "Ethics Reminder: Academic monitoring should support students, "
        "not label or punish them."
    )

elif selected_page == "Student Data":
    st.title("Student Data")

    total_students = len(student_df)
    average_score = student_df["Score"].mean()
    average_attendance = student_df["Attendance"].mean()
    high_risk_students = student_df[
        student_df["Risk Level"] == "High Risk"
    ].shape[0]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Students", total_students)

    with col2:
        st.metric("Average Score", round(average_score, 2))

    with col3:
        st.metric("Average Attendance", f"{round(average_attendance, 2)}%")

    with col4:
        st.metric("High Risk Students", high_risk_students)

    st.metric("Low Score Students", int((student_df["Score"] < 60).sum()))

    st.subheader("Data Inspection")
    st.write("Rows and Columns:", student_df.shape)
    st.write("Column Names:")
    st.write(student_df.columns.tolist())
    st.write("First 5 Rows:")
    st.dataframe(styled_students(student_df.head()), hide_index=True, width="stretch")

    st.subheader("Full Student Dataset")
    st.dataframe(styled_students(student_df), hide_index=True, width="stretch")

elif selected_page == "Risk Checker":
    st.title("Single Student Risk Checker")

    st.write(
        "Enter student information to check risk level. "
        "The result is based on score and attendance."
    )

    st.info(
        "This tool is for academic support. Risk results should help students, "
        "not label or punish them."
    )

    with st.form("risk_checker_form"):
        input_name = st.text_input("Student Name")
        input_score = st.number_input("Score", 0, 100, 50)
        input_attendance = st.number_input("Attendance", 0, 100, 50)

        submitted = st.form_submit_button("Check Risk")

    if submitted:
        if input_name.strip() == "":
            st.warning("Please enter the student name.")
        else:
            risk_result = get_risk_level(
                input_score,
                input_attendance
            )

            result = {
                "Student Name": input_name.strip(),
                "Score": input_score,
                "Attendance": input_attendance,
                "Risk Level": risk_result
            }

            st.session_state["risk_history"].append(result)

            if risk_result == "Low Risk":
                st.success("Risk Level: Low Risk")
                st.write("Student appears on track.")
            elif risk_result == "Medium Risk":
                st.warning("Risk Level: Medium Risk")
                st.write("Monitor progress and provide guidance.")
            else:
                st.error("Risk Level: High Risk")
                st.write("Student may need additional support.")

            st.write("Student Name:", input_name.strip())
            st.write("Score:", input_score)
            st.write("Attendance:", input_attendance)

    st.subheader("Recent Risk Checks")

    if st.session_state["risk_history"]:
        if st.button("Clear History"):
            st.session_state["risk_history"] = []
            st.success("Risk check history cleared.")

    if st.session_state["risk_history"]:
        history_df = pd.DataFrame(st.session_state["risk_history"])
        st.dataframe(styled_students(history_df), hide_index=True, width="stretch")
    else:
        st.info("No risk checks yet.")

    st.warning(
        "Ethics Reminder: Risk results should be used as guidance for support, "
        "not as final judgment about a student."
    )

else:
    st.title("About")

    st.write("This app is part of Lab 04.")
    st.write("Course: Web App Development for Data Science")
    st.write("Project Theme: EduRisk Analytics")
    st.write("Topic: Forms, Validation, and Session State")

    st.info(
        "This version improves the Risk Checker page using Streamlit forms, "
        "input validation, and session state."
    )

    st.warning(
        "Ethics Reminder: Student risk information should be used responsibly "
        "to support learning and student success."
    )
