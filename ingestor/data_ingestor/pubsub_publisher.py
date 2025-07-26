import os
import json
from google.cloud import pubsub_v1

# Set your GCP project ID and topic ID
PROJECT_ID = os.getenv("GCP_PROJECT_ID", "your-gcp-project-id")
TOPIC_ID = os.getenv("PUBSUB_TOPIC_ID", "city-events")

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)

def publish_event(event):
    # event: dict
    data = json.dumps(event).encode("utf-8")
    future = publisher.publish(topic_path, data=data)
    return future.result() 