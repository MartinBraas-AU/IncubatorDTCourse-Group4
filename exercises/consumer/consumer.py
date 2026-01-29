import json
import os
import time

import pika
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
QUEUE_NAME = os.getenv("QUEUE_NAME", "sensor_queue")
INFLUX_URL = os.getenv("INFLUX_URL", "http://influxdb:8086")
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN", "")
INFLUX_ORG = os.getenv("INFLUX_ORG", "dt-course")
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET", "sensor-data")


def connect_rabbitmq():
    while True:
        try:
            conn = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
            return conn
        except pika.exceptions.AMQPConnectionError:
            print("[!] RabbitMQ not ready, retrying in 3s...")
            time.sleep(3)


influx = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
write_api = influx.write_api(write_options=SYNCHRONOUS)

conn = connect_rabbitmq()
ch = conn.channel()
ch.queue_declare(queue=QUEUE_NAME, durable=True)
ch.basic_qos(prefetch_count=1)

print(f"[*] Consumer waiting on {QUEUE_NAME} @ {RABBITMQ_HOST}")


def on_message(ch, method, properties, body):
    data = json.loads(body.decode())
    print("[x] Received:", data)

    point = (
        Point("temperature")
        .tag("sensor", data["sensor"])
        .field("value", float(data["value"]))
        .time(data["ts"], WritePrecision.S)
    )
    write_api.write(bucket=INFLUX_BUCKET, record=point)
    ch.basic_ack(delivery_tag=method.delivery_tag)


ch.basic_consume(queue=QUEUE_NAME, on_message_callback=on_message, auto_ack=False)
ch.start_consuming()
