import json
import os
import socket
import time
import random
from datetime import datetime, timezone

import pika

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
QUEUE_NAME = os.getenv("QUEUE_NAME", "sensor_queue")
SENSOR_ID = os.getenv("SENSOR_ID", socket.gethostname())
INTERVAL = float(os.getenv("INTERVAL", "2"))


def connect():
    while True:
        try:
            conn = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
            return conn
        except pika.exceptions.AMQPConnectionError:
            print("[!] RabbitMQ not ready, retrying in 3s...")
            time.sleep(3)


conn = connect()
ch = conn.channel()
ch.queue_declare(queue=QUEUE_NAME, durable=True)

print(f"[*] Producer {SENSOR_ID} publishing to {QUEUE_NAME} every {INTERVAL}s")

while True:
    payload = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "value": round(20 + random.random() * 5, 3),
        "sensor": SENSOR_ID,
    }
    ch.basic_publish(exchange="", routing_key=QUEUE_NAME, body=json.dumps(payload).encode())
    print("[x] Sent", payload)
    time.sleep(INTERVAL)
