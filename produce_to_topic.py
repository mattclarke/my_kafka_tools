import argparse
import time

from confluent_kafka import Producer as KafkaProducer
from confluent_kafka import TopicPartition


def generate_config(user, password, brokers):
    return {
        "security.protocol": "SASL_SSL",
        "sasl.mechanism": "SCRAM-SHA-256",
        "ssl.ca.location": "ecdc-kafka-ca-real.crt",
        "sasl.username": user,
        "sasl.password": password,
        "bootstrap.servers": ",".join(brokers),
        "message.max.bytes": 1_000_000_000,
    }


def produce_msg(config, topic, message):
    producer = KafkaProducer(**config)
    producer.produce(topic, message)
    producer.flush(10000)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    required_args = parser.add_argument_group("required arguments")
    required_args.add_argument(
        "-b",
        "--brokers",
        type=str,
        nargs="+",
        help="the broker addresses",
        required=True,
    )

    required_args.add_argument(
        "-t", "--topic", type=str, help="the topic to consume", required=True
    )

    required_args.add_argument(
        "-m", "--message", type=str, help="the message to send", required=True
    )

    required_args.add_argument(
        "-u", "--user", type=str, help="the user name", required=True
    )

    required_args.add_argument(
        "-p", "--password", type=str, help="the password", required=True
    )

    args = parser.parse_args()

    kafka_config = generate_config(args.user, args.password, args.brokers)

    produce_msg(kafka_config, args.topic, args.message)
