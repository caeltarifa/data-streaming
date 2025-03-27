import streamlit as st
import time
import threading
import pandas as pd
import os

from kafka_client import KafkaConsumerClient
from data_processor import DataProcessor
from visualization import create_chart
from utils import setup_logging, log_message

# Setup logging
logger = setup_logging()

# Set page config
st.set_page_config(
    page_title="Real-Time Pressure & Temperature Monitor",
    page_icon="🌡️",
    layout="wide",
)

# Create a lock for thread-safe operations
data_lock = threading.Lock()

# Initialize session state variables
def init_session_state():
    if 'data' not in st.session_state:
        st.session_state.data = pd.DataFrame({
            'timestamp': [],
            'pressure': [],
            'temperature': [],
            'source': []  # 'kafka' or 'waiting'
        })

    if 'kafka_connected' not in st.session_state:
        st.session_state.kafka_connected = False

    if 'last_update' not in st.session_state:
        st.session_state.last_update = time.time()
        
    if 'update_thread_running' not in st.session_state:
        st.session_state.update_thread_running = False
        
    if 'data_points_to_keep' not in st.session_state:
        st.session_state.data_points_to_keep = 100
        
    if 'waiting_for_data' not in st.session_state:
        st.session_state.waiting_for_data = True

# Initialize session state
init_session_state()

# Global variables for thread access
kafka_client = None
data_processor = None

