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


# --- PDF Generation Function ---
# This function creates the PDF report using the FPDF library
def create_pdf(employee_data, results, overall_score):
    """Generates a professional PDF report from assessment data with branding."""
    pdf = FPDF()
    pdf.add_page()

    # --- Header with Logo ---
    if os.path.exists(LOGO_PATH):
        # Position logo on the top left
        pdf.image(LOGO_PATH, x=10, y=8, w=33)

    pdf.set_font("Arial", 'B', 18)
    # Set text color to dark brown
    pdf.set_text_color(89, 29, 7)  # Corresponds to #591D07
    pdf.cell(0, 10, "Employee Self-Assessment Report", 0, 1, 'C')
    pdf.set_text_color(0, 0, 0)  # Reset to black
    pdf.ln(15)

    # --- Employee Information Table ---
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(50, 8, "Employee Name:", 0, 0)
    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 8, employee_data['name'], 0, 1)

    pdf.set_font("Arial", 'B', 11)
    pdf.cell(50, 8, "Manager Name:", 0, 0)
    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 8, employee_data['manager'], 0, 1)

    pdf.set_font("Arial", 'B', 11)
    pdf.cell(50, 8, "Assessment Period:", 0, 0)
    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 8, employee_data['period'], 0, 1)

    pdf.set_font("Arial", 'B', 11)
    pdf.cell(50, 8, "Date of Generation:", 0, 0)
    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 8, datetime.date.today().strftime("%B %d, %Y"), 0, 1)

    # --- Overall Score ---
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(50, 10, "Overall Score:", 0, 0)
    pdf.set_font("Arial", 'B', 12)
    # Use dark brown for the score text
    pdf.set_text_color(89, 29, 7)
    pdf.cell(0, 10, f"{overall_score:.1f}%", 0, 1)
    pdf.set_text_color(0, 0, 0)  # Reset to black
    pdf.ln(10)

    # --- Results Section ---
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Assessment Results", 0, 1, 'L')

    # Set table header with brand colors
    pdf.set_font("Arial", 'B', 10)
    pdf.set_fill_color(191, 144, 86)  # Corresponds to #BF9056
    pdf.set_text_color(255, 255, 255)  # White text for contrast
    pdf.cell(90, 8, "Individual KPI", 1, 0, 'C', 1)
    pdf.cell(60, 8, "Employee Input Figures", 1, 0, 'C', 1)
    pdf.cell(40, 8, "Result / Score", 1, 1, 'C', 1)
    pdf.set_text_color(0, 0, 0)  # Reset text color

    # Table rows
    pdf.set_font("Arial", '', 10)

    for category, kpis in results.items():
        if not kpis:
            continue
        pdf.set_font("Arial", 'B', 11)
        pdf.set_fill_color(242, 182, 109)  # Corresponds to #F2B66D
        pdf.cell(190, 10, category, 1, 1, 'L', 1)
        pdf.set_font("Arial", '', 10)
        for kpi, data in kpis.items():
            y_before = pdf.get_y()
            pdf.multi_cell(90, 8, kpi, 1, 'L')
            y_after_kpi = pdf.get_y()
            pdf.set_y(y_before)
            pdf.set_x(10 + 90)

            pdf.multi_cell(60, 8, data['inputs'], 1, 'L')
            y_after_inputs = pdf.get_y()
            pdf.set_y(y_before)
            pdf.set_x(10 + 90 + 60)

            pdf.multi_cell(40, 8, data['result'], 1, 'C')
            y_after_result = pdf.get_y()

            pdf.set_y(max(y_after_kpi, y_after_inputs, y_after_result))

    # --- Signature Section ---
    pdf.ln(25)
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
st.set_page_config(layout="wide", page_title="Self-Assessment PDF Generator")
local_css()

st.title("Self-Assessment PDF Generator")
st.markdown(
    "Fill in the details below to generate your performance assessment report. Once generated, you can print the PDF to discuss with your manager.")

st.sidebar.header("Employee Details")
if os.path.exists(LOGO_PATH):
    st.sidebar.image(LOGO_PATH)

