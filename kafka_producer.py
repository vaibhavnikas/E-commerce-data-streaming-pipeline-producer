import json
from kafka import KafkaProducer


def create_kafka_producer(bootstrap_servers:list):
    """Creates a Kafka producer instance"""
    try:
        producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer = lambda v: json.dumps(v).encode('utf-8')
        )
        return producer 
    except Exception as e:
        print(f"Error creating Kafka producer: {e}")
        return None

def send_message(producer, topic, message):
    """Sends a message to a Kafka topic"""
    if producer:
        try:
            producer.send(topic, message)
            producer.flush()
            print(f"Message sent to {topic}: {message}")
        except Exception as e:
            print(f"Error sending message: {e}")
    else:
        print("Producer not initialized")

def close_producer(producer):
    """Closes the Kafka producer"""
    if producer:
        producer.close()
        print("Producer closed")
