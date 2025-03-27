from confluent_kafka import Consumer, KafkaError

bootstrap_servers = "localhost:9092"  # Replace with your Kafka broker address
topic = "sensors"  # Replace with your Kafka topic
group_id = "test-consumer-group"

consumer_conf = {
    'bootstrap.servers': bootstrap_servers,
    'group.id': group_id,
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(consumer_conf)
consumer.subscribe([topic])

try:
    while True:
        msg = consumer.poll(1.0)  # Poll for messages with a timeout

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                print('End of partition reached {0}/{1}'.format(
                    msg.topic(), msg.partition()))
            else:
                print('Error occurred: {0}'.format(msg.error().str()))
        else:
            print('Received message: {}'.format(msg.value().decode('utf-8')))

except KeyboardInterrupt:
    consumer.close()
    print("Consumer closed.")