emp_name = st.sidebar.text_input("Your Full Name")
emp_manager = st.sidebar.text_input("Your Direct Manager's Name")
emp_period = st.sidebar.text_input("Assessment Period (e.g., Q3 2025)")

results = {"Financial": {}, "Processes": {}, "Customers": {}, "Teams": {}}

st.header("KPI Assessment")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    with st.expander("Category: Processes", expanded=True):
        st.subheader("Task Completion")
        tasks_completed = st.number_input("How many tasks were completed?", min_value=0, step=1, key="p1_comp")
        tasks_planned = st.number_input("How many tasks were planned?", min_value=0, step=1, key="p1_plan")

        st.subheader("Incident Resolution Time")
        total_time_incidents = st.number_input("What was the total time spent resolving incidents (hours)?",
                                               min_value=0.0, step=0.5, key="p2_time")
        total_incidents = st.number_input("How many incidents were resolved?", min_value=0, step=1, key="p2_inc")

        st.subheader("Root Cause Analysis")
        incidents_root_cause = st.number_input("How many incidents had a documented root cause?", min_value=0, step=1,
                                               key="p3_root")
        total_incidents_occurred = st.number_input("How many incidents occurred?", min_value=0, step=1, key="p3_total")

with col2:
    with st.expander("Category: Customers", expanded=True):
        st.subheader("Customer Satisfaction")
        positive_responses = st.number_input("What was the total number of satisfied (positive ratings)?", min_value=0,
                                             step=1, key="c1_pos")
        total_responses = st.number_input("What was the total number of survey responses?", min_value=0, step=1,
                                          key="c1_total")

        st.subheader("Average Response Time")
        total_response_time = st.number_input("What was the total time spent before first response (hours)?",
                                              min_value=0.0, step=0.5, key="c2_time")
        total_tickets = st.number_input("How many tickets were handled?", min_value=0, step=1, key="c2_tickets")

        st.subheader("First Call Resolution Rate")
        tickets_first_contact = st.number_input("How many tickets were resolved on first contact?", min_value=0, step=1,
                                                key="c3_first")
        total_tickets_handled = st.number_input("How many tickets were handled in total?", min_value=0, step=1,
                                                key="c3_total")

with st.expander("Category: Teams", expanded=True):
    t_col1, t_col2 = st.columns(2)
    with t_col1:
        st.subheader("Certification Attainment")
        staff_certified = st.number_input("How many IT staff currently hold valid certifications?", min_value=0, step=1,
                                          key="t1_cert")
        staff_total = st.number_input("How many IT staff are there in total?", min_value=0, step=1, key="t1_total")

        st.subheader("Training Completion Rate")
        mandatory_completed = st.number_input("How many staff completed mandatory training?", min_value=0, step=1,
                                              key="t2_comp")
        mandatory_required = st.number_input("How many staff were required to complete it?", min_value=0, step=1,
                                             key="t2_req")

    with t_col2:
        st.subheader("Team Satisfaction")
        staff_satisfied = st.number_input("How many staff responded positive/satisfied in the pulse survey?",
                                          min_value=0, step=1, key="t3_sat")
        staff_responded = st.number_input("How many staff responded in total?", min_value=0, step=1, key="t3_resp")

        st.subheader("Project Success Rate")
        projects_successful = st.number_input("How many IT projects were completed successfully?", min_value=0, step=1,
                                              key="t4_succ")
        projects_total = st.number_input("How many projects in total?", min_value=0, step=1, key="t4_total")

st.markdown("---")

