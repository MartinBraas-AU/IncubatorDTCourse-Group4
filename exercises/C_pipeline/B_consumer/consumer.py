import os
import pika

host = os.getenv("RABBITMQ_HOST", "rabbitmq")
queue = os.getenv("QUEUE_NAME", "hello")

conn = pika.BlockingConnection(pika.ConnectionParameters(host))
ch = conn.channel()
ch.queue_declare(queue=queue, durable=True)

print(f"[*] Waiting on {queue} @ {host}")

def cb(ch, method, props, body):
    print("[x] Received:", body.decode())
    ch.basic_ack(delivery_tag=method.delivery_tag)

ch.basic_qos(prefetch_count=1)
ch.basic_consume(queue=queue, on_message_callback=cb, auto_ack=False)
ch.start_consuming()
