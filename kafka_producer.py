#!/usr/bin/env python3
import json
import time
import random
from utils import setup_logging, log_message
from kafka_simulator import SimulatedProducer

# Setup logging
logger = setup_logging()

class SensorDataProducer:
    """
    Producer to generate random sensor data and send it to the simulated Kafka topic.
    """
    
    def __init__(self, topic):
        """
        Initialize the Kafka producer.
        
        Args:
            topic (str): Kafka topic to produce to
        """
        self.topic = topic
        self.producer = None
        
        # Define normal ranges for pressure and temperature
        self.pressure_range = (14.0, 15.0)  # PSI (standard atmospheric pressure range)
        self.temperature_range = (20.0, 25.0)  # °C (room temperature range)
        
        # Keep track of last values for smooth transitions
        self.last_pressure = (self.pressure_range[0] + self.pressure_range[1]) / 2
        self.last_temperature = (self.temperature_range[0] + self.temperature_range[1]) / 2
    
    def connect(self):
        """
        Create the producer instance.
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
self.socket.connect(('0.0.0.0', 9292))
            log_message(logger, "info", f"Producer initialized for topic: {self.topic}")
        except Exception as e:
            log_message(logger, "error", f"Failed to initialize producer: {str(e)}")
            raise
    
    def generate_sensor_data(self):
        """
        Generate random sensor data with smooth transitions.
        
        Returns:
            dict: Dictionary containing pressure and temperature values
        """
        # Generate pressure value with small changes from last value
        max_pressure_change = 0.1  # Maximum change per update
        pressure_delta = random.uniform(-max_pressure_change, max_pressure_change)
        new_pressure = self.last_pressure + pressure_delta
        
        # Keep pressure within reasonable range
        new_pressure = max(self.pressure_range[0], min(self.pressure_range[1], new_pressure))
        
        # Generate temperature value with small changes from last value
        max_temp_change = 0.2  # Maximum change per update
        temp_delta = random.uniform(-max_temp_change, max_temp_change)
        new_temperature = self.last_temperature + temp_delta
        
        # Keep temperature within reasonable range
        new_temperature = max(self.temperature_range[0], min(self.temperature_range[1], new_temperature))
        
        # Update last values
        self.last_pressure = new_pressure
        self.last_temperature = new_temperature
        
        return {
            'timestamp': time.time(),
            'pressure': new_pressure,
            'temperature': new_temperature
        }
    
    def produce_data(self, interval=3.0):
        """
        Continuously produce sensor data at the specified interval.
        
        Args:
            interval (float): Time between messages in seconds
        """
        if not self.producer:
            log_message(logger, "error", "Producer not initialized. Call connect() first.")
            return
        
        try:
            log_message(logger, "info", f"Starting to produce data to topic {self.topic} every {interval} seconds")
            
            while True:
                # Generate sensor data
                data = self.generate_sensor_data()
                
                # Send data to topic
                try:
                    self.socket.send(json.dumps(data).encode())
                    log_message(logger, "info", f"Produced data: {json.dumps(data)}")
                except Exception as e:
                    log_message(logger, "error", f"Failed to produce data: {str(e)}")
                
                # Wait for next interval
                time.sleep(interval)
                
        except KeyboardInterrupt:
            log_message(logger, "info", "Producer stopped by user")
        except Exception as e:
            log_message(logger, "error", f"Error producing data: {str(e)}")
        finally:
            log_message(logger, "info", "Producer closed")

def main():
    """
    Main function to run the producer.
    """
    # Configuration
    topic = "sensors"  # Topic name
    interval = 3.0  # 3 seconds between messages
    
    # Create and run producer
    producer = SensorDataProducer(topic)
    producer.connect()
    producer.produce_data(interval)

if __name__ == "__main__":
    main()