if st.button("Generate Assessment PDF"):
    if not emp_name or not emp_manager or not emp_period:
        st.warning("Please fill in all Employee Details in the sidebar first.")
    else:
        processes_scores = []
        customers_scores = []
        teams_scores = []

        # --- Perform Calculations ---
        # Processes
        task_ratio = (tasks_completed / tasks_planned) * 100 if tasks_planned > 0 else 0
        processes_scores.append(task_ratio)
        results["Processes"]["Task Completion"] = {"inputs": f"{tasks_completed} / {tasks_planned}",
                                                   "result": f"{task_ratio:.1f}%"}

        avg_res_time = total_time_incidents / total_incidents if total_incidents > 0 else 0
        results["Processes"]["Incident Resolution Time"] = {
            "inputs": f"{total_time_incidents} hrs / {total_incidents} incidents",
            "result": f"{avg_res_time:.1f} hrs/inc"}

        root_cause_ratio = (
                                       incidents_root_cause / total_incidents_occurred) * 100 if total_incidents_occurred > 0 else 0
        processes_scores.append(root_cause_ratio)
        results["Processes"]["Root Cause Analysis"] = {"inputs": f"{incidents_root_cause} / {total_incidents_occurred}",
                                                       "result": f"{root_cause_ratio:.1f}%"}

        # Customers
        csat_ratio = (positive_responses / total_responses) * 100 if total_responses > 0 else 0
        customers_scores.append(csat_ratio)
        results["Customers"]["Customer Satisfaction"] = {"inputs": f"{positive_responses} / {total_responses}",
                                                         "result": f"{csat_ratio:.1f}% (CSAT)"}

        avg_response = total_response_time / total_tickets if total_tickets > 0 else 0
        results["Customers"]["Average Response Time"] = {
            "inputs": f"{total_response_time} hrs / {total_tickets} tickets",
            "result": f"{avg_response:.1f} hrs/ticket"}

        fcr_ratio = (tickets_first_contact / total_tickets_handled) * 100 if total_tickets_handled > 0 else 0
        customers_scores.append(fcr_ratio)
        results["Customers"]["First Call Resolution Rate"] = {
            "inputs": f"{tickets_first_contact} / {total_tickets_handled}", "result": f"{fcr_ratio:.1f}%"}

        # Teams
        cert_ratio = (staff_certified / staff_total) * 100 if staff_total > 0 else 0
        teams_scores.append(cert_ratio)
        results["Teams"]["Certification Attainment"] = {"inputs": f"{staff_certified} / {staff_total}",
                                                        "result": f"{cert_ratio:.1f}%"}

        training_ratio = (mandatory_completed / mandatory_required) * 100 if mandatory_required > 0 else 0
        teams_scores.append(training_ratio)
        results["Teams"]["Training Completion Rate"] = {"inputs": f"{mandatory_completed} / {mandatory_required}",
                                                        "result": f"{training_ratio:.1f}%"}

        team_sat_ratio = (staff_satisfied / staff_responded) * 100 if staff_responded > 0 else 0
        teams_scores.append(team_sat_ratio)
        results["Teams"]["Team Satisfaction"] = {"inputs": f"{staff_satisfied} / {staff_responded}",
                                                 "result": f"{team_sat_ratio:.1f}%"}

        proj_success_ratio = (projects_successful / projects_total) * 100 if projects_total > 0 else 0
        teams_scores.append(proj_success_ratio)
        results["Teams"]["Project Success Rate"] = {"inputs": f"{projects_successful} / {projects_total}",
                                                    "result": f"{proj_success_ratio:.1f}%"}

        processes_avg = sum(processes_scores) / len(processes_scores) if processes_scores else 0
        customers_avg = sum(customers_scores) / len(customers_scores) if customers_scores else 0
        teams_avg = sum(teams_scores) / len(teams_scores) if teams_scores else 0

        weights = {'processes': 0.30, 'customers': 0.30, 'teams': 0.20}
        total_weight = sum(weights.values())

        overall_score = 0
        if total_weight > 0:
            weighted_sum = (processes_avg * weights['processes']) + \
                           (customers_avg * weights['customers']) + \
                           (teams_avg * weights['teams'])
            overall_score = weighted_sum / total_weight

        employee_details = {"name": emp_name, "manager": emp_manager, "period": emp_period}
        pdf_bytes = create_pdf(employee_details, results, overall_score)

        b64 = base64.b64encode(pdf_bytes).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="Self_Assessment_{emp_name.replace(" ", "_")}.pdf">Download Your PDF Report</a>'
        st.success("Your PDF report has been generated!")
        st.markdown(href, unsafe_allow_html=True)

