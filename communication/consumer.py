from kafka import KafkaConsumer


def start_listenting():
    return KafkaConsumer('health-in', bootstrap_servers=['localhost:9092'])