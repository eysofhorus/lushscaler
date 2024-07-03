import streamlit as st
import pyodbc
import pandas as pd
import plotly.express as px

# Function to fetch data from weight_log table
def fetch_measurements():
    if 'staff_id' not in st.session_state:
        st.error("No staff ID found in session state.")
        return pd.DataFrame()

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
            SELECT log_date AS Date, shift AS Shift, line AS Line, sku AS SKU, ColorName, weight AS Weight, Staffid
            FROM lushscaler.dbo.weight_log
            WHERE Staffid = ?
        """, (st.session_state.staff_id,))
        rows = cursor.fetchall()
        
        # Extract column names
        columns = [column[0] for column in cursor.description]
        
        conn.close()
        
        # Convert to DataFrame
        df = pd.DataFrame.from_records(rows, columns=columns)
        return df
    except Exception as e:
        st.error(f"Error fetching measurements: {e}")
        return pd.DataFrame()

# Function to create dashboard page
def dashboard_page():
    st.title("Dashboard Page")
    
    # Fetch data from database
    df = fetch_measurements()
    
    if not df.empty:
        st.subheader("Measurement Data")
        
        # # Create scatter plot
        # fig = px.scatter(df, x='Date', y='Weight', color='SKU', size='Weight', hover_data=['Shift', 'Line', 'ColorName'],
        #                  title='Weight Measurement by Date and SKU')
        # fig.update_layout(xaxis_title='Date', yaxis_title='Weight (kg)')
        # st.plotly_chart(fig)

        # # Create bar graph for total weight per SKU by shift
        # bar_fig = px.bar(df, x='SKU', y='Weight', color='Shift', hover_data=['Line', 'ColorName', 'Date'],
        #                  title='Total Weight per SKU by Shift', barmode='group')
        # bar_fig.update_layout(xaxis_title='SKU', yaxis_title='Total Weight (kg)')
        # st.plotly_chart(bar_fig)

        # # Create bar graph for monthly total weight per SKU
        # df['Month'] = pd.to_datetime(df['Date']).dt.to_period('M').astype(str)  
        # monthly_df = df.groupby(['Month', 'SKU']).agg({'Weight': 'sum'}).reset_index()
        # monthly_bar_fig = px.bar(monthly_df, x='Month', y='Weight', color='SKU', hover_data=['SKU'],
        #                          title='Monthly Total Weight per SKU', barmode='group')
        # monthly_bar_fig.update_layout(xaxis_title='Month', yaxis_title='Total Weight (kg)')
        # st.plotly_chart(monthly_bar_fig)

        # Create pie chart for total weight by SKU
        pie_fig = px.pie(df, values='Weight', names='SKU', title='Total Weight Distribution by SKU')
        st.plotly_chart(pie_fig)

        # Display data table 
        st.write("DATA TABLE")
        st.dataframe(df)
    else:
        st.warning("No measurements found.")

if __name__ == "__main__":
    dashboard_page()
