from google.cloud import pubsub_v1
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path("umbrella-producao", "veritas-reputation-updates")
publisher.create_topic(request={"name": topic_path})
print("✅ Pub/Sub topic criado:", topic_path)
