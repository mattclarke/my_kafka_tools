import argparse
import time

from confluent_kafka.admin import AdminClient, NewTopic


def create_topic(broker, topic, partitions):
    admin = AdminClient({"bootstrap.servers": broker,})

    new_topics = [NewTopic(topic, num_partitions=partitions, replication_factor=1)]

    fs = admin.create_topics(new_topics)

    for tp, f in fs.items():
        try:
            f.result()
            print(f"Topic {tp} created")
        except Exception as e:
            print(f"Failed to create topic {tp}: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    required_args = parser.add_argument_group("required arguments")
    required_args.add_argument(
        "-b", "--broker", type=str, help="the broker address", required=True
    )

    required_args.add_argument(
        "-t", "--topic", type=str, help="the topic to create", required=True
    )

    parser.add_argument(
        "-p",
        "--num_partitions",
        type=int,
        default=1,
        help="the number of partitions to create",
    )

    args = parser.parse_args()

    create_topic(args.broker, args.topic, args.num_partitions)
