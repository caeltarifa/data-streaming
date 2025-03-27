#!/usr/bin/env python3
import json
import time
import random
import os
import threading
from pathlib import Path
from utils import setup_logging, log_message

# Setup logging
logger = setup_logging()

# Constants
DATA_DIR = Path("./data")
TOPICS_DIR = DATA_DIR / "topics"
LOCK_FILE = DATA_DIR / "locks"

class KafkaSimulator:
    """
    A file-based Kafka simulator for development and testing.
    Uses files to simulate Kafka topics and messages.
    """
    
    @staticmethod
    def initialize():
        """
        Initialize the simulator by creating necessary directories.
        """
        # Create data directory if it doesn't exist
        if not DATA_DIR.exists():
            DATA_DIR.mkdir()
            log_message(logger, "info", f"Created data directory: {DATA_DIR}")
            
        # Create topics directory if it doesn't exist
        if not TOPICS_DIR.exists():
            TOPICS_DIR.mkdir()
            log_message(logger, "info", f"Created topics directory: {TOPICS_DIR}")
            
        # Create locks directory if it doesn't exist
        if not LOCK_FILE.parent.exists():
            LOCK_FILE.parent.mkdir(exist_ok=True)
            
        log_message(logger, "info", "Kafka simulator initialized")

class SimulatedProducer:
    """
    A simulated Kafka producer that writes messages to files.
    """
    
    def __init__(self, topic):
        """
        Initialize the producer for a specific topic.
        
        Args:
            topic (str): Topic name
        """
        self.topic = topic
        self.topic_dir = TOPICS_DIR / topic
        self.lock = threading.Lock()
        
        # Create topic directory if it doesn't exist
        if not self.topic_dir.exists():
            self.topic_dir.mkdir(parents=True)
            log_message(logger, "info", f"Created topic directory: {self.topic_dir}")
    
    def produce(self, message):
        """
        Produce a message to the topic.
        
        Args:
            message (dict): Message to produce
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Ensure message has a timestamp
            if 'timestamp' not in message:
                message['timestamp'] = time.time()
                
            # Create a unique filename based on timestamp
            filename = f"{message['timestamp']:.6f}.json"
            filepath = self.topic_dir / filename
            
            # Write message to file with locking to prevent race conditions
            with self.lock:
                with open(filepath, 'w') as f:
                    json.dump(message, f)
                    
            log_message(logger, "info", f"Produced message to {self.topic}: {json.dumps(message)}")
            return True
            
        except Exception as e:
            log_message(logger, "error", f"Error producing message: {str(e)}")
            return False

class SimulatedConsumer:
    """
    A simulated Kafka consumer that reads messages from files.
    """
    
    def __init__(self, topic, group_id):
        """
        Initialize the consumer for a specific topic.
        
        Args:
            topic (str): Topic name
            group_id (str): Consumer group ID
        """
        self.topic = topic
        self.group_id = group_id
        self.topic_dir = TOPICS_DIR / topic
        self.offset_file = DATA_DIR / f"offsets-{group_id}-{topic}.txt"
        self.lock = threading.Lock()
        self.last_consumed = 0
        
        # Create topic directory if it doesn't exist
        if not self.topic_dir.exists():
            self.topic_dir.mkdir(parents=True)
            log_message(logger, "info", f"Created topic directory: {self.topic_dir}")
            
        # Load last consumed offset if it exists
        if self.offset_file.exists():
            try:
                with open(self.offset_file, 'r') as f:
                    self.last_consumed = float(f.read().strip())
                log_message(logger, "info", f"Loaded offset for {topic}: {self.last_consumed}")
            except Exception as e:
                log_message(logger, "error", f"Error loading offset: {str(e)}")
    
    def _update_offset(self, offset):
        """
        Update the offset file with the latest consumed message timestamp.
        
        Args:
            offset (float): Timestamp of the latest consumed message
        """
        try:
            with open(self.offset_file, 'w') as f:
                f.write(str(offset))
            self.last_consumed = offset
        except Exception as e:
            log_message(logger, "error", f"Error updating offset: {str(e)}")
    
    def consume(self, timeout=1.0):
        """
        Consume a single message from the topic.
        
        Args:
            timeout (float): Maximum time to wait for a message in seconds
            
        Returns:
            dict: Message value or None if no message is available
        """
        try:
            # Check if topic directory exists
            if not self.topic_dir.exists():
                return None
                
            # Get all message files
            files = list(self.topic_dir.glob("*.json"))
            
            # Sort by timestamp (filename)
            files.sort()
            
            # Find the first file with timestamp greater than last consumed
            newest_message = None
            newest_timestamp = self.last_consumed
            
            for file in files:
                # Extract timestamp from filename
                try:
                    timestamp = float(file.stem)
                    
                    # Skip if already consumed based on consumer group's offset
                    if timestamp <= self.last_consumed:
                        continue
                        
                    # Read the message
                    with open(file, 'r') as f:
                        message = json.load(f)
                        
                    # Keep track of newest message
                    if newest_message is None or timestamp > newest_timestamp:
                        newest_message = message
                        newest_timestamp = timestamp
                    
                except Exception as e:
                    log_message(logger, "error", f"Error reading message file {file}: {str(e)}")
                    continue
            
            # Update offset if a message was found
            if newest_message is not None:
                with self.lock:
                    self._update_offset(newest_timestamp)
                log_message(logger, "info", f"Consumed message from {self.topic}: {json.dumps(newest_message)}")
                return newest_message
                
            return None
            
        except Exception as e:
            log_message(logger, "error", f"Error consuming message: {str(e)}")
            return None

# Initialize the simulator when the module is imported
KafkaSimulator.initialize()