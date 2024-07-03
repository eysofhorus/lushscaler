import streamlit as st
import serial.tools.list_ports

# Function to fetch available COM ports
def get_available_com_ports():
    com_ports = [port.device for port in serial.tools.list_ports.comports()]
    return com_ports

# Configuration Page Function
def configuration_page():
    st.title("Configuration Settings")

    ports = get_available_com_ports()
    selected_port = st.selectbox("Select Port", ports, key="select_port")
    baudrates = [1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200]
    selected_baudrate = st.selectbox("Select Baudrate", baudrates, key="select_baudrate")

    # Define the number input for bit level with the initial value from session state
    bit_level = st.number_input("Bit Level", min_value=1, step=1, key="bit_level", value=st.session_state.bit_level)

    if st.button("Save Configuration", key="save_config"):
        st.session_state.configured = True
        st.session_state.selected_port = selected_port
        st.session_state.selected_baudrate = selected_baudrate
        st.success("Configuration saved.")


if __name__ == "__main__":
    configuration_page()
