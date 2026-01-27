import pika
import time

conn = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
ch = conn.channel()
ch.queue_declare(queue="hello", durable=True)

for i in range(10):
    msg = f"hello #{i}"
    ch.basic_publish(exchange="", routing_key="hello", body=msg)
    print("[x] Sent", msg)
    time.sleep(0.3)

conn.close()
