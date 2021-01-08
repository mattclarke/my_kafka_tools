import argparse
import time

from confluent_kafka import Consumer as KafkaConsumer
from confluent_kafka import TopicPartition


def get_topics(broker):
    consumer = KafkaConsumer(
        {
            "bootstrap.servers": broker,
            "group.id": f"get-topic-{time.time_ns()}",
            "auto.offset.reset": "latest",
        }
    )
    metadata = consumer.list_topics()
    for n, v in metadata.topics.items():
        print(f"{n} {len(v.partitions)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    required_args = parser.add_argument_group("required arguments")
    required_args.add_argument(
        "-b", "--broker", type=str, help="the broker address", required=True
    )

    args = parser.parse_args()

    get_topics(args.broker)
