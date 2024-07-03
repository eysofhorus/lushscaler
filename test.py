import streamlit as st
import serial
import serial.tools.list_ports

def capture_data(port, baud_rate=9600):
    try:
        ser = serial.Serial(port, baud_rate, timeout=1)
        # Assuming the scale sends a line of data continuously
        reading = ser.readline().decode().strip()  # Read and decode the data
        ser.close()
        return reading
    except Exception as e:
        return str(e)

def button_data():
    # Get available COM ports
    ports = [port.device for port in serial.tools.list_ports.comports()]
    if not ports:
        st.error("No COM ports detected. Make sure your device is connected.")
        return

    # Display select boxes for COM port and baud rate
    selected_port = st.selectbox("Select Port", ports, key="select_port")
    baudrates = [1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200]
    selected_baudrate = st.selectbox("Select Baudrate", baudrates, key="select_baudrate")

    if st.button('Click Me'):
        data_cap = capture_data(selected_port, selected_baudrate)
        st.write("Data captured:", data_cap)

button_data()
