"""
Main application file for Streamlit web app.
This script initializes and orchestrates the three main sections of the application.
"""

import streamlit as st
from input_section.input_section_ui import InputSection
from analytics_section.analytics_ui import AnalyticsSection
from chat_interface.chat_ui import ChatInterface


def main():
    """
    Main function to run the Streamlit application.
    Instantiates and displays each section of the application.
    """
    # Set page config
    st.set_page_config(page_title="Computer-Vision-Based Analytics",
                       page_icon="📊",
                       layout="wide")

    # Display application title
    st.title("Computer-Vision-Based Analytics")
    
    # Add container with API endpoint information
    with st.sidebar:
        st.header("API Information")
        st.info("📤 Sending data to API endpoint:\n\n"
                "`https://camera-data-ingestor.nicedesert-291b7b89.eastus.azurecontainerapps.io/ingest`\n\n"
                "Click the Start buttons to begin sending random data every 15 seconds.")

    # Create analytics section first and store in session state so other sections can access it
    analytics_section = AnalyticsSection()
    st.session_state.analytics_section = analytics_section
    
    # Create and display each section
    input_section = InputSection()
    input_section.display()

    # Add a separator between sections
    st.markdown("---")

    # Display the analytics section
    analytics_section.display()

    # Add a separator between sections
    st.markdown("---")

    chat_interface = ChatInterface()
    chat_interface.display()


if __name__ == "__main__":
    main()
