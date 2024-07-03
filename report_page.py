import streamlit as st
import pyodbc
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# Function to fetch data from weight_log table
def fetch_weight_log(staff_id):
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

        # Adjusted SQL query to match column names in the database and filter by staff_id
        cursor.execute("""
            SELECT log_date AS Date, log_time AS Time, shift AS Shift, line AS Line, sku AS SKU, ColorName, weight AS Weight, Staffid
            FROM lushscaler.dbo.weight_log
            WHERE Staffid = ?
        """, (staff_id,))
        rows = cursor.fetchall()

        # Extract column names
        columns = [column[0] for column in cursor.description]

        conn.close()

        # Convert to DataFrame
        df = pd.DataFrame.from_records(rows, columns=columns)
        return df
    except Exception as e:
        st.error(f"Error fetching weight log: {e}")
        return pd.DataFrame()

# Function to generate daily, monthly, yearly, and all-time reports
def generate_report(df, report_type):
    df['Date'] = pd.to_datetime(df['Date'])
    if report_type == "Daily":
        report_df = df.groupby([df['Date'].dt.date, 'Shift', 'Line', 'SKU', 'ColorName']).agg({'Weight': 'sum'}).reset_index()
        report_df.columns = ['Date', 'Shift', 'Line', 'SKU', 'ColorName', 'Total Weight']
    elif report_type == "Monthly":
        df['Month'] = df['Date'].dt.to_period('M').apply(lambda r: r.start_time)
        report_df = df.groupby(['Month', 'Shift', 'Line', 'SKU', 'ColorName']).agg({'Weight': 'sum'}).reset_index()
        report_df.columns = ['Month', 'Shift', 'Line', 'SKU', 'ColorName', 'Total Weight']
    elif report_type == "Yearly":
        df['Year'] = df['Date'].dt.to_period('Y').apply(lambda r: r.start_time)
        report_df = df.groupby(['Year', 'Shift', 'Line', 'SKU', 'ColorName']).agg({'Weight': 'sum'}).reset_index()
        report_df.columns = ['Year', 'Shift', 'Line', 'SKU', 'ColorName', 'Total Weight']
    elif report_type == "All":
        report_df = df
    else:
        report_df = pd.DataFrame()
    
    return report_df

# Function to create report page
def report_page():
    st.title("Report Page")

    # Ensure staff_id is in session state
    if 'staff_id' not in st.session_state:
        st.error("No staff ID found in session state.")
        return

    # Fetch data from database
    df = fetch_weight_log(st.session_state.staff_id)

    if df.empty:
        st.warning("No data found for the current user.")
        return

    # Select report type
    report_type = st.selectbox("Select Report Type", ["Daily", "Monthly", "Yearly", "All"])

    # Generate and display report
    report_df = generate_report(df, report_type)
    if not report_df.empty:
        st.subheader(f"{report_type} Report")

        if report_type == "Daily":
            fig = px.line(report_df, x='Date', y='Total Weight', color='SKU', title='Daily Total Weight by SKU', hover_data=['Shift', 'Line', 'ColorName'])
        elif report_type == "Monthly":
            fig = px.line(report_df, x='Month', y='Total Weight', color='SKU', title='Monthly Total Weight by SKU', hover_data=['Shift', 'Line', 'ColorName'])
        elif report_type == "Yearly":
            fig = px.line(report_df, x='Year', y='Total Weight', color='SKU', title='Yearly Total Weight by SKU', hover_data=['Shift', 'Line', 'ColorName'])
        elif report_type == "All":
            fig = px.scatter(report_df, x='Date', y='Weight', color='SKU', size='Weight', title='All-Time Weight Measurements', hover_data=['Shift', 'Line', 'ColorName', 'Time'])
        
        st.plotly_chart(fig)
        st.write("DATA TABLE")

        if report_type == "All":
            st.dataframe(report_df[['Date', 'Time', 'Shift', 'Line', 'SKU', 'ColorName', 'Weight']])
        else:
            st.dataframe(report_df)
    else:
        st.warning("No data available for the selected report type.")

if __name__ == "__main__":
    st.set_page_config(page_title="Report Page")
    report_page()
