import os
from google.cloud import pubsub_v1

# Get project ID from environment variable
project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
if not project_id:
    raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, "veritas-reputation-updates")
publisher.create_topic(request={"name": topic_path})
print("✅ Pub/Sub topic criado:", topic_path)
