from confluent_kafka.admin import AdminClient, NewTopic


def create_topic(broker, topic, partitions):
    admin = AdminClient(
        {
            "bootstrap.servers": broker,
        }
    )

    new_topics = [NewTopic(topic, num_partitions=partitions, replication_factor=1)]

    fs = admin.create_topics(new_topics)

    for tp, f in fs.items():
        try:
            f.result()
            print(f"Topic {tp} created")
        except Exception as e:
            print(f"Failed to create topic {tp}: {e}")


if __name__ == "__main__":
    topics = [
        "local_jbi_heartbeat",
        "local_jbi_responses",
        "local_jbi_commands",
        "local_filewriter_status",
        "local_filewriter_pool",
        "local_jbi_visualisation",
        "local_filewriter",
        "local_forwarder_commands",
        "local_forwarder_status",
        "local_forwarder_config",
        "local_visualisation",
        "local_detector",
    ]

    for name in topics:
        print(f"creating {name}")
        create_topic("localhost:9092", name, 1)
