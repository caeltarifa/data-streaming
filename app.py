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

    # Create and display each section
    input_section = InputSection()
    input_section.display()

    # Add a separator between sections
    st.markdown("---")

    analytics_section = AnalyticsSection()
    analytics_section.display()

    # Add a separator between sections
    st.markdown("---")

    chat_interface = ChatInterface()
    chat_interface.display()


if __name__ == "__main__":
    main()
