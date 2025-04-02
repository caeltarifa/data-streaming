"""
Input Section UI Module.
This module contains the class responsible for rendering the data input controls.
"""

import streamlit as st


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

        # Initialize session state for tracking data collection status
        if "data_collection_active" not in st.session_state:
            st.session_state.data_collection_active = {}
            # Initialize status for each company and data point
            for company in self.companies:
                for i in range(3):
                    key = f"{company}_data_{i+1}"
                    st.session_state.data_collection_active[key] = False

    def display(self):
        """
        Display the input section with company name headers and data collection buttons.
        
        For each company, displays a title and three toggleable "Start/Stop" buttons horizontally.
        """
        st.header("DATA STREAMING")

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

                        # Display camera icon and current status
                        st.markdown("🎥")

                        # Toggle button state based on current status
                        is_active = st.session_state.data_collection_active[
                            button_key]

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
                            st.session_state.data_collection_active[
                                button_key] = not is_active

                            # Show a toast notification about the action
                            action = "Stopping" if is_active else "Starting"
                            st.toast(
                                f"{action} data collection {i+1} for {company}"
                            )

                            # In a real application, this would trigger data collection
                            # self._collect_data(company, i+1, not is_active)

                            # Force a rerun to update UI
                            st.rerun()

    def _collect_data(self, company, data_id, start=True):
        """
        Placeholder method for data collection functionality.
        
        Args:
            company (str): The company name for which to collect data.
            data_id (int): Identifier for the specific data collection process.
            start (bool): True to start data collection, False to stop.
        """
        # This would contain the actual implementation for data collection
        pass
