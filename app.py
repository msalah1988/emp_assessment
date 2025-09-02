import streamlit as st
from fpdf import FPDF
import base64
import datetime
import os

# --- Branding & Configuration ---
LOGO_PATH = "MC4 Logo.png"
# Colors from the provided palette
COLORS = {
    "primary_orange": "#F29F05",
    "secondary_peach": "#F2B66D",
    "accent_tan": "#BF9056",
    "dark_brown_text": "#591D07",
    "light_bg": "#F2E2F2"
}
# Category weights
WEIGHTS = {'financial': 0.20, 'processes': 0.30, 'customers': 0.30, 'teams': 0.20}


# --- PDF Generation Function ---
# This function creates the PDF report using the FPDF library
def create_pdf(employee_data, results, overall_score, weights):
    """Generates a professional PDF report from assessment data with branding."""
    pdf = FPDF()
    pdf.add_page()

    # --- Header with Logo ---
    if os.path.exists(LOGO_PATH):
        # Position logo on the top left, with size increased
        pdf.image(LOGO_PATH, x=10, y=8, w=20)

    pdf.set_font("Arial", 'B', 18)
    # Set text color to dark brown
    pdf.set_text_color(89, 29, 7)  # Corresponds to #591D07
    pdf.cell(0, 10, "Employee Assessment Report", 0, 1, 'C')
    pdf.set_text_color(0, 0, 0)  # Reset to black
    pdf.ln(10)  # Reduced vertical space

    # --- Employee Information Table (Two Columns) ---
    col1_width = 95
    col2_x_start = 10 + col1_width

    # Row 1: Name and Period
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(50, 8, "Employee Name:", 0, 0)
    pdf.set_font("Arial", '', 11)
    pdf.cell(col1_width - 50, 8, employee_data['name'], 0, 0)

    pdf.set_x(col2_x_start)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(50, 8, "Assessment Period:", 0, 0)
    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 8, employee_data['period'], 0, 1)

    # Row 2: ID and Date
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(50, 8, "Employee ID Number:", 0, 0)
    pdf.set_font("Arial", '', 11)
    pdf.cell(col1_width - 50, 8, employee_data['id'], 0, 0)

    pdf.set_x(col2_x_start)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(50, 8, "Date of Generation:", 0, 0)
    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 8, datetime.date.today().strftime("%B %d, %Y"), 0, 1)

    # Row 3: Manager and Score
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(50, 8, "Manager Name:", 0, 0)
    pdf.set_font("Arial", '', 11)
    pdf.cell(col1_width - 50, 8, employee_data['manager'], 0, 0)

    pdf.set_x(col2_x_start)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(50, 8, "Overall Score:", 0, 0)
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(89, 29, 7)
    pdf.cell(0, 8, f"{overall_score:.1f}%", 0, 1)
    pdf.set_text_color(0, 0, 0)  # Reset color

    pdf.ln(10)  # Space after the info block

    # --- Results Section ---
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Assessment Results", 0, 1, 'L')

    # Set table header with brand colors
    pdf.set_font("Arial", 'B', 10)
    pdf.set_fill_color(191, 144, 86)  # Corresponds to #BF9056
    pdf.set_text_color(255, 255, 255)  # White text for contrast
    pdf.cell(90, 7, "Individual KPI", 1, 0, 'C', 1)
    pdf.cell(60, 7, "Employee Input Figures", 1, 0, 'C', 1)
    pdf.cell(40, 7, "Result / Score", 1, 1, 'C', 1)
    pdf.set_text_color(0, 0, 0)  # Reset text color

    # Table rows
    pdf.set_font("Arial", '', 9)  # Reduced font size for content

    for category, kpis in results.items():
        if not kpis:
            continue

        weight_percent = int(weights.get(category.lower(), 0) * 100)
        category_title = f"{category} ({weight_percent}%)" if weight_percent > 0 else category

        pdf.set_font("Arial", 'B', 10)  # Reduced font size
        pdf.set_fill_color(242, 182, 109)  # Corresponds to #F2B66D
        pdf.cell(190, 8, category_title, 1, 1, 'L', 1)  # Reduced cell height
        pdf.set_font("Arial", '', 9)
        for kpi, data in kpis.items():
            CELL_HEIGHT = 6  # Reduced cell height for compactness
            y_before = pdf.get_y()
            pdf.multi_cell(90, CELL_HEIGHT, kpi, 1, 'L')
            y_after_kpi = pdf.get_y()
            pdf.set_y(y_before)
            pdf.set_x(10 + 90)

            pdf.multi_cell(60, CELL_HEIGHT, data['inputs'], 1, 'L')
            y_after_inputs = pdf.get_y()
            pdf.set_y(y_before)
            pdf.set_x(10 + 90 + 60)

            pdf.multi_cell(40, CELL_HEIGHT, data['result'], 1, 'C')
            y_after_result = pdf.get_y()

            pdf.set_y(max(y_after_kpi, y_after_inputs, y_after_result))

    # --- Signature Section ---
    pdf.ln(12)  # Reduced vertical space
    pdf.set_font("Arial", '', 12)
    pdf.cell(95, 10, "_____________________________", 0, 0, 'L')
    pdf.cell(95, 10, "_____________________________", 0, 1, 'L')
    pdf.cell(95, 6, "Employee Signature", 0, 0, 'L')
    pdf.cell(95, 6, "Direct Manager Signature", 0, 1, 'L')

    return pdf.output(dest='S')


