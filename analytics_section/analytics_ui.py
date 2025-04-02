"""
Analytics Section UI Module.
This module contains the class responsible for rendering the real-time analytics visualization.
"""

import streamlit as st
import altair as alt
import pandas as pd
import numpy as np

class AnalyticsSection:
    """
    Class responsible for displaying the real-time analytics section of the application.
    
    This section visualizes data using Altair charts.
    """
    
    def __init__(self):
        """
        Initialize the AnalyticsSection class.
        """
        # This would typically load or initialize data sources in a real application
        pass
    
    def display(self):
        """
        Display the analytics section with visualizations.
        
        Creates and displays sample Altair charts with example data.
        """
        st.header("REAL-TIME ANALYTICS")
        
        # Create a container with a yellow border for the analytics section
        analytics_container = st.container(border=True)
        
        with analytics_container:
            # Create tabs for different chart types
            tab1, tab2 = st.tabs(["Line Chart", "Bar Chart"])
            
            with tab1:
                st.subheader("Time Series Data")
                st.altair_chart(self._create_line_chart(), use_container_width=True)
            
            with tab2:
                st.subheader("Categorical Data")
                st.altair_chart(self._create_bar_chart(), use_container_width=True)
    
    def _create_line_chart(self):
        """
        Create a sample line chart using Altair.
        
        Returns:
            alt.Chart: An Altair line chart visualization.
        """
        # Generate sample data for the line chart
        # In a real application, this would use actual data from a database or API
        dates = pd.date_range(start='2023-01-01', periods=30, freq='D')
        data = pd.DataFrame({
            'date': dates,
            'value': np.sin(np.arange(30) / 3) * 10 + 20 + np.random.randn(30) * 2
        })
        
        # Create and return the chart
        chart = alt.Chart(data).mark_line().encode(
            x=alt.X('date:T', title='Date'),
            y=alt.Y('value:Q', title='Value', scale=alt.Scale(domain=[0, 40])),
            tooltip=['date', 'value']
        ).interactive()
        
        return chart
    
    def _create_bar_chart(self):
        """
        Create a sample bar chart using Altair.
        
        Returns:
            alt.Chart: An Altair bar chart visualization.
        """
        # Generate sample data for the bar chart
        # In a real application, this would use actual data from a database or API
        categories = ['Category A', 'Category B', 'Category C', 'Category D', 'Category E']
        values = [25, 40, 15, 35, 20]
        
        data = pd.DataFrame({
            'category': categories,
            'value': values
        })
        
        # Create and return the chart
        chart = alt.Chart(data).mark_bar().encode(
            x=alt.X('category:N', title='Category', sort='-y'),
            y=alt.Y('value:Q', title='Value'),
            color=alt.Color('category:N', legend=None),
            tooltip=['category', 'value']
        ).interactive()
        
        return chart
