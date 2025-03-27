import altair as alt
import pandas as pd
from utils import setup_logging, log_message

# Setup logger
logger = setup_logging()

def create_chart(data):
    """
    Create an Altair chart for visualizing pressure and temperature data.
    
    Args:
        data (pd.DataFrame): DataFrame containing timestamp, pressure, temperature, 
                             and source columns
                             
    Returns:
        alt.Chart: Altair chart object
    """
    try:
        if data.empty:
            log_message(logger, "warning", "Attempted to create chart with empty data")
            # Return empty chart
            return alt.Chart(pd.DataFrame({'x': [0], 'y': [0]})).mark_point()
        
        # Ensure data has required columns
        required_columns = ['timestamp', 'pressure', 'temperature', 'source']
        for col in required_columns:
            if col not in data.columns:
                log_message(logger, "error", f"Data missing required column: {col}")
                return alt.Chart(pd.DataFrame({'x': [0], 'y': [0]})).mark_point()
        
        # Create a copy of the data to avoid modifying the original
        chart_data = data.copy()
        
        # Convert timestamp to string format for better display
        chart_data['formatted_time'] = chart_data['timestamp'].dt.strftime('%H:%M:%S')
        
        # Create color scale for data source
        color_scale = alt.Scale(
            domain=['kafka', 'random'],
            range=['#1E88E5', '#FFA726']  # Blue for Kafka, Orange for random
        )
        
        # Create the base chart
        base = alt.Chart(chart_data).encode(
            x=alt.X('formatted_time:N', title='Time', sort=None),
            color=alt.Color('source:N', scale=color_scale, title='Data Source')
        )
        
        # Create pressure line chart
        pressure_scale = alt.Scale(
            domain=[
                chart_data['pressure'].min() * 0.95,
                chart_data['pressure'].max() * 1.05
            ]
        )
        
        pressure_line = base.mark_line(point=True).encode(
            y=alt.Y('pressure:Q', scale=pressure_scale, title='Pressure (PSI)'),
            tooltip=['formatted_time', 'pressure', 'temperature', 'source']
        )
        
        # Create temperature line chart
        temperature_scale = alt.Scale(
            domain=[
                chart_data['temperature'].min() * 0.95,
                chart_data['temperature'].max() * 1.05
            ]
        )
        
        temperature_line = base.mark_line(point=True, stroke='#FF4081').encode(
            y=alt.Y('temperature:Q', scale=temperature_scale, title='Temperature (°C)'),
            tooltip=['formatted_time', 'pressure', 'temperature', 'source']
        )
        
        # Create selection for interactive zooming
        selection = alt.selection_interval(bind='scales')
        
        # Combine charts
        pressure_chart = pressure_line.properties(
            title='Pressure Over Time',
            width='container',
            height=300
        ).add_selection(selection)
        
        temperature_chart = temperature_line.properties(
            title='Temperature Over Time',
            width='container',
            height=300
        ).add_selection(selection)
        
        # Combine charts vertically
        combined_chart = alt.vconcat(
            pressure_chart,
            temperature_chart
        ).resolve_scale(
            color='independent'
        )
        
        return combined_chart
        
    except Exception as e:
        log_message(logger, "error", f"Error creating chart: {str(e)}")
        # Return empty chart in case of error
        return alt.Chart(pd.DataFrame({'x': [0], 'y': [0]})).mark_point()
