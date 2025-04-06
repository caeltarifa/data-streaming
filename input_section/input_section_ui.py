"""
Input Section UI Module.
This module contains the class responsible for rendering the data input controls.
"""

import streamlit as st
import requests
import json
import random
from datetime import datetime
import time


class InputSection:
    """
    Class responsible for displaying the data input controls section of the application.
    
    This section displays company names and associated data collection buttons.
    """

    def __init__(self):
        """
        Initialize the InputSection class.
        """
        # List of companies to display buttons for
        self.companies = ["Company A", "Company B"]
        
        # API endpoint for data ingestion
        self.api_endpoint = "https://data-ingestor-api-mngr.azure-api.net/ingest"
        
        # Initialize session state for tracking data collection status and API responses
        if "data_collection_active" not in st.session_state:
            st.session_state.data_collection_active = {}
            # Initialize status for each company and data point
            for company in self.companies:
                for i in range(3):
                    key = f"{company}_data_{i+1}"
                    st.session_state.data_collection_active[key] = False
                    
        # Initialize last sent time dict
        if "last_sent_time" not in st.session_state:
            st.session_state.last_sent_time = {}
            for company in self.companies:
                for i in range(3):
                    key = f"{company}_data_{i+1}"
                    st.session_state.last_sent_time[key] = 0
                    
        # Initialize API response tracking dict
        if "api_responses" not in st.session_state:
            st.session_state.api_responses = {}
            for company in self.companies:
                for i in range(3):
                    key = f"{company}_data_{i+1}"
                    st.session_state.api_responses[key] = {"status": None, "message": "Not started"}
                    
        # Initialize data send counter dict
        if "data_send_counter" not in st.session_state:
            st.session_state.data_send_counter = {}
            for company in self.companies:
                for i in range(3):
                    key = f"{company}_data_{i+1}"
                    st.session_state.data_send_counter[key] = 0

    def display(self):
        """
        Display the input section with company name headers and data collection buttons.
        
        For each company, displays a title and three toggleable "Start/Stop" buttons horizontally.
        """
        st.header("INPUTS")

        # Create the main input section container
        input_container = st.container(border=True)

        with input_container:
            # Iterate through each company and create button groups
            for company in self.companies:
                st.subheader(company)

                # Create three columns for button layout
                cols = st.columns(3)

                # Add a button in each column
                for i, col in enumerate(cols):
                    with col:
                        # Button key for this specific data stream
                        button_key = f"{company}_data_{i+1}"

                        # Display camera icon
                        st.markdown("🎥")

                        # Toggle button state based on current status
                        is_active = st.session_state.data_collection_active[button_key]
                        
                        # If active, check if it's time to send new data
                        if is_active:
                            current_time = time.time()
                            last_sent = st.session_state.last_sent_time[button_key]
                            
                            # Send data every 15 seconds if button is active
                            if current_time - last_sent > 15:
                                try:
                                    status_code = self._send_random_data_to_api(company, i+1)
                                    st.session_state.last_sent_time[button_key] = current_time
                                    
                                    # Increment the counter
                                    if button_key in st.session_state.data_send_counter:
                                        st.session_state.data_send_counter[button_key] += 1
                                    else:
                                        st.session_state.data_send_counter[button_key] = 1
                                    
                                    # Update API response status
                                    if status_code == 200:
                                        st.session_state.api_responses[button_key] = {
                                            "status": "success",
                                            "message": f"Data sent at {datetime.now().strftime('%H:%M:%S')} (sent {st.session_state.data_send_counter[button_key]} times)"
                                        }
                                        
                                        # Flag for UI update without force rerun
                                        if "needs_update" not in st.session_state:
                                            st.session_state.needs_update = True
                                    else:
                                        st.session_state.api_responses[button_key] = {
                                            "status": "error",
                                            "message": f"API Error: {status_code}"
                                        }
                                    
                                except Exception as e:
                                    st.session_state.api_responses[button_key] = {
                                        "status": "error",
                                        "message": f"Error: {str(e)[:50]}"
                                    }

                        # Display Start/Stop button with appropriate color
                        if is_active:
                            button_label = "Stop"
                            button_type = "primary"
                        else:
                            button_label = "Start"
                            button_type = "secondary"

                        if st.button(button_label,
                                     key=button_key,
                                     type=button_type):
                            # Toggle the status when clicked
                            new_status = not is_active
                            st.session_state.data_collection_active[button_key] = new_status

                            if new_status:
                                # If starting, send data immediately
                                try:
                                    status_code = self._send_random_data_to_api(company, i+1)
                                    st.session_state.last_sent_time[button_key] = time.time()
                                    
                                    # Increment the counter on first send
                                    if button_key in st.session_state.data_send_counter:
                                        st.session_state.data_send_counter[button_key] += 1
                                    else:
                                        st.session_state.data_send_counter[button_key] = 1
                                        
                                    if status_code == 200:
                                        st.toast(f"Started data collection for {company}, device {i+1}", icon="✅")
                                        st.session_state.api_responses[button_key] = {
                                            "status": "success",
                                            "message": f"Data sent at {datetime.now().strftime('%H:%M:%S')} (sent {st.session_state.data_send_counter[button_key]} times)"
                                        }
                                        
                                        # Mark that the UI needs to update - let the Streamlit refresh cycle handle it
                                        if "needs_update" not in st.session_state:
                                            st.session_state.needs_update = True
                                    else:
                                        st.toast(f"Error sending data: API returned {status_code}", icon="⚠️")
                                        st.session_state.api_responses[button_key] = {
                                            "status": "error",
                                            "message": f"API Error: {status_code}"
                                        }
                                        
                                except Exception as e:
                                    st.toast(f"Error sending data: {str(e)[:50]}", icon="❌")
                                    st.session_state.api_responses[button_key] = {
                                        "status": "error",
                                        "message": f"Error: {str(e)[:50]}"
                                    }
                            else:
                                st.toast(f"Stopped data collection for {company}, device {i+1}")
                                st.session_state.api_responses[button_key] = {
                                    "status": "stopped", 
                                    "message": "Data collection stopped"
                                }

                            # Force a rerun to update UI
                            st.rerun()
                        
                        # Display current status indicator
                        status = st.session_state.api_responses[button_key]["status"]
                        message = st.session_state.api_responses[button_key]["message"]
                        
                        if status == "success":
                            st.success(message)
                        elif status == "error":
                            st.error(message)
                        elif status == "stopped":
                            st.info(message)
                        else:
                            st.info("Ready")
    
    def _send_random_data_to_api(self, company, data_id):
        """
        Send random data to the API endpoint.
        
        Args:
            company (str): The company name.
            data_id (int): Camera device identifier.
            
        Returns:
            int: HTTP status code from the API response
        """
        # Generate random data according to the required structure
        person_count = random.randint(1, 10)
        
        # Generate people data with age and gender
        people = []
        for _ in range(person_count):
            # Randomly select gender
            gender = random.choice(["male", "female", "unknown"])
            # Generate random age
            age = random.randint(18, 70)
            # Add person to list
            people.append({
                "age": age,
                "gender": gender
            })
        
        # Create the payload
        payload = {
            "people": people,
            "company_name": company,
            "device_id": f"CAM{company[-1]}{data_id:03d}",  # Format: CAMA001, CAMB002, etc.
            "person_count": person_count,
            "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        }
        
        # Set request headers
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        
        # Send POST request to the API
        response = requests.post(
            self.api_endpoint,
            headers=headers,
            data=json.dumps(payload),
            timeout=10
        )
        
        # Log the response and payload
        print(f"API call to {self.api_endpoint}")
        print(f"Payload: {json.dumps(payload)}")
        print(f"Response: {response.status_code} - {response.text}")
        
        # Store the data in analytics section if available
        if "analytics_section" in st.session_state:
            st.session_state.analytics_section.add_sent_data_to_log(
                json.dumps(payload), 
                response.status_code
            )
            
        return response.status_code