# --- Inject Custom CSS for Streamlit Branding ---
def local_css():
    css = f"""
    <style>
        /* Main background color */
        .stApp {{
            background-color: {COLORS['light_bg']};
        }}
        /* Main text color */
        body, .stTextInput, .stNumberInput, .stMarkdown {{
            color: {COLORS['dark_brown_text']};
        }}
        /* Title color */
        h1, h2, h3 {{
            color: {COLORS['dark_brown_text']};
        }}
        /* Sidebar branding */
        .st-emotion-cache-16txtl3 {{
            background-color: #FFFFFF;
        }}
        /* Generate button styling */
        .stButton>button {{
            background-color: {COLORS['primary_orange']};
            color: white;
            border-radius: 5px;
            border: none;
            padding: 10px 20px;
        }}
        .stButton>button:hover {{
            background-color: {COLORS['accent_tan']};
            color: white;
        }}
        /* Expander headers */
        .st-emotion-cache-134p1ja {{
            background-color: {COLORS['secondary_peach']};
            border-radius: 5px;
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


# --- Streamlit App UI ---
st.set_page_config(layout="wide", page_title="Employee Assessment PDF Generator")
local_css()

st.title("Employee Assessment PDF Generator")
st.markdown(
    "Fill in the details below to generate your performance assessment report. Once generated, you can print the PDF to discuss with your manager.")

st.sidebar.header("Employee Details")
if os.path.exists(LOGO_PATH):
    st.sidebar.image(LOGO_PATH)

emp_name = st.sidebar.text_input("Your Full Name")
emp_id = st.sidebar.text_input("Your Employee ID Number")
emp_manager = st.sidebar.text_input("Your Direct Manager's Name")
emp_period = st.sidebar.text_input("Assessment Period (e.g., Q3 2025)")

results = {"Financial": {}, "Processes": {}, "Customers": {}, "Teams": {}}

st.header("KPI Assessment")
st.markdown("---")

# --- Form Columns ---
col1, col2 = st.columns(2)

with col1:
    with st.expander("Category: Financial", expanded=True):
        st.subheader("Project Completion Rate")
        projects_completed_scope = st.number_input("How many IT projects were delivered on time and within scope?",
                                                   min_value=0, step=1, key="f1_comp")
        projects_planned = st.number_input("How many projects were planned in total?", min_value=0, step=1,
                                           key="f1_plan")

        st.subheader("System Uptime")
        system_uptime_hours = st.number_input("What was the total system uptime (hours)?", min_value=0.0, step=0.5,
                                              key="f2_uptime")
        total_available_hours = st.number_input("What were the total available hours in the period?", min_value=0.0,
                                                step=0.5, key="f2_avail")

    with st.expander("Category: Customers", expanded=True):
        st.subheader("Customer Satisfaction")
        positive_responses = st.number_input("What was the total number of satisfied (positive ratings)?", min_value=0,
                                             step=1, key="c1_pos")
        total_responses = st.number_input("What was the total number of survey responses?", min_value=0, step=1,
                                          key="c1_total")

        st.subheader("Average Response Time")
        total_response_time = st.number_input("What was the total time spent before first response (hours)?",
                                              min_value=0.0, step=0.5, key="c2_time")
        total_tickets_resp = st.number_input("How many tickets were handled (for response time)?", min_value=0, step=1,
                                             key="c2_tickets")

        st.subheader("First Call Resolution Rate")
        tickets_first_contact = st.number_input("How many tickets were resolved on first contact?", min_value=0, step=1,
                                                key="c3_first")
        total_tickets_handled_fcr = st.number_input("How many tickets were handled in total (for FCR)?", min_value=0,
                                                    step=1, key="c3_total")

        st.subheader("Call Volume")
        tickets_handled_period = st.number_input("How many tickets/support calls were handled during the period?",
                                                 min_value=0, step=1, key="c4_handled")

        st.subheader("Tickets Closed vs. Opened")
        tickets_closed = st.number_input("How many tickets were closed?", min_value=0, step=1, key="c5_closed")
        tickets_opened = st.number_input("How many tickets were opened?", min_value=0, step=1, key="c5_opened")

with col2:
    with st.expander("Category: Processes", expanded=True):
        p_col1, p_col2 = st.columns(2)
        with p_col1:
            st.subheader("Tasks Completed")
            tasks_completed = st.number_input("How many tasks were completed?", min_value=0, step=1, key="p1_comp")
            tasks_planned_process = st.number_input("How many tasks were planned?", min_value=0, step=1, key="p1_plan")

            st.subheader("Root Cause Analysis")
            incidents_root_cause = st.number_input("How many incidents had a documented root cause?", min_value=0,
                                                   step=1, key="p3_root")
            total_incidents_occurred = st.number_input("How many incidents occurred?", min_value=0, step=1,
                                                       key="p3_total")

            st.subheader("Issue Escalation Rate")
            issues_escalated = st.number_input("How many issues were escalated beyond first-level?", min_value=0,
                                               step=1, key="p5_esc")
            total_issues_handled = st.number_input("How many total issues were handled?", min_value=0, step=1,
                                                   key="p5_total")

            st.subheader("Innovation Rate")
            ideas_adopted = st.number_input("How many new ideas/solutions were adopted?", min_value=0, step=1,
                                            key="p7_adopted")
            ideas_proposed = st.number_input("How many new ideas/solutions were proposed?", min_value=0, step=1,
                                             key="p7_proposed")

        with p_col2:
            st.subheader("Incident Resolution Time")
            total_time_incidents = st.number_input("Total time spent resolving incidents (hours)?", min_value=0.0,
                                                   step=0.5, key="p2_time")
            total_incidents = st.number_input("How many incidents were resolved?", min_value=0, step=1, key="p2_inc")

            st.subheader("Problem Prevention")
            preventive_actions = st.number_input("How many preventive actions were implemented?", min_value=0, step=1,
                                                 key="p4_actions")
            recurring_issues = st.number_input("How many recurring issues were reported?", min_value=0, step=1,
                                               key="p4_issues")

            st.subheader("Process Improvement")
            improvements_initiated = st.number_input("How many IT process improvements were initiated?", min_value=0,
                                                     step=1, key="p6_improv")

# --- Teams Category (Full Width) ---
with st.expander("Category: Teams", expanded=True):
    t_col1, t_col2, t_col3 = st.columns(3)
    with t_col1:
        st.subheader("Certification Attainment")
        staff_certified = st.number_input("How many staff hold valid certifications?", min_value=0, step=1,
                                          key="t1_cert")
        staff_total_cert = st.number_input("How many IT staff are there in total (for cert)?", min_value=0, step=1,
                                           key="t1_total")

        st.subheader("Training Completion Rate")
        mandatory_completed = st.number_input("How many staff completed mandatory training?", min_value=0, step=1,
                                              key="t3_comp")
        mandatory_required = st.number_input("How many staff were required to complete it?", min_value=0, step=1,
                                             key="t3_req")

        st.subheader("Project Success Rate")
        projects_successful = st.number_input("How many IT projects were completed successfully?", min_value=0, step=1,
                                              key="t6_succ")
        projects_total = st.number_input("How many projects in total?", min_value=0, step=1, key="t6_total")

    with t_col2:
        st.subheader("Technical Skill Proficiency")
        total_assessment_score = st.number_input("What was the total score across tech assessments?", min_value=0.0,
                                                 step=0.1, key="t2_score")
        staff_assessed = st.number_input("How many staff took the assessment?", min_value=0, step=1, key="t2_staff")

        st.subheader("Team Satisfaction")
        staff_satisfied = st.number_input("How many staff responded positive in pulse survey?", min_value=0, step=1,
                                          key="t4_sat")
        staff_responded = st.number_input("How many staff responded in total?", min_value=0, step=1, key="t4_resp")

        st.subheader("Knowledge Sharing")
        staff_contributed = st.number_input("How many staff contributed to knowledge-sharing?", min_value=0, step=1,
                                            key="t7_contrib")
        total_staff_ks = st.number_input("How many staff in total (for knowledge share)?", min_value=0, step=1,
                                         key="t7_total")

    with t_col3:
        st.subheader("Employee Development")
        employees_promoted = st.number_input("How many employees were promoted/role-enhanced?", min_value=0, step=1,
                                             key="t5_promo")
        total_employees = st.number_input("How many employees in total?", min_value=0, step=1, key="t5_total")

st.markdown("---")

if st.button("Generate Assessment PDF"):
    if not emp_name or not emp_manager or not emp_period or not emp_id:
        st.warning("Please fill in all Employee Details in the sidebar first.")
    else:
        financial_scores, processes_scores, customers_scores, teams_scores = [], [], [], []

        # --- Perform Calculations ---
        # Financial
        project_completion_ratio = (projects_completed_scope / projects_planned) * 100 if projects_planned > 0 else 0
        financial_scores.append(project_completion_ratio)
        results["Financial"]["Project Completion Rate"] = {"inputs": f"{projects_completed_scope} / {projects_planned}",
                                                           "result": f"{project_completion_ratio:.1f}%"}

        system_uptime_ratio = (system_uptime_hours / total_available_hours) * 100 if total_available_hours > 0 else 0
        financial_scores.append(system_uptime_ratio)
        results["Financial"]["System Uptime"] = {"inputs": f"{system_uptime_hours}h / {total_available_hours}h",
                                                 "result": f"{system_uptime_ratio:.1f}%"}

        # Processes
        task_ratio = (tasks_completed / tasks_planned_process) * 100 if tasks_planned_process > 0 else 0
        processes_scores.append(task_ratio)
        results["Processes"]["Tasks Completed"] = {"inputs": f"{tasks_completed} / {tasks_planned_process}",
                                                   "result": f"{task_ratio:.1f}%"}

        avg_res_time = total_time_incidents / total_incidents if total_incidents > 0 else 0
        results["Processes"]["Incident Resolution Time"] = {"inputs": f"{total_time_incidents}h / {total_incidents}",
                                                            "result": f"{avg_res_time:.1f} hrs/inc"}

        root_cause_ratio = (
                                       incidents_root_cause / total_incidents_occurred) * 100 if total_incidents_occurred > 0 else 0
        processes_scores.append(root_cause_ratio)
        results["Processes"]["Root Cause Analysis"] = {"inputs": f"{incidents_root_cause} / {total_incidents_occurred}",
                                                       "result": f"{root_cause_ratio:.1f}%"}

        problem_prevention_ratio = (preventive_actions / recurring_issues) * 100 if recurring_issues > 0 else 0
        processes_scores.append(problem_prevention_ratio)
        results["Processes"]["Problem Prevention"] = {"inputs": f"{preventive_actions} / {recurring_issues}",
                                                      "result": f"{problem_prevention_ratio:.1f}%"}

        escalation_ratio = (issues_escalated / total_issues_handled) * 100 if total_issues_handled > 0 else 0
        processes_scores.append(escalation_ratio)
        results["Processes"]["Issue Escalation Rate"] = {"inputs": f"{issues_escalated} / {total_issues_handled}",
                                                         "result": f"{escalation_ratio:.1f}%"}

        results["Processes"]["Process Improvement"] = {"inputs": f"{improvements_initiated} initiated",
                                                       "result": f"{improvements_initiated}"}

        innovation_ratio = (ideas_adopted / ideas_proposed) * 100 if ideas_proposed > 0 else 0
        processes_scores.append(innovation_ratio)
        results["Processes"]["Innovation Rate"] = {"inputs": f"{ideas_adopted} / {ideas_proposed}",
                                                   "result": f"{innovation_ratio:.1f}%"}

        # Customers
        csat_ratio = (positive_responses / total_responses) * 100 if total_responses > 0 else 0
        customers_scores.append(csat_ratio)
        results["Customers"]["Customer Satisfaction"] = {"inputs": f"{positive_responses} / {total_responses}",
                                                         "result": f"{csat_ratio:.1f}%"}

        avg_response = total_response_time / total_tickets_resp if total_tickets_resp > 0 else 0
        results["Customers"]["Average Response Time"] = {"inputs": f"{total_response_time}h / {total_tickets_resp}",
                                                         "result": f"{avg_response:.1f} hrs/tkt"}

        fcr_ratio = (tickets_first_contact / total_tickets_handled_fcr) * 100 if total_tickets_handled_fcr > 0 else 0
        customers_scores.append(fcr_ratio)
        results["Customers"]["First Call Resolution"] = {
            "inputs": f"{tickets_first_contact} / {total_tickets_handled_fcr}", "result": f"{fcr_ratio:.1f}%"}

        results["Customers"]["Call Volume"] = {"inputs": f"{tickets_handled_period} handled",
                                               "result": f"{tickets_handled_period}"}

        closed_ratio = (tickets_closed / tickets_opened) * 100 if tickets_opened > 0 else 0
        customers_scores.append(closed_ratio)
        results["Customers"]["Tickets Closed vs. Opened"] = {"inputs": f"{tickets_closed} / {tickets_opened}",
                                                             "result": f"{closed_ratio:.1f}%"}

        # Teams
        cert_ratio = (staff_certified / staff_total_cert) * 100 if staff_total_cert > 0 else 0
        teams_scores.append(cert_ratio)
        results["Teams"]["Certification Attainment"] = {"inputs": f"{staff_certified} / {staff_total_cert}",
                                                        "result": f"{cert_ratio:.1f}%"}

        avg_skill_score = total_assessment_score / staff_assessed if staff_assessed > 0 else 0
        results["Teams"]["Technical Skill Proficiency"] = {
            "inputs": f"{total_assessment_score} / {staff_assessed} staff", "result": f"{avg_skill_score:.1f} avg"}

        training_ratio = (mandatory_completed / mandatory_required) * 100 if mandatory_required > 0 else 0
        teams_scores.append(training_ratio)
        results["Teams"]["Training Completion"] = {"inputs": f"{mandatory_completed} / {mandatory_required}",
                                                   "result": f"{training_ratio:.1f}%"}

        team_sat_ratio = (staff_satisfied / staff_responded) * 100 if staff_responded > 0 else 0
        teams_scores.append(team_sat_ratio)
        results["Teams"]["Team Satisfaction"] = {"inputs": f"{staff_satisfied} / {staff_responded}",
                                                 "result": f"{team_sat_ratio:.1f}%"}

        promo_ratio = (employees_promoted / total_employees) * 100 if total_employees > 0 else 0
        teams_scores.append(promo_ratio)
        results["Teams"]["Employee Development"] = {"inputs": f"{employees_promoted} / {total_employees}",
                                                    "result": f"{promo_ratio:.1f}%"}

        proj_success_ratio = (projects_successful / projects_total) * 100 if projects_total > 0 else 0
        teams_scores.append(proj_success_ratio)
        results["Teams"]["Project Success Rate"] = {"inputs": f"{projects_successful} / {projects_total}",
                                                    "result": f"{proj_success_ratio:.1f}%"}

        knowledge_ratio = (staff_contributed / total_staff_ks) * 100 if total_staff_ks > 0 else 0
        teams_scores.append(knowledge_ratio)
        results["Teams"]["Knowledge Sharing"] = {"inputs": f"{staff_contributed} / {total_staff_ks}",
                                                 "result": f"{knowledge_ratio:.1f}%"}

        # --- Calculate Category and Overall Scores ---
        financial_avg = sum(financial_scores) / len(financial_scores) if financial_scores else 0
        processes_avg = sum(processes_scores) / len(processes_scores) if processes_scores else 0
        customers_avg = sum(customers_scores) / len(customers_scores) if customers_scores else 0
        teams_avg = sum(teams_scores) / len(teams_scores) if teams_scores else 0

        total_weight = sum(WEIGHTS.values())
        overall_score = 0
        if total_weight > 0:
            weighted_sum = (financial_avg * WEIGHTS['financial']) + \
                           (processes_avg * WEIGHTS['processes']) + \
                           (customers_avg * WEIGHTS['customers']) + \
                           (teams_avg * WEIGHTS['teams'])
            overall_score = weighted_sum / total_weight

        employee_details = {"name": emp_name, "id": emp_id, "manager": emp_manager, "period": emp_period}
        pdf_bytes = create_pdf(employee_details, results, overall_score, WEIGHTS)

        b64 = base64.b64encode(pdf_bytes).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="Employee_Assessment_{emp_name.replace(" ", "_")}.pdf">Download Your PDF Report</a>'
        st.success("Your PDF report has been generated!")
        st.markdown(href, unsafe_allow_html=True)

