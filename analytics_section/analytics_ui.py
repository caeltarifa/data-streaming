"""
Analytics Section UI Module.
This module contains the class responsible for rendering the real-time analytics visualization.
"""

import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
import json
import time
from datetime import datetime

class AnalyticsSection:
    """
    Class responsible for displaying the real-time analytics section of the application.
    
    This section visualizes data using Altair charts.
    """
    
    def __init__(self):
        """
        Initialize the AnalyticsSection class.
        """
        # Initialize session state for storing sent data if it doesn't exist
        if "sent_data_log" not in st.session_state:
            st.session_state.sent_data_log = []
        
        # Initialize session state for tracking when data was last updated
        if "last_data_update" not in st.session_state:
            st.session_state.last_data_update = time.time()
    
    def display(self):
        """
        Display the analytics section with visualizations.
        
        Creates and displays sample Altair charts with example data.
        """
        st.header("REAL-TIME ANALYTICS")
        
        # Create a container with a border for the analytics section
        analytics_container = st.container(border=True)
        
        with analytics_container:
            # Create tabs for different chart types and data views
            tab1, tab2, tab3 = st.tabs(["Age Distribution", "Person Count", "API Data Log"])
            
            with tab1:
                st.subheader("Age Distribution")
                age_chart = self._create_age_distribution_chart()
                if age_chart:
                    st.altair_chart(age_chart, use_container_width=True)
                else:
                    st.info("No data available yet. Start data collection to see analytics.")
            
            with tab2:
                st.subheader("Person Count by Device")
                count_chart = self._create_person_count_chart()
                if count_chart:
                    st.altair_chart(count_chart, use_container_width=True)
                else:
                    st.info("No data available yet. Start data collection to see analytics.")
            
            with tab3:
                st.subheader("Recent API Data")
                self._display_data_log()
    
    def _create_age_distribution_chart(self):
        """
        Create a histogram chart showing age distribution from collected data.
        
        Returns:
            alt.Chart: An Altair chart visualization or None if no data.
        """
        # If no data has been sent yet, return None
        if not st.session_state.sent_data_log:
            return None
        
        # Extract all ages from the logs
        all_ages = []
        for entry in st.session_state.sent_data_log[-30:]:  # Use last 30 entries
            try:
                payload = json.loads(entry.get("payload", "{}"))
                all_ages.extend(payload.get("ages", []))
            except (json.JSONDecodeError, AttributeError):
                continue
        
        if not all_ages:
            return None
        
        # Create a dataframe with all ages
        data = pd.DataFrame({"age": all_ages})
        
        # Create an age distribution histogram
        chart = alt.Chart(data).mark_bar().encode(
            alt.X("age:Q", bin=True, title="Age"),
            alt.Y("count()", title="Count"),
            tooltip=["count()", alt.Tooltip("age:Q", bin=True)]
        ).properties(
            title="Age Distribution of Detected Persons"
        ).interactive()
        
        return chart
    
    def _create_person_count_chart(self):
        """
        Create a bar chart showing person count by device.
        
        Returns:
            alt.Chart: An Altair chart visualization or None if no data.
        """
        # If no data has been sent yet, return None
        if not st.session_state.sent_data_log:
            return None
        
        # Extract person count data from logs
        device_data = []
        for entry in st.session_state.sent_data_log[-50:]:  # Use last 50 entries
            try:
                payload = json.loads(entry.get("payload", "{}"))
                device_data.append({
                    "device_id": payload.get("device_id", "Unknown"),
                    "company": payload.get("company_name", "Unknown"),
                    "person_count": payload.get("person_count", 0),
                    "timestamp": entry.get("timestamp", "")
                })
            except (json.JSONDecodeError, AttributeError):
                continue
        
        if not device_data:
            return None
        
        # Create a dataframe with the device data
        data = pd.DataFrame(device_data)
        
        # Calculate average person count per device
        avg_counts = data.groupby(["device_id", "company"])["person_count"].mean().reset_index()
        
        # Create a chart to show average person count by device
        chart = alt.Chart(avg_counts).mark_bar().encode(
            x=alt.X("device_id:N", title="Device ID", sort="-y"),
            y=alt.Y("person_count:Q", title="Average Person Count"),
            color=alt.Color("company:N", title="Company"),
            tooltip=["device_id", "company", "person_count"]
        ).properties(
            title="Average Person Count by Device"
        ).interactive()
        
        return chart
    
    def _display_data_log(self):
        """
        Display a table of the most recent data sent to the API.
        """
        if not st.session_state.sent_data_log:
            st.info("No data has been sent to the API yet.")
            return
        
        # Display the most recent entries in the log
        st.write("Most recent API requests:")
        
        # Create a formatted table of the last 10 entries
        log_data = []
        for entry in st.session_state.sent_data_log[-10:]:
            try:
                payload = json.loads(entry.get("payload", "{}"))
                log_data.append({
                    "Timestamp": entry.get("timestamp", ""),
                    "Company": payload.get("company_name", ""),
                    "Device": payload.get("device_id", ""),
                    "People": payload.get("person_count", 0),
                    "Ages": str(payload.get("ages", []))
                })
            except (json.JSONDecodeError, AttributeError):
                continue
        
        # Convert to DataFrame and display
        if log_data:
            log_df = pd.DataFrame(log_data)
            st.dataframe(log_df, use_container_width=True)
        else:
            st.info("Could not parse recent API request data.")
        
        # Add a button to clear the log
        if st.button("Clear Data Log"):
            st.session_state.sent_data_log = []
            st.rerun()
    
    def add_sent_data_to_log(self, payload_str, status_code):
        """
        Add sent data to the log for visualization.
        
        Args:
            payload_str (str): JSON string of the payload sent to the API.
            status_code (int): HTTP status code from the API response.
        """
        # Add new entry to the log
        entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "payload": payload_str,
            "status_code": status_code
        }
        
        # Add to the beginning of the list
        st.session_state.sent_data_log.append(entry)
        
        # Keep only the last 100 entries to avoid using too much memory
        if len(st.session_state.sent_data_log) > 100:
            st.session_state.sent_data_log = st.session_state.sent_data_log[-100:]
        
        # Update the last update time
        st.session_state.last_data_update = time.time()
