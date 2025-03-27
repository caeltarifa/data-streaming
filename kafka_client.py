import json
import socket
from utils import setup_logging, log_message
from kafka_simulator import SimulatedConsumer

class KafkaConsumerClient:
    """
    Client for consuming data from simulated Kafka topics.
    """

    def __init__(self, bootstrap_servers, topic, group_id):
        """
        Initialize Kafka consumer client.

        Args:
            bootstrap_servers (str): Not used in simulation, kept for API compatibility
            topic (str): Kafka topic to consume from
            group_id (str): Consumer group ID
        """
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.group_id = group_id
        self.consumer = None
        self.logger = setup_logging()
        self.socket = None

    def connect(self):
        """
        Establish connection to simulated Kafka.

        Raises:
            Exception: If initialization fails
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect(('0.0.0.0', 9292))
            log_message(self.logger, "info", f"Connected to simulated Kafka topic: {self.topic}")
        except Exception as e:
            log_message(self.logger, "error", f"Failed to initialize consumer: {str(e)}")
            raise

    def consume(self, timeout=1.0):
        """
        Consume a single message from the simulated Kafka topic.

        Args:
            timeout (float): Maximum time to wait for a message in seconds

        Returns:
            dict: Message value or None if no message is available
        """
        if not self.socket:
            log_message(self.logger, "error", "Consumer not initialized")
            return None

        try:
            log_message(self.logger, "debug", f"Attempting to consume message from {self.topic}")

            # Get a message from the simulated consumer
            data = self.socket.recv(1024)
            message = None
            if data:
                message = json.loads(data.decode())
                log_message(self.logger, "info", f"Consumed message from {self.topic}: {message}")
            return message

        except Exception as e:
            log_message(self.logger, "error", f"Error consuming from topic: {str(e)}")
            return None

    def close(self):
        """
        Close the consumer connection (no-op for simulation).
        """
        if self.socket:
            self.socket.close()
        log_message(self.logger, "info", "Consumer closed")