def main():
    global kafka_client, data_processor
    
    # Page header
    st.title("Real-Time Pressure & Temperature Monitor")
    
    # Sidebar configurations
    with st.sidebar:
        st.header("Configuration")
        
        # Kafka connection settings
        st.subheader("Kafka Settings")
        kafka_bootstrap_servers = st.text_input("Bootstrap Servers", "localhost:9092")
        kafka_topic = st.text_input("Topic", "sensors")
        kafka_group_id = st.text_input("Consumer Group ID", "streamlit-app")
        
        # Data retention settings
        st.subheader("Data Settings")
        data_points = st.slider("Data Points to Display", 10, 500, 100)
        # Update session state
        st.session_state.data_points_to_keep = data_points
        
        # Connect to Kafka button
        kafka_connect_button = st.button("Connect to Kafka")
        
        # Kafka connection status indicator
        if st.session_state.kafka_connected:
            st.success("✅ Connected to Kafka")
        else:
            st.error("❌ Not connected to Kafka")
            
        # Note about Kafka Producer
        st.subheader("Producer Information")
        st.info("""
            To generate data, start the Kafka producer:
            ```
            python kafka_producer.py
            ```
            This will send data to the Kafka topic every 3 seconds.
        """)
    
    # Create metrics containers for current values
    col1, col2, col3 = st.columns(3)
    with col1:
        pressure_metric = st.empty()
    with col2:
        temperature_metric = st.empty()
    with col3:
        data_source_indicator = st.empty()
    
    # Create chart container
    chart_container = st.empty()
    
    # Last update time indicator
    update_time_container = st.empty()
    
    # Error message container
    error_container = st.empty()
    
    # Initialize Kafka client and data processor if not already done
    if kafka_client is None:
        kafka_client = KafkaConsumerClient(
            bootstrap_servers=kafka_bootstrap_servers,
            topic=kafka_topic,
            group_id=kafka_group_id
        )
    
    if data_processor is None:
        data_processor = DataProcessor()
    
    # Event handler for Kafka connection button
    if kafka_connect_button:
        try:
            log_message(logger, "info", f"Attempting to connect to Kafka at {kafka_bootstrap_servers}")
            kafka_client.connect()
            with data_lock:
                st.session_state.kafka_connected = True
            log_message(logger, "info", f"Successfully connected to Kafka at {kafka_bootstrap_servers}")
        except Exception as e:
            error_container.error(f"Failed to connect to Kafka: {str(e)}")
            log_message(logger, "error", f"Failed to connect to Kafka: {str(e)}")
    
    # Always show connection status
    log_message(logger, "info", f"Kafka connection status: {st.session_state.kafka_connected}")
    
    # Main data update function
    def update_data():
        # Set a flag to indicate this thread is running
        st.session_state.update_thread_running = True
        
        while st.session_state.update_thread_running:
            try:
                # Only try to get data if connected to Kafka
                if 'kafka_connected' in st.session_state and st.session_state.kafka_connected:
                    message = kafka_client.consume(timeout=1.0)
                    
                    if message:
                        # Process Kafka message
                        pressure, temperature = data_processor.process_kafka_message(message)
                        data_source = 'kafka'
                        log_message(logger, "info", f"Received data from Kafka: Pressure={pressure}, Temperature={temperature}")
                        
                        # Create new data point
                        new_data = pd.DataFrame({
                            'timestamp': [pd.Timestamp.now()],
                            'pressure': [pressure],
                            'temperature': [temperature],
                            'source': [data_source]
                        })
                        
                        # Update session state data with thread safety
                        with data_lock:
                            st.session_state.waiting_for_data = False
                            if 'data' in st.session_state:
                                st.session_state.data = pd.concat([st.session_state.data, new_data]).reset_index(drop=True)
                                
                                # Keep only the specified number of data points
                                if 'data_points_to_keep' in st.session_state and len(st.session_state.data) > st.session_state.data_points_to_keep:
                                    st.session_state.data = st.session_state.data.iloc[-st.session_state.data_points_to_keep:]
                                
                                # Update last update time
                                st.session_state.last_update = time.time()
                    else:
                        log_message(logger, "info", "No Kafka data available, waiting for producer")
                        with data_lock:
                            st.session_state.waiting_for_data = True
                
            except Exception as e:
                log_message(logger, "error", f"Error updating data: {str(e)}")
            
            # Wait for next update (approximately 3 seconds)
            time.sleep(3)
    
    # Start data update thread if not already running
    if not st.session_state.update_thread_running:
        update_thread = threading.Thread(target=update_data, daemon=True)
        update_thread.start()
        st.session_state.update_thread = update_thread
    
    # Display current data and update UI
    def update_ui():
        try:
            # Update only if there's data and it's not empty
            with data_lock:
                waiting_for_data = st.session_state.waiting_for_data
                if 'data' in st.session_state and not st.session_state.data.empty:
                    # Make a copy to avoid thread conflicts
                    display_data = st.session_state.data.copy()
                    last_update = st.session_state.last_update
                else:
                    display_data = pd.DataFrame()
                    last_update = time.time()
            
            if not display_data.empty:
                # Get the most recent data point
                latest_data = display_data.iloc[-1]
                
                # Update metrics
                pressure_metric.metric(
                    "Current Pressure (PSI)", 
                    f"{latest_data['pressure']:.2f}"
                )
                temperature_metric.metric(
                    "Current Temperature (°C)", 
                    f"{latest_data['temperature']:.2f}"
                )
                
                # Update data source indicator
                if latest_data['source'] == 'kafka':
                    data_source_indicator.success("Data Source: Kafka (Live)")
                else:
                    data_source_indicator.warning("Data Source: Waiting for data...")
                
                # Create and display the chart
                chart = create_chart(display_data)
                chart_container.altair_chart(chart, use_container_width=True)
                
                # Update last update time
                seconds_since_update = time.time() - last_update
                update_time_container.info(f"Last updated: {seconds_since_update:.1f} seconds ago")
            else:
                # Display waiting message
                if st.session_state.kafka_connected:
                    if waiting_for_data:
                        chart_container.info("Connected to Kafka but no data available. Is the producer running?")
                    else:
                        chart_container.info("Waiting for data...")
                else:
                    chart_container.info("Not connected to Kafka. Please connect using the sidebar.")
                
                # Clear metrics when no data
                pressure_metric.empty()
                temperature_metric.empty()
                data_source_indicator.warning("No Data Available")
                
        except Exception as e:
            error_container.error(f"Error updating UI: {str(e)}")
            log_message(logger, "error", f"Error updating UI: {str(e)}")
    
    # Call update_ui once to initialize the display
    update_ui()
    
    # Set up automatic refresh every 3 seconds
    time.sleep(0.1)  # Small sleep to prevent UI freeze
    update_ui()
    time.sleep(2.9)  # Rest of the 3-second interval
    st.rerun()  # Rerun the app to refresh the UI

if __name__ == "__main__":
    main()
