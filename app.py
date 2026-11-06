# Libraries: Streamlit builds the interface, Pandas handles tables,
# and Altair and Plotly create charts.
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px


# PAGE SETUP: use a wide layout and keep the drawer closed initially.
st.set_page_config(
    page_title="EduRisk Analytics - Lab 05",
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

# CUSTOM APPEARANCE: style sidebar buttons, metric boxes, and risk cards.
# The st-key-* selectors match the keys assigned to the metric containers.
st.html("""
<style>
    [data-testid="stSidebar"] {border-right: 1px solid #dce4f0;}
    [data-testid="stSidebar"] [data-testid="stButton"] button {
        justify-content: flex-start !important; text-align: left !important;
        gap: 12px; border-radius: 9px; min-height: 44px;
        padding: 10px 14px; margin-bottom: 3px;
    }
    [data-testid="stSidebar"] [data-testid="stButton"] button > div {
        justify-content: flex-start !important;
    }
    [data-testid="stSidebar"] [data-testid="stButton"] button [data-testid="stMarkdownContainer"] {
        flex: 1; text-align: left !important;
    }
    [data-testid="stSidebar"] [data-testid="stButton"] button p {
        text-align: left !important;
    }
    [data-testid="stSidebar"] button[kind="primary"] {
        background: #3d6df2; border-color: #3d6df2; color: white;
    }
    [data-testid="stSidebar"] button[kind="primary"]:hover {background: #2c58ce;}
    [data-testid="stMetric"] {padding: 18px 20px; border-radius: 12px;}
    .st-key-metric_students [data-testid="stMetric"] {
        background: #EDF3FF; border: 1px solid #CDDDFB; border-top: 4px solid #4776E6;
        color: #234A9F;
    }
    .st-key-metric_score [data-testid="stMetric"] {
        background: #F3EEFC; border: 1px solid #E1D5F5; border-top: 4px solid #9570D8;
        color: #64429A;
    }
    .st-key-metric_attendance [data-testid="stMetric"] {
        background: #EAF7F5; border: 1px solid #C6E8E3; border-top: 4px solid #23A5A0;
        color: #146D67;
    }
    .st-key-metric_risk [data-testid="stMetric"] {
        background: #FDEEF1; border: 1px solid #F3CCD5; border-top: 4px solid #DC4C64;
        color: #A82440;
    }
    .st-key-metric_low_score [data-testid="stMetric"] {
        background: #FFF5E3; border: 1px solid #F1DCAF; border-top: 4px solid #CF850D;
        color: #855100;
    }
    [class*="st-key-metric_"] [data-testid="stMetricLabel"],
    [class*="st-key-metric_"] [data-testid="stMetricValue"] {color: inherit;}
    .risk-card {padding: 15px 18px; border-radius: 12px; margin: 8px 0 20px;
        border: 1px solid currentColor; border-left-width: 5px;}
    .risk-card .risk-count {font-size: 26px; font-weight: 750; margin-top: 3px;}
    .risk-label {font-size: 14px; font-weight: 650;}
</style>
""")


# Return a styled table that highlights only the Risk Level cells.
# The underlying data remains unchanged, so CSV downloads contain plain values.
def styled_students(data):
    # Convert one risk label into background, text-color, and font-weight rules.
    def risk_cell(value):
        background, foreground = RISK_STYLES.get(value, ("transparent", "inherit"))
        return f"background-color: {background}; color: {foreground}; font-weight: 700"

    return data.style.map(risk_cell, subset=["Risk Level"])


# Build a reusable Altair color encoding with a fixed risk order and palette.
# Fixed colors keep High Risk red even when filters remove other categories.
def risk_color():
    return alt.Color("Risk Level:N", sort=RISK_ORDER,
                     scale=alt.Scale(domain=RISK_ORDER, range=RISK_COLORS),
                     legend=alt.Legend(title=None, orient="bottom"))


# Sidebar button callback: remember the selected page before Streamlit reruns.
def select_page(page):
    st.session_state["selected_page"] = page


# Load students.csv from the current project folder.
# Show a helpful error and stop rendering if the file is missing.
def load_student_data():
    try:
        return pd.read_csv("students.csv")
    except FileNotFoundError:
        st.error(
            "students.csv was not found. Please place it in the same folder as app.py."
        )
        st.stop()


# Load the full dataset once during this script run; dashboard filters use a copy.
student_df = load_student_data()

# Classify a student using score OR attendance.
# Below 60 is High Risk; otherwise below 75 is Medium Risk; both >= 75 is Low Risk.
def get_risk_level(score, attendance):
    if score < 60 or attendance < 60:
        return "High Risk"
    elif score < 75 or attendance < 75:
        return "Medium Risk"
    else:
        return "Low Risk"

# Calculate Risk Level for every row. axis=1 passes one student row at a time.
student_df["Risk Level"] = student_df.apply(
    lambda row: get_risk_level(row["Score"], row["Attendance"]),
    axis=1
)

# SESSION MEMORY: initialize only when absent so reruns do not erase history.
# History is temporary for this session and is never written to students.csv.
if "risk_history" not in st.session_state:
    st.session_state["risk_history"] = []

# Start new sessions on Home and retain the selected page across reruns.
if "selected_page" not in st.session_state:
    st.session_state["selected_page"] = "Home"

# DRAWER NAVIGATION: icon buttons replace radio buttons; the active page is blue.
with st.sidebar:
    st.title("🎓 EduRisk")
    st.caption("STUDENT SUPPORT · LABS 01–05")
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

# HOME PAGE: introduce Lab 05 and retain the original Lab 01 welcome button.
if selected_page == "Home":
    st.title("🎓 EduRisk Analytics")
    st.subheader("Interactive Dashboard with Visualization and Filters")
    st.write("Welcome to Lab 05.")
    st.write(
        "In this lab, the app improves the Dashboard page using "
        "grouped summaries, interactive filters, Streamlit charts, and Plotly charts."
    )
    st.success("Lab 05 app is running successfully!")

    if st.button("Click Me"):
        st.write("Welcome")

# DASHBOARD PAGE: every metric, summary, chart, and export uses filtered_df.
elif selected_page == "Dashboard":
    st.title("Interactive Student Performance Dashboard")

    st.write("Use the filters below to explore student performance loaded from students.csv.")

    # Collect course, risk, minimum-attendance, and minimum-score selections.
    st.subheader("Dashboard Filters")
    filter_columns = st.columns(4)
    with filter_columns[0]:
        selected_course = st.selectbox("Filter by Course", ["All"] + sorted(student_df["Course"].unique()))
    with filter_columns[1]:
        selected_risk = st.selectbox("Filter by Risk Level", ["All"] + RISK_ORDER)
    with filter_columns[2]:
        min_attendance = st.slider("Minimum Attendance", 0, 100, 0)
    with filter_columns[3]:
        min_score = st.slider("Minimum Score", 0, 100, 0)

    # Apply all selected filters in sequence without modifying the full dataset.
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

    # An empty selection is valid: warn the user instead of failing.
    if filtered_df.empty:
        st.warning("No students match the selected filters. Please adjust the filters.")

    # Count matching students and use zero averages when there are no matches.
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

    # Display the filtered metrics in four colored, bordered containers.
    st.subheader("Filtered Dashboard Metrics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        with st.container(key="metric_students"):
            st.metric("Students", total_students, border=True)

    with col2:
        with st.container(key="metric_score"):
            st.metric("Average Score", round(average_score, 2), border=True)

    with col3:
        with st.container(key="metric_attendance"):
            st.metric("Average Attendance", f"{round(average_attendance, 2)}%", border=True)

    with col4:
        with st.container(key="metric_risk"):
            st.metric("High Risk", high_risk_students, border=True)

    # groupby collects students by course; agg computes each summary statistic.
    st.subheader("Course Summary")
    if not filtered_df.empty:
        course_summary = filtered_df.groupby("Course").agg(
            Students=("Student Name", "count"),
            Average_Score=("Score", "mean"),
            Average_Attendance=("Attendance", "mean"),
            Average_Study_Hours=("Study Hours", "mean"),
        ).reset_index()
        st.dataframe(course_summary.round(2), hide_index=True, width="stretch")
    else:
        st.info("No course summary available for the selected filters.")

    # value_counts counts records in each risk category present in the selection.
    st.subheader("Risk Level Summary")
    if not filtered_df.empty:
        risk_summary = filtered_df["Risk Level"].value_counts().rename_axis("Risk Level").reset_index(name="Students")
        st.dataframe(styled_students(risk_summary), hide_index=True, width="stretch")
    else:
        st.info("No risk summary available for the selected filters.")

    # Let users show/hide matching records and download those records as CSV.
    show_data = st.checkbox("Show Filtered Dataset", True)

    if show_data:
        st.subheader("Filtered Student Records")
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

    # Reindex keeps all three risk cards visible, including categories with zero students.
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

    # Built-in bar charts: student scores use risk colors; course bars show counts.
    st.subheader("Streamlit Charts")
    simple_columns = st.columns(2)
    with simple_columns[0]:
        st.write("Student Scores")
        if not filtered_df.empty:
            score_chart = filtered_df[["Student Name", "Score", "Risk Level"]].copy()
            score_chart["Color"] = score_chart["Risk Level"].map(dict(zip(RISK_ORDER, RISK_COLORS)))
            st.bar_chart(score_chart, x="Student Name", y="Score", color="Color")
        else:
            st.info("No score chart available.")
    with simple_columns[1]:
        st.write("Students by Course")
        if not filtered_df.empty:
            course_count = filtered_df["Course"].value_counts()
            st.bar_chart(course_count, color="#4776E6")
        else:
            st.info("No course count chart available.")

    # Plotly adds hover details and interactive controls. Skip charts for empty data.
    st.subheader("Interactive Plotly Charts")
    plotly_columns = st.columns(2)
    colors = dict(zip(RISK_ORDER, RISK_COLORS))
    with plotly_columns[0]:
        if not filtered_df.empty:
            fig_risk = px.bar(risk_summary, x="Risk Level", y="Students", color="Risk Level",
                              title="Risk Level Distribution", color_discrete_map=colors,
                              category_orders={"Risk Level": RISK_ORDER}, text="Students")
            fig_risk.update_yaxes(dtick=1)
            st.plotly_chart(fig_risk, width='stretch', key="plotly_risk")
        else:
            st.info("No risk distribution chart available.")
    with plotly_columns[1]:
        if not filtered_df.empty:
            fig_score = px.bar(filtered_df, x="Student Name", y="Score", color="Risk Level",
                               title="Student Scores by Risk Level", color_discrete_map=colors,
                               category_orders={"Risk Level": RISK_ORDER},
                               hover_data=["Course", "Attendance", "Study Hours"])
            fig_score.update_yaxes(range=[0,100])
            st.plotly_chart(fig_score, width='stretch', key="plotly_scores")
        else:
            st.info("No score chart available.")

    # Preserve earlier Altair charts in a collapsible section to keep the dashboard tidy.
    with st.expander("Additional Charts · Course colors and risk doughnut"):
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
                # Divide category counts by the filtered total to show percentage tooltips.
                pie_data["Share"] = pie_data["Students"] / len(filtered_df)
                donut = alt.Chart(pie_data).mark_arc(innerRadius=65, cornerRadius=4).encode(
                    theta=alt.Theta("Students:Q", stack=True), color=risk_color(),
                    order=alt.Order("Risk Level:N", sort="ascending"),
                    tooltip=["Risk Level:N", "Students:Q", alt.Tooltip("Share:Q", format=".0%")],
                ).properties(height=280)
                st.altair_chart(donut, width="stretch")
                st.caption("Share of students matching the current filters.")

    st.info(
        "Ethics Reminder: Visualizations should support students and guide academic support decisions, "
        "not label or punish them."
    )

# STUDENT DATA PAGE: show the full dataset, independent of Dashboard filters.
elif selected_page == "Student Data":
    st.title("Student Data")

    total_students = len(student_df)
    average_score = student_df["Score"].mean()
    average_attendance = student_df["Attendance"].mean()
    high_risk_students = student_df[
        student_df["Risk Level"] == "High Risk"
    ].shape[0]

    # Each tuple supplies the label, value, and styling key for one summary card.
    st.subheader("Student Summary")
    summary_metrics = [
        ("Total Students", total_students, "metric_students"),
        ("Average Score", f"{average_score:.2f}", "metric_score"),
        ("Average Attendance", f"{average_attendance:.1f}%", "metric_attendance"),
        ("High Risk Students", high_risk_students, "metric_risk"),
        ("Low Score Students", int((student_df["Score"] < 60).sum()), "metric_low_score"),
    ]
    for column, (label, value, card_key) in zip(st.columns(5), summary_metrics):
        with column:
            with st.container(key=card_key):
                st.metric(label, value, border=True)

    # Explain dataset dimensions and columns, then show a preview and the full table.
    st.subheader("Data Inspection")
    st.caption(f"{student_df.shape[0]} rows · {student_df.shape[1]} columns")
    column_descriptions = {
        "Student Name": "Name of the student",
        "Course": "Course the student is taking",
        "Score": "Academic score out of 100",
        "Attendance": "Attendance percentage",
        "Study Hours": "Recorded study hours",
        "Risk Level": "Calculated Low, Medium, or High Risk classification",
    }
    inspection_df = pd.DataFrame({
        "Column": student_df.columns.tolist(),
        "Description": [column_descriptions.get(name, "Student data field")
                        for name in student_df.columns],
    })
    st.dataframe(inspection_df, hide_index=True, width="stretch")

    st.subheader("First 5 Rows")
    st.dataframe(styled_students(student_df.head()), hide_index=True, width="stretch")

    st.subheader("Full Student Dataset")
    st.dataframe(styled_students(student_df), hide_index=True, width="stretch")

# RISK CHECKER PAGE: validate one submission and retain valid checks in session memory.
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

    # A form batches input changes until Check Risk is clicked.
    # Number-input bounds restrict score and attendance to 0–100.
    with st.form("risk_checker_form"):
        input_name = st.text_input("Student Name")
        input_score = st.number_input("Score", 0, 100, 50)
        input_attendance = st.number_input("Attendance", 0, 100, 50)

        submitted = st.form_submit_button("Check Risk")

    # Process only submitted forms; strip removes whitespace around the name.
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

            # Save exactly one valid result per submission, without changing the CSV.
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

    # Clear memory before rendering the table so it disappears immediately on click.
    st.subheader("Recent Risk Checks")

    if st.session_state["risk_history"]:
        if st.button("Clear History"):
            st.session_state["risk_history"] = []
            st.success("Risk check history cleared.")

    # Convert saved dictionaries into a table; otherwise display the empty-history message.
    if st.session_state["risk_history"]:
        history_df = pd.DataFrame(st.session_state["risk_history"])
        st.dataframe(styled_students(history_df), hide_index=True, width="stretch")
    else:
        st.info("No risk checks yet.")

    st.warning(
        "Ethics Reminder: Risk results should be used as guidance for support, "
        "not as final judgment about a student."
    )

# ABOUT PAGE: describe the current lab and responsible use of student information.
else:
    st.title("About")

    st.write("This app is part of Lab 05.")
    st.write("Course: Web App Development for Data Science")
    st.write("Project Theme: EduRisk Analytics")
    st.write("Topic: Visualization and Interactivity")

    st.info(
        "This version improves the Dashboard page using grouped summaries, "
        "interactive filters, Streamlit charts, and Plotly charts."
    )

    st.warning(
        "Ethics Reminder: Student performance visualizations should be used "
        "responsibly to support learning and student success."
    )
