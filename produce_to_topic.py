import argparse
import time

from confluent_kafka import Producer as KafkaProducer
from confluent_kafka import TopicPartition


def produce_msg(broker, topic, message):
    producer = KafkaProducer(
        {
            "bootstrap.servers": broker,
        }
    )

    producer.produce(topic, message)
    producer.flush(10000)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    required_args = parser.add_argument_group("required arguments")
    required_args.add_argument(
        "-b", "--broker", type=str, help="the broker address", required=True
    )

    required_args.add_argument(
        "-t", "--topic", type=str, help="the topic to consume", required=True
    )

    required_args.add_argument(
        "-m", "--message", type=str, help="the message to send", required=True
    )

    args = parser.parse_args()

    produce_msg(args.broker, args.topic, args.message)
