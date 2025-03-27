import time
import json
from utils import setup_logging, log_message

class DataProcessor:
    """
    Processor for handling sensor data from Kafka.
    """
    
    def __init__(self):
        """
        Initialize the data processor.
        """
        self.logger = setup_logging()
        # Expected ranges for pressure and temperature (for validation)
        self.pressure_range = (0, 100)  # PSI 
        self.temperature_range = (-50, 100)  # °C
    
    def process_kafka_message(self, message):
        """
        Process a message from Kafka containing sensor data.
        
        Args:
            message (dict): Message received from Kafka
            
        Returns:
            tuple: (pressure, temperature) values extracted from the message
            
        Raises:
            ValueError: If the message format is invalid
        """
        try:
            # Log the raw message for debugging
            log_message(self.logger, "debug", f"Processing raw message: {message}")
            
            # Handle string messages (convert to dict if needed)
            if isinstance(message, str):
                try:
                    message = json.loads(message)
                    log_message(self.logger, "info", "Converted string message to dict")
                except json.JSONDecodeError:
                    raise ValueError(f"Message is a string but not valid JSON: {message}")
            
            # Check if the message has the expected format
            if not isinstance(message, dict):
                raise ValueError(f"Message is not a dictionary: {type(message)}")
                
            # Extract pressure and temperature values
            pressure = message.get('pressure')
            temperature = message.get('temperature')
            
            # Validate the values
            if pressure is None:
                raise ValueError(f"Message missing pressure field: {message}")
            if temperature is None:
                raise ValueError(f"Message missing temperature field: {message}")
                
            # Convert to float if they're strings
            if isinstance(pressure, str):
                pressure = float(pressure)
            if isinstance(temperature, str):
                temperature = float(temperature)
                
            # Log a warning if values are outside expected ranges
            if not (self.pressure_range[0] <= pressure <= self.pressure_range[1]):
                log_message(self.logger, "warning", f"Pressure value out of expected range: {pressure}")
            if not (self.temperature_range[0] <= temperature <= self.temperature_range[1]):
                log_message(self.logger, "warning", f"Temperature value out of expected range: {temperature}")
            
            log_message(self.logger, "info", f"Successfully processed message: pressure={pressure}, temperature={temperature}")
            return pressure, temperature
            
        except Exception as e:
            log_message(self.logger, "error", f"Error processing Kafka message: {str(e)}")
            # Reraise the exception
            raise
