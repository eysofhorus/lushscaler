import streamlit as st
from login_page import show_login_page
from configuration_page import configuration_page
from measure_page import measurement_page
from setup import setup_page
from report_page import report_page
from dashboard_page import dashboard_page
from test2 import test2_page  

# Set Streamlit page configuration
st.set_page_config(page_title="LUSH SCALER")

# Initialize session states
st.session_state.setdefault('logged_in', False)
st.session_state.setdefault('configured', False)
st.session_state.setdefault('selected_sku', None)
st.session_state.setdefault('selected_shift', None)
st.session_state.setdefault('selected_line', None)
st.session_state.setdefault('started', False)
st.session_state.setdefault('measurements', 0)
st.session_state.setdefault('staff_id', None)
st.session_state.setdefault('bit_level', 8)
st.session_state.setdefault('selected_port', None)
st.session_state.setdefault('selected_baudrate', None)

# Handle navigation and session management
if __name__ == '__main__':
    if not st.session_state.logged_in:
        show_login_page()
    else:
        st.sidebar.title("Navigation")
        page = st.sidebar.radio("Go to", ["Dashboard", "Configuration", "Setup", "Measure", "Report", "Test2"])  # Add "Test2" to the sidebar options

        if page == "Dashboard":
            dashboard_page()
        elif page == "Configuration":
            configuration_page()
        elif page == "Setup":
            setup_page()
        elif page == "Measure":
            measurement_page()
        elif page == "Report":
            report_page()
        elif page == "Test2":  
            test2_page()  

        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.configured = False
            st.session_state.started = False
            st.session_state.measurements = 0
            st.session_state.staff_id = None
