import streamlit as st
import pyodbc
from datetime import datetime
import random

# Function to fetch colors and their codes for a selected SKU from the database
def fetch_colors_for_sku(sku):
    conn_str = (
        r"DRIVER={ODBC Driver 17 for SQL Server};"
        r"SERVER=DUF-COR-AUSTIN;"
        r"DATABASE=lushscaler;"
        r"UID=sas;"
        r"PWD=Laptop@2024"
    )
    
    colors = []
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        # Query to fetch colors for the selected SKU
        query = """
        SELECT c.ColorName, c.ColorCode
        FROM SKU_Color sc
        JOIN Color c ON sc.ColorName = c.ColorName
        WHERE sc.SKU = ?
        """
        cursor.execute(query, (sku,))
        rows = cursor.fetchall()
        
        # Extract color names and codes
        colors = [{'name': row.ColorName, 'code': row.ColorCode} for row in rows]
        
        conn.close()
    except Exception as e:
        st.error(f"Error fetching colors: {e}")
    
    return colors

# Function to save weight log to database
def save_weight_log(staff_id, sku, line, shift, color_name, weight):
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

        # Get current date and time
        log_date = datetime.now().date()
        log_time = datetime.now().time()

        # Insert query
        insert_query = """
        INSERT INTO weight_log (StaffID, sku, line, shift, ColorName, log_date, log_time, weight)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(insert_query, (staff_id, sku, line, shift, color_name, log_date, log_time, weight))
        conn.commit()
        conn.close()
        st.success("Weight log saved successfully.")
    except Exception as e:
        st.error(f"Error saving weight log: {e}")

# Function to generate random weight
def generate_random_weight():
    return round(random.uniform(10, 100), 2)  

# Measurement Page
def measurement_page():
    st.title("Measurement Page")

    if 'measurements' not in st.session_state:
        st.session_state.measurements = 0

    if 'selected_color' not in st.session_state:
        st.session_state.selected_color = None

    if not st.session_state.selected_sku or not st.session_state.selected_line or not st.session_state.selected_shift:
        st.error("Please complete the setup page before taking measurements.")
        return

    selected_sku = st.session_state.selected_sku
    selected_line = st.session_state.selected_line
    selected_shift = st.session_state.selected_shift
    staff_id = st.session_state.staff_id  

    st.write(f"Selected SKU: {selected_sku}")
    st.write(f"Selected Line: {selected_line}")
    st.write(f"Selected Shift: {selected_shift}")

    # Fetch colors for the selected SKU from database
    colors = fetch_colors_for_sku(selected_sku)

    if not colors:
        st.warning("No colors found for selected SKU.")
    else:
        st.write("Select a color and measure:")
        
        num_columns = 4
        color_chunks = [colors[i:i + num_columns] for i in range(0, len(colors), num_columns)]
        
        for chunk in color_chunks:
            cols = st.columns(len(chunk))
            for index, color in enumerate(chunk):
                if cols[index].button(color['name'], key=f"color_button_{color['name']}_{index}"):
                    st.session_state.selected_color = color['name']
                    st.session_state.random_weight = generate_random_weight()
                    st.success(f"Measured weight for {color['name']}: {st.session_state.random_weight} kg")
                    result_data=f"<div style='font-size:80px;'>{st.session_state.random_weight}</div>"
                    st.write(result_data,unsafe_allow_html=True)

    # Show the selected color and measured weight
    if 'selected_color' in st.session_state and st.session_state.selected_color:
        st.write(f"Selected Color: {st.session_state.selected_color}")

        # Show save button only if a weight has been generated
        if 'random_weight' in st.session_state and st.session_state.random_weight:
            if st.button("Save"):
                save_weight_log(staff_id, selected_sku, selected_line, selected_shift, st.session_state.selected_color, st.session_state.random_weight)
                st.session_state.measurements += 1
                # Reset selected color and random weight
                st.session_state.selected_color = None
                st.session_state.random_weight = None

if __name__ == '__main__':
    st.set_page_config(page_title="Measurement Page")
    measurement_page()