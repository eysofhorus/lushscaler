import streamlit as st
import pyodbc

# SKU Selection Page Function


def setup_page():
    st.title("Setup Page - SKU Selection")

    sku_options = fetch_sku_options()

    shift_options = ["Shift1", "Shift2", "Shift3"]
    line_options = ["Line1", "Line2", "Line3"]

    cols = st.columns(3)
    with cols[0]:
        selected_sku = st.selectbox(
            "Select SKU", sku_options, key="select_sku")
    with cols[1]:
        selected_shift = st.selectbox(
            "Select Shift", shift_options, key="select_shift")
    with cols[2]:
        selected_line = st.selectbox(
            "Select Line", line_options, key="select_line")

    if st.button("Confirm Selection", key="confirm_selection"):
        st.session_state.selected_sku = selected_sku
        st.session_state.selected_shift = selected_shift
        st.session_state.selected_line = selected_line
        st.success("Selection confirmed.")

# Function to fetch SKU options from database


def fetch_sku_options():
    conn_str = (
        r"DRIVER={ODBC Driver 17 for SQL Server};"
        r"SERVER=DUF-COR-AUSTIN;"
        r"DATABASE=IOU;"
        r"UID=sas;"
        r"PWD=Laptop@2024"
    )
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("SELECT SKU FROM lushscaler.dbo.Product")
        sku_options = [row.SKU for row in cursor.fetchall()]
        conn.close()
        return sku_options
    except Exception as e:
        st.error(f"Error fetching SKU options: {e}")
        return []


if __name__ == "__main__":
    setup_page()
