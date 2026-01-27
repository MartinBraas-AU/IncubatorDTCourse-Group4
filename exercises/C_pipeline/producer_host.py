import json
import time
import random
from datetime import datetime, timezone
import pika

conn = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
ch = conn.channel()
ch.queue_declare(queue="sensor_queue", durable=True)

for i in range(20):
    payload = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "value": round(20 + random.random() * 5, 3),
        "sensor": "demo1",
    }
    ch.basic_publish(exchange="", routing_key="sensor_queue", body=json.dumps(payload).encode())
    print("[x] Sent", payload)
    time.sleep(1)

conn.close()
