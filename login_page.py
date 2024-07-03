import streamlit as st
import pyodbc

# Function to check login credentials and fetch user's name
def check_login(staff_id, password):
    conn_str = (
        r"DRIVER={ODBC Driver 17 for SQL Server};"
        r"SERVER=DUF-COR-AUSTIN;"
        r"DATABASE=lushscaler;"
        r"UID=sas;"
        r"PWD=Laptop@2024"
    )
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT staffid, password, surname, firstname, status 
            FROM dbo.Users 
            WHERE staffid = ? AND password = ?
        """, (staff_id, password))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            if result.status != 'Active':
                st.error("Your account has been deactivated. Please contact the administrator.")
                return False
            st.session_state.user_name = f"{result.surname} {result.firstname}"
            st.session_state.staff_id = result.staffid  # Save StaffID to session state
            return True
        else:
            return False
    except Exception as e:
        st.error(f"Error connecting to the database: {e}")
        return False

# Login Page Function
def show_login_page():
    st.title("LUSH SCALER")
    st.subheader("Please log in")

    staff_id = st.text_input("Staff ID")
    password = st.text_input("Password", type="password")

    if st.button("Log In"):
        if check_login(staff_id, password):
            st.session_state.logged_in = True
            st.success("Login successful")
            st.rerun()  
        else:
            st.error("Invalid Staff ID or Password")
