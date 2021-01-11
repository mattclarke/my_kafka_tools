import argparse
import time

from confluent_kafka import Consumer as KafkaConsumer
from confluent_kafka import TopicPartition


def consume_topic(broker, topic, start_from_oldest=False, truncate=False):
    consumer = KafkaConsumer(
        {
            "bootstrap.servers": broker,
            "group.id": f"get-topic-{time.time_ns()}",
            "auto.offset.reset": "earliest" if start_from_oldest else "latest",
        }
    )

    metadata = consumer.list_topics(topic)
    if topic not in metadata.topics:
        raise Exception("Topic does not exist")

    topic_partitions = [
        TopicPartition(topic, p) for p in metadata.topics[topic].partitions
    ]

    consumer.assign(topic_partitions)

    while True:
        msg = consumer.poll(0.0)

        if msg:
            value = msg.value()[0:100] if truncate else msg.value()
            print(f"Timestamp: {msg.timestamp()[1]}\n{value}")

        time.sleep(0.1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    required_args = parser.add_argument_group("required arguments")
    required_args.add_argument(
        "-b", "--broker", type=str, help="the broker address", required=True
    )

    required_args.add_argument(
        "-t", "--topic", type=str, help="the topic to consume", required=True
    )

    parser.add_argument(
        "-so",
        "--start-from-oldest",
        action="store_true",
        help="whether to start consuming from oldest message",
    )

    parser.add_argument(
        "-tr",
        "--truncate",
        action="store_true",
        help="whether to truncate the contents of the message",
    )

    args = parser.parse_args()

    consume_topic(args.broker, args.topic, args.start_from_oldest, args.truncate)
