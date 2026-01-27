import os
import time
import pika

host = os.getenv("RABBITMQ_HOST", "localhost")
queue = os.getenv("QUEUE_NAME", "demo_queue")

def connect():
    params = pika.ConnectionParameters(host=host, heartbeat=30)
    return pika.BlockingConnection(params)

while True:
    try:
        conn = connect()
        ch = conn.channel()
        ch.queue_declare(queue=queue, durable=False)
        print(f"[receiver] waiting on queue={queue} host={host}", flush=True)

        def on_message(ch, method, properties, body):
            print(f"[receiver] got: {body.decode()}", flush=True)
            ch.basic_ack(delivery_tag=method.delivery_tag)

        ch.basic_consume(queue=queue, on_message_callback=on_message, auto_ack=False)
        ch.start_consuming()
    except Exception as e:
        print(f"[receiver] error: {e} (retrying in 2s)", flush=True)
        time.sleep(2)
