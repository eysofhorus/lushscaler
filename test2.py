# test2.py

import streamlit as st
import serial

# Function to read weight from the scale using selected COM port and baud rate
def read_scale(selected_port, selected_baudrate):
    try:
        # Initialize serial connection with selected port and baud rate
        ser = serial.Serial(selected_port, selected_baudrate, timeout=1)
        st.write(f"Serial port '{selected_port}' opened successfully.")
        
        # Read weight data from scale
        weight = ser.readline().strip()
        
        # Close serial port
        ser.close()
        
        return weight.decode('utf-8')  # Decode bytes to string
    except Exception as e:
        st.error(f"Error reading from scale: {e}")
        return None

# Test2 Page
def test2_page():
    st.title("Scale Test2 Page")

    # Ensure configuration is done before proceeding
    if not st.session_state.configured:
        st.warning("Please configure the application first.")
        return

    selected_port = st.session_state.selected_port
    selected_baudrate = st.session_state.selected_baudrate

    if st.button("Read Scale"):
        weight = read_scale(selected_port, selected_baudrate)
        if weight:
            st.success(f"Weight read from scale: {weight}")
        else:
            st.error("Failed to read weight from scale.")
    

if __name__ == '__main__':
    st.set_page_config(page_title="Scale Test2 Page")
    test2_page()
