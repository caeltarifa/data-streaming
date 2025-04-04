"""
Main application file for Streamlit web app.
This script initializes and orchestrates the three main sections of the application.
"""

import streamlit as st
import time
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
    
    # Initialize the auto-refresh interval in session state if not already present
    if "last_refresh_time" not in st.session_state:
        st.session_state.last_refresh_time = time.time()
    
    # Add container with API endpoint information
    with st.sidebar:
        st.header("API Information")
        st.info("📤 Sending data to API endpoint:\n\n"
                "`https://camera-data-ingestor.nicedesert-291b7b89.eastus.azurecontainerapps.io/ingest`\n\n"
                "Click the Start buttons to begin sending random data every 15 seconds.")
        
        # Add auto-refresh toggle
        with st.expander("Advanced Settings"):
            # If auto-refresh is not in session state, initialize it
            if "auto_refresh" not in st.session_state:
                st.session_state.auto_refresh = True
                
            # Create a toggle for auto-refresh
            st.session_state.auto_refresh = st.toggle(
                "Auto-refresh charts", 
                value=st.session_state.auto_refresh,
                help="When enabled, charts will automatically refresh when new data is received"
            )

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
    
    # Auto-refresh mechanism that doesn't interfere with button clicks
    current_time = time.time()
    
    # Check if it's time to refresh (5 second interval)
    if st.session_state.auto_refresh and (current_time - st.session_state.last_refresh_time > 5):
        # Update refresh time
        st.session_state.last_refresh_time = current_time
        
        # If there's new data that needs to be reflected in charts, rerun the app
        if "needs_update" in st.session_state and st.session_state.needs_update:
            st.session_state.needs_update = False
            # Use JavaScript to refresh the page instead of st.rerun()
            st.markdown(
                """
                <script>
                    setTimeout(function() {
                        window.location.reload();
                    }, 100);
                </script>
                """,
                unsafe_allow_html=True
            )


if __name__ == "__main__":
    main()
